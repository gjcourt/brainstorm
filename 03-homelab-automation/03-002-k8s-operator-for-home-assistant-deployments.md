---
title: 'K8s Operator for Home Assistant Deployments'
number: '03-002'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Months'
target_skills: 'Go, Kubernetes API, kubebuilder / Operator SDK, controller-runtime'
status: 'Not Started'
depends_on:
  - homelab/home-assistant
  - homelab/talos
---

# K8s Operator for Home Assistant Deployments

## Description

Build a custom Kubernetes Operator in Go that manages the lifecycle of Home Assistant instances,
including automated backups, structured restore, declarative config injection, and (optionally) an
mDNS reflector DaemonSet for LAN discovery.

## Exit Criteria

- [ ] `HomeAssistantInstance` CRD installed in cluster; `kubectl get homeassistantinstances` works
- [ ] Controller reconciles a `HomeAssistantInstance` CR to a running HA Pod/Deployment with correct
      config
- [ ] Automated backup: each instance spec includes a backup schedule (cron) and retention; the
      operator drives a per-instance backup pipeline (CronJob + Job, Velero `Schedule`, or CSI
      volume snapshot — choice deferred to Phase 1) whose output lands in a configured S3 bucket or
      PVC and respects retention
- [ ] Config injection: a referenced ConfigMap is mounted as a read-only fragment under `/config/`
      (e.g. `packages/operator.yaml`) and pulled in via HA's `!include`/`packages:` mechanism so it
      does not collide with HA's writable state in `/config`; ConfigMap changes trigger a rolling
      restart of HA
- [ ] Restore subresource / CR: a structured `HomeAssistantRestore` CR (or `spec.restore` block with
      explicit `completed` status) drives restores — _not_ free-form annotations — so the operation
      is idempotent and auditable
- [ ] mDNS discovery (optional): operator can run an avahi reflector on the host network as a
      DaemonSet selected by node label (_not_ a pod-network sidecar — Pod overlay does not carry
      link-local multicast); gated by `spec.proxy.enabled`
- [ ] `.status` subresource: phase field reflects `Pending / Running / BackupInProgress / Degraded`;
      last backup timestamp and backup count exposed
- [ ] Operator deployed via Helm chart committed to homelab GitOps repo (Flux reconciles it)
- [ ] Existing HA instance migrated from manual Helm/Flux config to operator-managed
      `HomeAssistantInstance` CR
- [ ] End-to-end test documented: delete CR + PVC, re-apply CR _plus_ a `HomeAssistantRestore`
      pointing at the most recent backup, verify HA starts with restored config and data
      (auto-restore from latest is explicitly out of scope — restores are always user-driven so the
      controller cannot silently overwrite a deliberately empty volume)

## Progress

### Phase 1 – Research & Architecture

- [ ] Audit current HA deployment in homelab repo (Helm chart, volume layout, config structure)
- [ ] Build-vs-buy decision for backup: evaluate Velero (cluster-scoped, PVC snapshots) vs an
      operator-owned CronJob/Job pipeline; document which problem each solves and pick one
- [ ] Tooling choice: kubebuilder + controller-runtime, or Operator SDK (which wraps both) — note
      this is a developer-experience decision, not an architectural one
- [ ] Design `HomeAssistantInstance` CRD spec (fields: image, configMapRef, backup spec, proxy spec,
      storage); prefer CEL validation rules (stable since K8s 1.29) over a validating webhook for
      the v1 schema
- [ ] Design backup storage interface (abstract over S3 and PVC backends)
- [ ] Identify proxy use case up front (mDNS reflection for LAN discovery) and decide whether to
      ship it at all in v0.1 — it is not on the critical path for HA reconciliation
- [ ] Write Architecture Decision Record (ADR) for operator design

### Phase 2 – Scaffold & CRD

- [ ] Scaffold Go module with kubebuilder (or Operator SDK; both produce a controller-runtime
      project)
- [ ] Define `HomeAssistantInstance` Go types and generate CRD YAML via `controller-gen`
- [ ] Write CRD validation: prefer CEL `x-kubernetes-validations` for required fields and
      cross-field rules; only add a validating webhook if a check needs cluster lookups
- [ ] Install CRD in dev cluster; verify `kubectl get homeassistantinstances` works
- [ ] Set up basic controller loop (create/watch/reconcile skeleton)

### Phase 3 – Core Reconciliation

- [ ] Reconcile Deployment (image, replicas, resource limits from spec)
- [ ] Reconcile Service (ClusterIP + optional LoadBalancer)
- [ ] Reconcile PVC for `/config` volume
- [ ] Implement finalizer to take a final backup before delete; include a
      `ha-operator/skip-final-backup: "true"` annotation escape hatch so a stuck backup cannot wedge
      namespace deletion
- [ ] Update `.status.phase` on each reconcile pass
- [ ] Unit tests for reconcile logic (envtest)

### Phase 4 – Config Injection

- [ ] Watch referenced ConfigMap for changes
- [ ] Mount ConfigMap read-only at a non-conflicting path (e.g. `/config/packages/operator.yaml` or
      `/operator-config/`) and reference it from HA via `!include` / `packages:` so HA's own writes
      to `/config` are not shadowed by the read-only ConfigMap volume
- [ ] Trigger rolling restart on ConfigMap change (hash the ConfigMap data and stamp the hash as a
      `pod-template` annotation on the Deployment)
- [ ] Integration test: update ConfigMap, verify pod restarts with new config and that HA's writable
      state under `/config` survives the restart

### Phase 5 – Backup & Restore

- [ ] Define `BackupSpec` (schedule cron, retention count, destination type, S3/PVC params); if
      Phase 1 picked Velero, this becomes a thin wrapper around a `Schedule` CR instead
- [ ] Reconcile the chosen backup driver per instance: CronJob+Job (operator-owned), a Velero
      `Schedule` (if Phase 1 picked Velero), or a periodic `VolumeSnapshot` reconciler
- [ ] If self-owned: implement the backup Job image/script — snapshot `/config` (rsync or `tar` from
      a paused HA, or a CSI volume snapshot), upload to S3 or copy to PVC
- [ ] Store backup metadata (timestamp, size, location, source-instance UID) in `.status.backups[]`
- [ ] Define a `HomeAssistantRestore` CR (or `spec.restore: { source, completed }` block) that the
      reconciler consumes to drive a pre-start init container which downloads + extracts the
      requested backup; mark `completed` so the same restore is not re-applied on every reconcile
- [ ] Test backup + restore end-to-end in dev cluster

### Phase 6 – mDNS Reflector (optional)

- [ ] Confirm the LAN-discovery requirement still exists after Phase 1 (skip this phase entirely if
      not)
- [ ] Deploy avahi-daemon in reflector mode as a `DaemonSet` on `hostNetwork: true` with a
      node-selector — _not_ as a Pod-network sidecar. mDNS is link-local multicast (224.0.0.251 /
      ff02::fb) and does not traverse the Pod overlay (Cilium/Flannel/etc.); only host-network or an
      L2-aware reflector can bridge it
- [ ] Expose proxy config fields in CRD spec (`spec.proxy.enabled`, `spec.proxy.nodeSelector`)
- [ ] Test mDNS discovery from a LAN client (`avahi-browse -a`) reaches the HA Service VIP

### Phase 7 – Helm Chart & GitOps Integration

- [ ] Build Helm chart (CRD, RBAC, Deployment, ServiceAccount)
- [ ] Add chart to homelab repo under `apps/ha-operator/`
- [ ] Create Flux HelmRelease manifest
- [ ] Migrate existing HA Helm release to `HomeAssistantInstance` CR
- [ ] Verify Flux reconciles operator and managed instance cleanly

### Phase 8 – Hardening & Documentation

- [ ] Chaos test: drain HA node mid-backup; verify backup resumes or is retried
- [ ] Measure and document backup timing for typical config size
- [ ] Write operator README: CRD field reference, backup/restore runbook, upgrade path
- [ ] Tag v0.1.0 release; build and push image to `ghcr.io/gjcourt/ha-operator` and pin the same tag
      in the Helm chart's `values.yaml`
