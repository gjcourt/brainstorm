---
title: 'ESP32-based IR Blaster for Legacy Devices'
number: '03-019'
category: 'homelab-automation'
difficulty: 'Easy'
time_commitment: '1-2 days'
target_skills: 'IR LEDs/Receivers, Signal Decoding, ESPHome'
status: 'In Progress'
depends_on:
  - hardware/esp32
  - homelab/home-assistant
---

# ESP32-based IR Blaster for Legacy Devices

## Description

Build a device that can record and transmit infrared (IR) signals. Use it to integrate legacy
devices (like an old TV, amplifier, or portable AC unit) into your Home Assistant automations.

**Concrete goal (2026-06):** replace the pile of cheap audio-gear remotes with one generalized
controller, surfaced in Home Assistant (phone, dashboards, automations). Confirmed the remotes
are **mainly IR**, not RF — so this is an IR-blaster job, not an SDR/RF job (no SDR can learn or
transmit IR).

## Approach (decided after RF-landscape research)

**Step 0 — per-remote IR vs RF check.** Point each remote at a phone's **front/selfie camera**
and press a button → flashing light = IR. (Use the *front* camera: many modern rear cameras have
IR-cut filters and show nothing even for real IR.) Anything that shows no flash *and* works
through walls / off-axis is 433 MHz RF — handle those separately (below).

**Primary build — ESP32 + ESPHome IR transceiver (~$15, local-first, best homelab fit):**
- ESP32 dev board running ESPHome `remote_receiver` (TSOP38238-class IR receiver) to *learn*
  codes, and `remote_transmitter` (IR LED) to *send* them. Native, fully-local HA integration —
  no cloud, no lock-in.
- ⚠️ Drive the IR LED through an **NPN transistor** (e.g. 2N2222) + current-limit resistor, never
  straight off a GPIO — direct-drive range is inches. With a transistor you get whole-room range.
- Learn each remote's codes from the ESPHome receiver logs (or capture with a Flipper), paste the
  protocol/code into YAML as HA buttons.
- No-solder option: **Athom** sells a pre-built ESPHome RF433+IR unit if you'd rather not build.

**Quick alternative — Broadlink RM4 Pro (~$40, plug-and-play):** IR *and* 433 MHz RF in one box,
native HA `broadlink` integration that can run fully local. Setup gotcha: it's cloud-capable — set
Wi-Fi in the Broadlink app, then **quit the app and configure in HA** to avoid cloud mode; a
firmware update can re-assert cloud, which the ESP32 route avoids entirely.

**For any 433 MHz RF stragglers:** the same Broadlink RM4 Pro absorbs 433 learn/replay, or go
local with a Sonoff RF Bridge R2 + Tasmota + Portisch → MQTT → HA. (Do NOT expect RTL-SDR to
control anything — it's receive-only.)

## Exit Criteria

- [ ] Every audio-gear remote inventoried + tagged IR or RF (front-camera test)
- [ ] One ESP32+ESPHome blaster flashed and adopted in Home Assistant
- [ ] Each target device controllable from HA (power, volume, input) at whole-room range
- [ ] HA dashboard/remote card (and at least one automation) replacing the physical remotes
- [ ] Fully local — no cloud dependency

## Shopping list (~$15)

- ESP32 dev board · IR LED + 2N2222 (or similar) NPN transistor + resistor · TSOP38238 IR receiver
- (or) Athom pre-built ESPHome IR+RF433 unit (~$15–20) · (or) Broadlink RM4 Pro (~$40) for instant

## Progress

- [x] Research: IR vs RF, tool landscape, approach decided (2026-06-27)
- [ ] Inventory + IR/RF test all remotes
- [ ] Build/flash ESP32 ESPHome blaster
- [ ] Learn codes + HA entities
- [ ] Documentation
