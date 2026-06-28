---
title: 'RF/SDR Exploration & Decoding (RTL-SDR on-ramp)'
number: '03-025'
category: 'homelab-automation'
difficulty: 'Medium'
time_commitment: '1-4 weeks'
target_skills: 'SDR fundamentals, GNU Radio, Universal Radio Hacker, rtl_433, DSP basics, HA/MQTT integration'
status: 'Not Started'
depends_on:
  - hardware/rtl-sdr
  - homelab/home-assistant
---

# RF/SDR Exploration & Decoding (RTL-SDR on-ramp)

## Description

The "Model B" on-ramp to RF: a cheap **RTL-SDR + open PC software** as a transferable foundation,
rather than a locked-in appliance. Key framing — **decouple the radio from the software**: the
software ecosystem (GNU Radio, SDR++, Universal Radio Hacker, rtl_433) is **hardware-agnostic via
SoapySDR**, so the skills carry forward to any future SDR (HackRF/bladeRF) without re-learning. You
do NOT need a specific device for these tools to be useful — unlike Flipper/PortaPack apps, which
are firmware locked to that gadget.

Goal: learn RF hands-on through a progression of receive-and-decode projects, and land real value
by pulling 433 MHz sensors into Home Assistant.

## Why RTL-SDR first

- ~$35, receive-only, 500 kHz–1.7 GHz, ~2.4 MHz BW — perfect to *learn* on.
- Universal software; skills transfer to every fancier SDR.
- Most of what makes RF fun is **RX** (see TX note below). Buy RX now; add TX only with a goal.
- ⚠️ Buy genuine from **rtl-sdr.com** (v4) — counterfeits are rampant.

## Progression (each a self-contained win)

1. **ADS-B** — decode aircraft (dump1090) and plot live planes. Classic first success, ~1 afternoon.
2. **Broadcast/NOAA** — FM, then decode NOAA weather-satellite APT images (antenna matters).
3. **rtl_433 → HA** — receive your 433 MHz sensors (weather stations, TPMS, door sensors) and pipe
   them into Home Assistant via **rtl_433 → MQTT → HA auto-discovery**. *This is the homelab payoff.*
4. **Pagers/ships** — POCSAG (paging) and AIS (ship transponders) for variety.
5. **Protocol RE** — capture an unknown signal and reverse it in **Universal Radio Hacker** (auto
   modulation detect). Note: URH went read-only/archived Mar 2026 — still the best tool, unmaintained.
6. **GNU Radio** — build a simple flowgraph; this is the skill that scales to wideband SDRs later.

## When TX earns its keep (the upgrade decision)

RX = observe/learn/decode. **TX = control/emulate/act.** Only add a transmitter for a specific
act-on-the-air goal. Genuinely useful TX cases:

- **Control no-smart-integration devices** — transmit 433 MHz/IR to garage/blinds/fans/RF outlets
  → into HA. *(The main everyday win — overlaps with [[03-019]] IR blaster.)*
- **Security-test your *own* fobs/locks** — replay to learn fixed-code vs rolling-code.
- **Ham radio** *(license required)* — digital modes, APRS, satellites, repeaters.
- **Prototype your own RF devices** (LoRa/sensor nets) · **RF signal-generator** test bench.

**Buy implication:** for practical "control my stuff" TX you do **not** need a HackRF — a **$5
CC1101/ESP32** or **$40 Broadlink** does sub-GHz TX better and integrates with HA. Wideband SDR TX
(HackRF/bladeRF) is for research/ham/odd frequencies only.

⚖️ **Responsible use:** TX is regulated. Stay on **your own devices, ISM bands (433/915 MHz,
2.4 GHz), low power**, or get a ham license for amateur bands. Never transmit on
cellular/aviation/public-safety/licensed bands, never jam, never replay others' devices.

## Exit Criteria

- [ ] Genuine RTL-SDR v4 + a decent antenna set in hand
- [ ] At least 3 RX wins decoded (e.g. ADS-B, NOAA APT, rtl_433 sensors)
- [ ] 433 MHz sensors flowing into Home Assistant via rtl_433 → MQTT
- [ ] One protocol reverse-engineered in URH (or one GNU Radio flowgraph built)
- [ ] A written decision on whether/what TX hardware to add (and for which concrete goal)

## Shopping list (~$35–60)

- RTL-SDR Blog v4 kit (~$35, includes antennas) from rtl-sdr.com
- (later, only with a TX goal) CC1101/ESP32 (~$5–35) or Broadlink RM4 Pro (~$40), or a HackRF/bladeRF for research/ham

## Progress

- [x] Framing: Model-B (decoupled HW/SW) on-ramp; TX decision deferred to a concrete goal (2026-06-27)
- [ ] Acquire RTL-SDR + antennas
- [ ] Work the RX progression
- [ ] rtl_433 → HA integration
- [ ] TX decision
