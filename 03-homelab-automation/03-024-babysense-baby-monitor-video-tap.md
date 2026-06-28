---
title: 'Babysense Baby-Monitor Video Tap (teardown → homelab stream)'
number: '03-024'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Weeks'
target_skills:
  'Hardware teardown, Logic analyzer/FPGA, SPI flash dump, Parallel-RGB (DPI) capture, SDR
  (optional), go2rtc/MediaMTX'
status: 'Not Started'
depends_on:
  - hardware/babysense-unit
  - hardware/sacrificial-parent-unit
  - homelab/home-assistant
---

# Babysense Baby-Monitor Video Tap (teardown → homelab stream)

## Description

Get the Babysense camera feed into the homelab as a network stream (RTSP/WebRTC → Home Assistant),
ideally without the head unit. The monitor is a **local-only 2.4 GHz digital video tx/rx** device
(no WiFi/cloud). This project is the _hacking_ path; the pragmatic fallback (a $30 LAN-only RTSP
cam) is noted at the end.

## Key findings (RF/hardware recon, 2026-06-27)

**Over-the-air interception is effectively infeasible** for a homelab tinkerer — three stacked
walls:

1. **Bandwidth:** the FHSS hop band is ~64–83 MHz wide; the widest affordable SDRs (bladeRF 2.0
   ~56–61 MHz, USRP B210 ~56 MHz) can't span it, and HackRF (20 MHz) isn't close. One missed hop
   corrupts frames.
2. **Hop sequence:** proprietary, pairing-derived — needs a firmware dump to recover.
3. **Codec:** undocumented proprietary video codec in the SoC; no open decoder. Never cracked
   publicly for this device class.

**Silicon (uniform across modern V43 / V24 / HD S2 / MaxView line):**

- **SONiX SN93xxx** multimedia SoC — H.264 + software-driven adaptive FHSS
- **AMICCOM A71xx** — 2.4 GHz GFSK RF PHY (⚠️ newer **A7157** adds hardware AES-128)
- **External SPI NOR flash** — confirmed **Winbond W25Q128 (16 MB)** on the MaxView parent (dump
  target)
- **LCD = ~40-pin parallel RGB888 (DPI)** — _not_ MIPI-DSI → tappable with a logic analyzer/FPGA
- _(V65 is an older Hisense lineage — none of the above confirmed for it.)_

## Recommended path — display-bus tap (bypass RF entirely)

The parent unit already follows the hops, demodulates, and decodes the codec into pixels for its
LCD. **Tap the decoded video off the parallel-RGB bus** on a _sacrificial_ parent unit: parallel-RGB
(pixel clock, HSYNC, VSYNC, DE, data) → logic analyzer / FPGA / Pi DPI pins → reconstruct frames →
encode (ffmpeg) → restream via **go2rtc / MediaMTX** → Home Assistant. This is mechanical +
logic-analyzer work (days–weeks), high success probability, no RF/codec RE.

## Step 0 (before buying anything)

Read the **model # / FCC ID** off the unit, then pull the **FCC test report** (fcc.report, grantee
`2AQVL`) — it hands you the hop parameters (channels/spacing/dwell/span) for free, and lets you
confirm the transceiver: **A7121** (plaintext era) vs **A7130/A7157** (possible AES-128).

## Exit Criteria

- [ ] Model # / FCC ID confirmed; FCC test report pulled; transceiver PN identified
- [ ] Decoded frames captured off the parent-unit parallel-RGB bus (proof of concept image)
- [ ] Continuous frame reconstruction → encoded stream
- [ ] Stream restreamed (go2rtc/MediaMTX) and visible as a camera in Home Assistant
- [ ] Documented; decide whether it's reliable enough to replace the head unit

## Shopping list (~$80)

- SOIC-8 test clip + CH341A programmer (~$15) — SPI flash dump (W25Q128-class)
- USB-TTL UART adapter (~$8) — boot-log/chip-ID recon (no shell expected)
- Cheap logic analyzer (Saleae clone) or ~$50 FPGA — the parallel-RGB capture
- A **second/sacrificial parent unit** for the destructive display tap

## Pragmatic fallback (the "cheating" win)

If the goal is just _a baby cam in the homelab_, skip all of the above: buy a **$25–40 LAN-only
ONVIF/RTSP cam** (Tapo C120 / Reolink), quarantine it on the IoT VLAN with **WAN egress blocked**,
and restream via go2rtc → HA. One hour, better image quality. (Keep a baby cam LAN-only — no cloud.)

## Cautions

- The best public teardown (noobie.dog, near-identical Victure hardware) reportedly carries an
  injected malicious script on its host page — read findings in reader mode, run nothing from it.
- Confirm the transceiver isn't an AES-128 A7157 before assuming a flash dump yields cleartext.

## Progress

- [x] Feasibility + silicon recon (2026-06-27) — display tap is the achievable path
- [ ] Step 0: model/FCC ID + test report
- [ ] Teardown + flash dump + UART recon
- [ ] Parallel-RGB capture POC
- [ ] Reconstruct → restream → HA
