---
title: 'eBPF-based Network Traffic Analyzer'
number: '03-001'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Months'
target_skills: 'C, eBPF, Go, Linux Kernel (optional: Rust userspace)'
status: 'Not Started'
depends_on:
  - homelab/prometheus
  - homelab/talos
---

# eBPF-based Network Traffic Analyzer

## Description

Build a per-node DaemonSet that attaches eBPF programs (written in C, loaded via libbpf-style CO-RE)
to host network interfaces and key kernel hooks on the Talos cluster, aggregates kernel-level
traffic and TCP-stack signals into per-CPU BPF maps, and exposes them as Prometheus metrics through
a userspace agent (Go via `cilium/ebpf`, optionally Rust via `aya` for the userspace half).

The cluster already runs Cilium, which provides eBPF-based L3/L4/L7 flow observability via Hubble.
This project deliberately does **not** duplicate Hubble. It targets two areas Hubble does not cover
well:

1. **Depth** — kernel-level signals (TCP retransmits, smoothed RTT, congestion events, DNS
   resolver-side latency) that Hubble's flow log does not surface.
2. **Coverage gaps** — host-network traffic, node-to-node management plane (Talos `apid`/`trustd`,
   kubelet), and off-cluster LAN traffic that Hubble does not see.

The project also carries an explicit **learning** goal: hands-on with C + libbpf + the BPF verifier,
CO-RE relocations, and the userspace BPF loader stack.

## Exit Criteria

- [ ] DaemonSet deployed to all 6 Talos nodes (3 control-plane + 3 worker), running ≥7 days
      continuously without OOM, restart, or BPF program load failures
- [ ] eBPF programs cover: TC ingress + TC egress on the primary host NIC, `fentry`/`fexit` on
      `tcp_retransmit_skb`, `fentry`/`fexit` on `tcp_rcv_established` (RTT extraction), and a kprobe
      on `udp_sendmsg` filtered to UDP/53 for DNS query latency
- [ ] At least 10 distinct Prometheus metric series per node exposed by the userspace agent (mix of
      counters, gauges, histograms)
- [ ] Grafana dashboard with at least 3 panels showing signals **not** available from Hubble:
  - TCP retransmit rate by node (counter rate)
  - Smoothed-RTT histogram per peer (on-cluster + off-cluster)
  - DNS query latency p50 / p95 / p99 from the host resolver
- [ ] Steady-state CPU overhead ≤2% of one core per node under typical homelab load
- [ ] Steady-state memory ≤64 MiB resident per agent pod
- [ ] Coexists cleanly with Cilium's TC programs — verified via `bpftool net show dev <iface>` on a
      stage node showing both Cilium and project programs attached, with documented attach order
- [ ] Source repository (`gjcourt/netscope` or equivalent) contains: README, architecture doc, build
      instructions, CO-RE / `vmlinux.h` regeneration steps, and Talos-specific deployment notes
- [ ] Helm chart or Flux Kustomization in `gjcourt/homelab` deploys the DaemonSet via GitOps; stage
      and prod overlays are distinct
- [ ] Postmortem document captures: what was learned, what surprised, what would be done
      differently, and an explicit "kill or continue" recommendation for ongoing maintenance

## Non-Goals

- **Reimplementing Hubble.** Standard L3/L4 flow logs and L7 HTTP visibility are Hubble's job; this
  project will not produce a parallel flow log.
- **Replacing node_exporter.** Generic host metrics stay with `node_exporter`; this project ships
  only signals that require eBPF.
- **Per-pod attribution as a v1 requirement.** Cgroup-ID-based pod correlation is real work and
  lives in Phase 5 (stretch). v1 attribution is per-node and per-peer-IP only.
- **L7 protocol parsing.** TLS SNI extraction and HTTP path inspection are stretch territory; the v1
  dataplane is L3/L4 + TCP-stack + DNS only.

## Architecture

```text
┌─────────────────── Talos node ───────────────────────────────┐
│                                                                │
│  Kernel hooks:                                                 │
│    TC clsact ingress  (eth0)  ── packet/byte counters         │
│    TC clsact egress   (eth0)  ── packet/byte counters         │
│    fentry tcp_retransmit_skb  ── retransmit counter           │
│    fentry tcp_rcv_established ── RTT histogram                │
│    kprobe udp_sendmsg :53     ── DNS query timing ringbuf     │
│                                                                │
│  BPF maps:                                                     │
│    per-CPU array  : packet/byte counters                      │
│    per-CPU hash   : retransmit counts keyed by 4-tuple        │
│    per-CPU hist   : RTT buckets (log2)                        │
│    ringbuf        : DNS events for userspace timing match     │
│                                                                │
│  ┌──────── Userspace pod (DaemonSet, hostNetwork) ─────────┐  │
│  │  Go binary using github.com/cilium/ebpf                  │  │
│  │  (or Rust binary using aya, see §"Userspace language")   │  │
│  │                                                           │  │
│  │  - Loads .o produced by clang -target bpf                │  │
│  │  - Attaches programs to hooks                            │  │
│  │  - Scrapes per-CPU maps every N seconds                  │  │
│  │  - Drains DNS ringbuf, computes query→response latency   │  │
│  │  - Exposes /metrics on :9101                             │  │
│  └─────────────────────────┬─────────────────────────────────┘ │
└────────────────────────────┼───────────────────────────────────┘
                             │ scrape
                       ┌─────▼─────┐
                       │ Prometheus│ ──→ Grafana dashboards
                       └───────────┘
```

### Userspace language

Default: **Go + `github.com/cilium/ebpf`**. The brainstorm names Go as a target skill, the library
is mature and used in production by Cilium, and `bpf2go` produces typed bindings from the C `.o`.

Optional swap: **Rust + `aya`** for the userspace half if Go feels limiting after Phase 2. Aya is
pure-Rust (no libbpf dependency) and has a pleasant typed-map API. Kernel-side stays in C either way
— switching kernel-side to Rust is explicitly out of scope (the brainstorm names C as a target
skill, and C + libbpf is the canonical kernel-side BPF path).

### Talos-specific constraints

Talos is an immutable-OS distribution; kernel-side BPF runs in userspace pods, but the deployment
model has more constraints than a generic Linux host. Items to validate in Phase 0:

- **BTF availability** — `/sys/kernel/btf/vmlinux` must exist on every node. Required for CO-RE.
- **Kernel version** — Talos v1.12.4 ships kernel 6.x (verify exact version on cluster); confirm
  `fentry`/`fexit` and ringbuf are available.
- **Capabilities** — pod needs `CAP_BPF`, `CAP_PERFMON`, `CAP_NET_ADMIN`. `CAP_SYS_ADMIN` may be
  required for some attach paths on older kernels; prefer narrower caps if possible.
- **Pod Security Admission** — namespace must be labeled
  `pod-security.kubernetes.io/enforce=privileged`. PSA `restricted` blocks `hostNetwork` and
  elevated caps.
- **Filesystem** — `/sys/fs/bpf` mounted into the pod (hostPath) for pinned maps; `/sys/kernel/btf`
  read-only for BTF access.
- **`hostNetwork: true`** required to attach to physical interfaces.
- **Cilium coexistence** — Cilium attaches its own TC programs via clsact. Multiple programs can
  attach to the same hook; verify ordering with `bpftool net show dev <iface>` on stage and document
  the resulting attach order in the README.
- **SOPS / GitOps** — per repo convention, secret-bearing manifests land as draft PRs with
  `.yaml.example` templates and CI is the gate. This project should not need secrets, but if a
  scrape-auth token is added, it follows that flow.

## Progress

### Phase 0 — Feasibility Spike (≈1 week)

Prove the riskiest assumptions on a single staging node before committing.

- [ ] Verify `/sys/kernel/btf/vmlinux` exists on a Talos worker node
- [ ] Build a minimal C BPF program (TC ingress, byte counter) with `clang -target bpf` against a
      Talos-pinned `vmlinux.h`
- [ ] Build a minimal Go loader using `cilium/ebpf` that loads the program, attaches to a single
      interface, reads the map, prints to stdout
- [ ] Run the loader as a `Pod` (not yet a DaemonSet) in a privileged staging namespace; confirm
      attachment with `bpftool prog list` via `nsenter` or talosctl debug
- [ ] Confirm Cilium does not block the additional TC attach; document program ordering
- [ ] **Decision gate:** if any of the above fail and cannot be resolved within the spike, kill the
      project and write the postmortem

### Phase 1 — DaemonSet Skeleton (≈2 weeks)

- [ ] Create new repo `gjcourt/netscope` (or naming TBD); decide layout: `bpf/` (C source),
      `cmd/agent/` (Go), `deploy/` (Helm chart)
- [ ] CI: `make build` produces `.o` via clang and Go binary; cross-builds for amd64 (homelab is
      x86)
- [ ] DaemonSet manifest with correct caps, hostNetwork, hostPath mounts, PSA label
- [ ] Single packet-counter metric exposed at `/metrics` per node
- [ ] Helm chart published in repo; Flux Kustomization PR opened against `gjcourt/homelab` for stage
      overlay only
- [ ] Stage Prometheus scraping the new agent; one Grafana panel showing per-node packet rate
- [ ] **Validation:** rollout to all 3 stage nodes succeeds; agent pods stable for 24 hours

### Phase 2 — Core Depth Metrics (≈3 weeks)

- [ ] `fentry`/`fexit` on `tcp_retransmit_skb` — per-4-tuple retransmit counter
- [ ] `fentry`/`fexit` on `tcp_rcv_established` — extract `tcp_sock->srtt_us`, populate log2
      histogram
- [ ] kprobe on `udp_sendmsg` filtered to dport 53 — emit DNS query event to ringbuf with timestamp
      and 5-tuple
- [ ] kprobe on `udp_recvmsg` (or tracepoint equivalent) for matching DNS response — userspace
      computes RTT
- [ ] Userspace agent: drain ringbuf, maintain in-flight DNS query table with TTL eviction, compute
      and export latency histogram
- [ ] Grafana dashboard: 3 required panels (retransmit rate, SRTT histogram, DNS latency
      percentiles)
- [ ] **Validation:** all 3 panels show plausible data on stage for 48 hours; no verifier load
      failures across 3 stage nodes

### Phase 3 — Production Rollout (≈2 weeks)

- [ ] Open Flux PR for prod overlay
- [ ] Roll out to one prod worker node first; observe for 24 hours
- [ ] Roll out to remaining workers, then control-plane nodes one at a time
- [ ] 7-day soak on prod; track CPU + memory overhead in Grafana
- [ ] Tune scrape interval, map sizes, ringbuf size based on observed load
- [ ] Document any incidents or surprises in the repo postmortem doc
- [ ] **Validation:** all 6 nodes running ≥7 days continuously meeting CPU/memory budgets

### Phase 4 — Documentation & Postmortem (≈1 week)

- [ ] README in `netscope` repo: overview, build, deploy, troubleshoot
- [ ] Architecture doc: program-by-program walkthrough, map design, attach ordering with Cilium
- [ ] CO-RE / `vmlinux.h` regeneration runbook (for Talos kernel upgrades)
- [ ] Postmortem with explicit kill-or-continue recommendation for ongoing maintenance burden
- [ ] Update this brainstorm doc: status `Complete`, link to repo and dashboards

### Phase 5 — Stretch Goals (open-ended; only if Phases 0–4 land cleanly)

- [ ] Per-pod attribution: read cgroup ID from BPF context, correlate to Pod via cgroupv2 hierarchy
      lookup in userspace
- [ ] L7 — TLS SNI extraction at TC egress for outbound HTTPS visibility
- [ ] L7 — HTTP request path / status extraction (cleartext only) at TC egress
- [ ] Userspace rewrite to Rust + aya — direct comparison of ergonomics, build complexity, and
      runtime resource footprint vs the Go implementation
- [ ] XDP variant of the ingress counter for line-rate measurement; CPU comparison vs TC

## Risks & Tradeoffs

| Risk                                                                   | Mitigation                                                                                                                        |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Talos kernel does not expose a needed hook (e.g. `fentry` unavailable) | Phase 0 validates the riskiest hooks first; fall back to tracepoints if `fentry`/`fexit` is unavailable                           |
| BPF verifier rejects programs (loop bounds, complexity limits)         | Keep individual programs small; use bounded loops; prefer per-CPU maps; iterate on stage                                          |
| CPU overhead exceeds budget at LAN line rate                           | XDP at NIC RX is the escape hatch for hot paths; TC tail-calls keep individual programs cheap; tune scrape interval               |
| Talos kernel upgrade breaks verifier-passing programs                  | CO-RE relocations + pinned `vmlinux.h` snapshot per kernel release; CI loads programs against multiple kernel BTFs                |
| Cilium TC ordering causes traffic to bypass project programs           | Validate via `bpftool net show` on stage; document attach order; coordinate with Cilium chain priority                            |
| Project duplicates Hubble and adds no real value                       | Exit criteria explicitly require ≥3 panels Hubble cannot produce; if Phase 2 cannot hit that bar, kill the project                |
| Maintenance burden post-build (kernel upgrades, BPF API churn)         | Postmortem in Phase 4 includes explicit kill-or-continue recommendation; project is allowed to be archived as a learning artifact |
| Userspace memory growth from in-flight DNS query table                 | TTL eviction in agent; bounded map size in BPF; alert if eviction count climbs                                                    |

## Open Questions

- **Repo placement** — new top-level repo `gjcourt/netscope`, or subdirectory in `gjcourt/homelab`?
  Recommendation: new repo (different lifecycle, different toolchain — C + clang + Go).
- **Naming** — `netscope`, `nettrace`, `kprobe-exporter`, something else?
- **Image build** — multi-stage Dockerfile with clang in builder stage; final image scratch or
  distroless? `ghcr.io/gjcourt/netscope` per homelab convention.
- **Metric prefix** — `netscope_*` or follow `node_*` convention from node_exporter?
- **Phase 5 commitment** — is per-pod attribution a real requirement or a learning curiosity? It is
  the single largest piece of post-v1 work and should be decided before Phase 4 closes.
