---
title: 'K8s Operator for Home Assistant Deployments'
number: '03-002'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Months'
target_skills: 'Go, Kubernetes API, Operator SDK'
status: 'Not Started'
depends_on:
  - homelab/home-assistant
  - homelab/talos
---

# K8s Operator for Home Assistant Deployments

## Description

Build a custom Kubernetes Operator in Go that manages the lifecycle of Home Assistant instances,
including automated backups, configuration injection, and sidecar proxy management for external
access.

## Exit Criteria

- [ ] `HomeAssistantInstance` CRD installed in cluster; `kubectl get homeassistantinstances` works
- [ ] Controller reconciles a `HomeAssistantInstance` CR to a running HA Pod/Deployment with correct config
- [ ] Automated backup: each instance spec includes a backup schedule (cron); operator creates/manages a CronJob that tars the HA config dir and stores to a configured S3 bucket or PVC
- [ ] Backup restore: annotating an instance with `ha-operator/restore: latest` (or a specific backup name) triggers restore from backup before HA pod starts
- [ ] Config injection: a referenced ConfigMap drives HA `configuration.yaml`; changes to the ConfigMap trigger a rolling restart of HA
- [ ] Sidecar proxy: operator injects an optional mDNS proxy sidecar (configurable via spec field) for local network discovery without exposing HA directly
- [ ] `.status` subresource: phase field reflects `Pending / Running / BackupInProgress / Degraded`; last backup timestamp and backup count exposed
- [ ] Operator deployed via Helm chart committed to homelab GitOps repo (Flux reconciles it)
- [ ] Existing HA instance migrated from manual Helm/Flux config to operator-managed `HomeAssistantInstance` CR
- [ ] End-to-end test documented: delete CR + PVC, re-apply CR, verify HA starts with restored config and data

## Progress

### Phase 1 – Research & Architecture

- [ ] Audit current HA deployment in homelab repo (Helm chart, volume layout, config structure)
- [ ] Compare controller-runtime vs Operator SDK; document choice and rationale
- [ ] Design `HomeAssistantInstance` CRD spec (fields: image, configMapRef, backup spec, proxy spec, storage)
- [ ] Design backup storage interface (abstract over S3 and PVC backends)
- [ ] Write Architecture Decision Record (ADR) for operator design

### Phase 2 – Scaffold & CRD

- [ ] Scaffold Go module with controller-runtime (or Operator SDK)
- [ ] Define `HomeAssistantInstance` Go types and generate CRD YAML
- [ ] Write CRD validation (CEL rules or webhook) for required fields
- [ ] Install CRD in dev cluster; verify `kubectl get homeassistantinstances` works
- [ ] Set up basic controller loop (create/watch/reconcile skeleton)

### Phase 3 – Core Reconciliation

- [ ] Reconcile Deployment (image, replicas, resource limits from spec)
- [ ] Reconcile Service (ClusterIP + optional LoadBalancer)
- [ ] Reconcile PVC for `/config` volume
- [ ] Implement finalizer to block deletion until backup completes
- [ ] Update `.status.phase` on each reconcile pass
- [ ] Unit tests for reconcile logic (envtest)

### Phase 4 – Config Injection

- [ ] Watch referenced ConfigMap for changes
- [ ] Mount ConfigMap as `/config/configuration.yaml`
- [ ] Trigger rolling restart on ConfigMap change (bump annotation on Deployment)
- [ ] Integration test: update ConfigMap, verify pod restarts with new config

### Phase 5 – Backup System

- [ ] Define BackupSpec (schedule cron, retention count, destination type, S3/PVC params)
- [ ] Reconcile CronJob per instance from BackupSpec
- [ ] Implement backup Job image/script: tar `/config`, upload to S3 or copy to PVC
- [ ] Store backup metadata (timestamp, size, location) in instance status
- [ ] Implement restore path: pre-start init container reads annotation, downloads backup, extracts
- [ ] Test backup + restore end-to-end in dev cluster

### Phase 6 – Sidecar Proxy

- [ ] Identify proxy use case (mDNS reflection for local discovery)
- [ ] Choose proxy image (avahi-daemon sidecar or udp-proxy)
- [ ] Implement optional sidecar injection via PodSpec template when `spec.proxy.enabled: true`
- [ ] Expose proxy config fields in CRD spec
- [ ] Test mDNS discovery through sidecar from LAN client

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
- [ ] Tag v0.1.0 release; push image to ghcr.io/gjcourt/ha-operator
