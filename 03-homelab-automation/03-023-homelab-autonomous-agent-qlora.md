---
title: 'Homelab Autonomous Agent — QLoRA Fine-Tuned Qwen2.5-Coder-32B'
number: '03-023'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Months'
target_skills: 'QLoRA Fine-Tuning, Agentic Scaffolding, Tool Use, LangGraph, kubectl/talosctl/flux CLI, Kubernetes, Axolotl'
status: 'Not Started'
---

# Homelab Autonomous Agent — QLoRA Fine-Tuned Qwen2.5-Coder-32B

## Description

An autonomous agent that can operate, debug, and evolve the homelab
infrastructure independently. Unlike the personal assistant (03-021) and
coach/mentor (03-022) which use Qwen3-32B as their base, this agent uses
**Qwen2.5-Coder-32B** as its base — pre-trained heavily on Kubernetes YAML,
Terraform, shell scripts, and infrastructure code, with significantly better
tool use in technical contexts.

The agent is not just a fine-tuned model — it's a model + agentic scaffold:
the LoRA adapter provides knowledge of the specific stack; a tool-calling
framework provides the ability to act.

Sibling project of 03-021 (personal assistant) and 03-022 (coach/mentor).

---

## Why Qwen2.5-Coder-32B (not Qwen3-32B)

| | Qwen3-32B | Qwen2.5-Coder-32B |
|---|---|---|
| General reasoning | ✅ Excellent | Good |
| Code / YAML / shell | Good | ✅ Excellent |
| Tool use (technical) | Good | ✅ Significantly better |
| Infrastructure tasks | Good | ✅ Pre-trained on this domain |

For an agent that needs to write kubectl patches, debug Flux kustomizations,
and reason about Cilium network policies, Coder-32B is the right base.

Note: this model runs as a separate base alongside Qwen3-32B in vLLM, not a
shared adapter. Two base models total on the hardware.

---

## Architecture: Model + Scaffold

```
User / cron trigger
       ↓
  Agent loop (LangGraph or custom)
       ↓
  Qwen2.5-Coder-32B + homelab LoRA
       ↓
  Tool calls:
    - kubectl (get, describe, patch, logs, exec)
    - talosctl (health, upgrade, reset)
    - flux (reconcile, get, suspend, resume)
    - git (branch, commit, push, PR via gh CLI)
    - helm (diff, upgrade)
    - curl (API calls, health checks)
    - bash (arbitrary shell)
       ↓
  Observe output → reason → next action
       ↓
  Human approval gate (configurable per action risk level)
```

The LoRA provides knowledge — what your specific cluster looks like, your
conventions, your incident history. The scaffold provides agency — the ability
to actually run commands and observe results.

---

## Training Data

Corpus from existing homelab repo:
- All Kubernetes YAML manifests (apps/, infra/)
- Flux kustomization configs and HelmRelease specs
- Incident reports (docs/incidents/) — teaches failure patterns and fixes
- Runbooks and guides (docs/guides/)
- talosctl / kubectl / flux CLI output patterns
- Git history and PR descriptions (what changed and why)
- AGENTS.md conventions

External corpus:
- Kubernetes documentation
- Talos Linux documentation
- Cilium documentation
- Flux CD documentation
- CloudNativePG documentation

Target dataset: 15,000–30,000 examples including:
- Natural language → kubectl/flux command pairs
- Incident description → diagnosis → fix sequences
- "What is wrong with this manifest?" → explanation + corrected YAML
- Multi-step troubleshooting traces

---

## Safety Model

Actions are tiered by risk:

| Tier | Examples | Gate |
|---|---|---|
| Read-only | kubectl get, describe, logs | Auto-approve |
| Low-risk write | flux reconcile, restart pod | Auto-approve with logging |
| Medium-risk | kubectl patch, git commit + PR | Require confirmation |
| High-risk | kubectl delete, talosctl reset | Always human approval |
| Destructive | node drain, cluster upgrade | Explicitly disallowed in agent loop |

---

## Training Stack

| Tool | Purpose |
|---|---|
| Axolotl | QLoRA training orchestrator |
| UnSloth | Training speedup |
| DeepSpeed ZeRO-2 | Multi-GPU |
| LangGraph | Agentic scaffold (stateful, cyclical agent loops) |
| vLLM | Serving (separate from Qwen3-32B instance) |

Estimated training time on 2x 4090s: 4–8 hours per iteration

---

## Exit Criteria

- [ ] Qwen2.5-Coder-32B base running in vLLM on GPU 0
- [ ] All homelab CLI tools wrapped as agent tools with structured outputs
- [ ] Homelab LoRA trained and loaded
- [ ] Agent loop with tiered approval gates operational
- [ ] Agent can diagnose a broken Flux kustomization from description alone
- [ ] Agent can draft and open a PR to fix a manifest issue
- [ ] Agent can run full health check of cluster and summarize state
- [ ] Logging and audit trail for all actions taken
- [ ] Notification delivery (Signal) for interventions and status updates

## Progress

- [ ] Hardware operational
- [ ] Qwen2.5-Coder-32B baseline serving
- [ ] Tool wrappers built (kubectl, flux, talosctl, git)
- [ ] Training corpus assembled from homelab repo
- [ ] First LoRA training run
- [ ] Agentic scaffold built in LangGraph
- [ ] Safety tiers implemented
- [ ] Integration test: end-to-end incident simulation
- [ ] Notification integration
- [ ] Documentation
