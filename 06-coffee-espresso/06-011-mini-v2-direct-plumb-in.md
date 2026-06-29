---
title: 'Mini Vivaldi II Direct Plumb-In via Reservoir Float-Fill'
number: '06-011'
category: 'coffee-espresso'
difficulty: 'Easy'
time_commitment: '1-2 days'
target_skills: 'Water Plumbing, Pressure Regulation, BSP Fittings'
status: 'Not Started'
depends_on:
  - hardware/lucca-a53
---

# Mini Vivaldi II Direct Plumb-In via Reservoir Float-Fill

## Description

Convert the **La Spaziale Mini Vivaldi II** (Clive's **LUCCA A53 Mini** rebadge — vibratory pump,
currently tank-fed) to a plumbed setup that's **robust** — meaning low-maintenance, reversible, and
respectful of the vibe pump's design constraints.

The s1cafe.com / home-barista.com community converged answer for vibe-pump Mini V2 plumb-in is
**reservoir float-fill, not inlet-side direct plumb**: the line keeps the existing tank topped up
via a mechanical float valve; the pump still gravity-feeds from the tank exactly as
factory-designed. Community reports suggest this preserves pump life substantially (multi-year vs.
~1-2 years on inlet plumb where the vibe pump fights inlet pressure on every stroke), keeps the
existing low-water float **switch** as dry-run protection, and is fully reversible without internal
modification.

**Out of scope (deliberately):**

- Drain plumbing for the drip tray — keep removable for now.
- Pump replacement / rotary conversion — explicitly not desired.

## Approach: reservoir float-fill

```text
[Aquasana Claryum output, 1/4" braided]
        │
        ├─ 1/4" inline shut-off (ball valve) ── for service isolation
        │
        ├─ 1/4" NC brass solenoid valve       ── energized only when machine is on; fail-closed
        │
        ├─ 1/4" pressure regulator @ ~20–25 PSI
        │
        └─ 1/4" line ─→ float valve in Mini V2 reservoir
                          │
                          └─ closes when tank reaches set level
                             → vibe pump still gravity-feeds as stock
                             → existing low-water switch unchanged
```

The Mini V2's existing **low-water float switch** (the magnetic switch that disables the pump when
the tank is dry) is **untouched** by this work and continues to provide dry-run protection. The new
mechanical **float valve** controls fill, not pump enable.

## Why this is "robust"

1. Vibe pump operates at atmospheric inlet pressure as factory-designed. No backpressure → no
   accelerated diaphragm / check-valve wear.
2. Original dry-run protection (low-water switch) remains in place.
3. Failure modes are bounded:
   - Stuck-open float valve → tank overfills → drip tray catches the overflow.
   - Stuck-closed float valve → tank slowly drains → original low-water switch trips → exact same
     failure mode as today.
   - Hose burst / fitting failure → only possible while machine is on (NC solenoid closes the line
     whenever machine is off); unattended flood risk is eliminated.
4. Reversible: disconnect at the regulator, refill manually, machine is back to stock.
5. Pressure-tolerant: even if the regulator fails high, the tank can't be over-pressurized (it's
   vented). Worst case is float-valve hammering / chatter and accelerated float-seat wear, which is
   loud and obvious — not a silent flood.
6. Fail-safe on power loss: NC solenoid de-energizes closed, so a house power outage shuts off the
   water supply automatically.

## Pre-flight: verify source-water hardness

The **Aquasana Claryum is a contaminant/taste filter (chlorine, chloramine, PFAS, lead, etc.) — it
does not soften water.** It does not remove calcium / magnesium hardness or significantly reduce
alkalinity. La Spaziale boilers don't auto-flush, so scale matters here.

**Do this before installing anything:**

1. API GH/KH titration kit (~$8) — reads hardness + alkalinity directly. (A TDS meter is only a
   rough proxy; the Claryum doesn't reduce TDS, so its reading ≈ tap.)
2. Test from the **Claryum output**, not the upstream tap.
3. Three numbers to check:

| Metric                    | Espresso-safe target | Action if exceeded                                                                                                             |
| ------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Total hardness (as CaCO₃) | ≤ 60 ppm             | If 60–120: proceed, plan annual descale. If >120: add a softening cartridge (Pentair Claris, BWT Bestmax) **before** plumb-in. |
| Total alkalinity (KH)     | 40–80 ppm            | High alkalinity = fast scale. Same softening cartridge addresses this.                                                         |
| Chloride                  | < 30 ppm             | Claryum reduces chlorine but not chloride salts. High chloride pits boilers. RO is the only reliable answer here.              |

If targets met → Claryum is sufficient and plan proceeds as written. If not → add softening stage to
BoM before going further.

## Bill of materials

Thread-standard note: this plan does **not** plumb into the boiler — all joints live on the supply
line between the Aquasana output and the reservoir float valve. Most espresso-aftermarket regulators
and RO-style float valves use **G-thread BSP-parallel** ports (sealed with a fiber/nylon washer
against a flat face), not tapered NPT. **Don't mix:** an NPT male into a BSPP female will start
threading and then leak under pressure. Verify each part's thread standard from its spec sheet
before buying, and replace fiber washers on every disassembly. **Simplest path:** stay all John
Guest push-fit end-to-end (both the regulator and the float valve come in 1/4" JG) — that eliminates
threaded joints and largely moots this whole note.

| #   | Item                                         | Spec                                                                                                                  | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | 1/4" inline shut-off ball valve              | Full-port, push-to-connect or compression                                                                             | [John Guest PPSV040808W](https://www.amazon.com/Speedfit-Connect-Plastic-Plumbing-PPSV040808W/dp/B003YKF2E2) (~$8). Local cutoff for service. Don't rely on the house valve.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 2   | NC brass solenoid valve                      | 1/4", normally-closed, brass body, Viton (FKM) seals, direct-acting (0 psi min), 24 V DC coil (preferred) or 110 V AC | Pick: [U.S. Solid 1/4" 24 V DC brass NC, Viton](https://ussolid.com/products/u-s-solid-electric-solenoid-valve-1-4-24v-dc-solenoid-valve-brass-body-normally-closed-viton-seal-html) (~$16); [110 V AC version](https://ussolid.com/products/u-s-solid-electric-solenoid-valve-1-4-110v-ac-230psi-solenoid-valve-brass-body-normally-closed-viton-seal-html) (~$33) avoids the wall-wart but means wiring mains. Seals are Viton, not NSF-61 potable-certified — fine for a cold feed. Avoid plastic-body solenoids. Energized only when machine is on; NC = fail-closed on power loss.                                                                      |
| 2a  | Smart plug (machine-side)                    | 15A indoor smart plug (Kasa / TP-Link / equivalent)                                                                   | [Kasa EP25](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-plug-slim-energy-monitoring-ep25) (~$13/ea in a 4-pack) or any 15 A plug. Single switched outlet feeds both the machine (~1400 W) and the coil-supply wall-wart — don't daisy-chain other loads. Machine "on" ⇒ solenoid open; "off" or power loss ⇒ solenoid closed.                                                                                                                                                                                                                                                                                                               |
| 2b  | Solenoid coil supply                         | If 24 V DC solenoid: 24 V DC wall-wart, ≥1 A; if 110 V AC solenoid: none needed (coil runs direct from smart plug)    | Mount the wall-wart and any coil wiring in a small junction box near the under-counter outlet. Don't free-air splice AC mains.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 3   | Pressure regulator                           | 1/4", set to ~20–25 PSI; stay JG push-fit to avoid thread transitions                                                 | Float-fill is low-demand — don't overspend. Value: [JG Micro Pressure Regulator](https://www.wb.coffee/shop/john-guest-micro-pressure-regulator-valve-1-8-1-4-43588) (~$29; 0–4 bar adjustable, JG push-fit, **no gauge**). Turnkey: [Chris' Coffee regulator w/ gauge](https://www.chriscoffee.com/products/pressure-regulator-valve) (~$100, JG 1/4"). Both JG-native → no thread transition. Skip the [Espresso Parts "Flojet → John Guest kit"](https://www.espressoparts.com/products/flojet-water-pressure-regulator-to-john-guest-kit) — same non-adjustable 1750-series pump regulator (3/8" JG, vendor-rated "temporary use" on espresso machines). |
| 4   | Reservoir float valve                        | Plastic RO float valve with a threaded mounting shank + 1/4" inlet                                                    | [Example: LiquaGen RO float valve](https://www.amazon.com/LiquaGen-Reverse-Osmosis-Filtration-Systems/dp/B07DGX3NGB) (~$10). Brass/quarter-turn unnecessary — service shut-off is line 1. Mounts through a hole drilled in the **tank lid**; close ~1/2" below max-fill. **Test-fit before drilling** (see install §4).                                                                                                                                                                                                                                                                                                                                      |
| 5   | 1/4" LLDPE polyethylene tubing               | Length: filter output → machine + ~12" service loop                                                                   | Espresso aftermarket standard. Routes easier than braided; takes John Guest fittings cleanly.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 6   | Push-to-connect fittings (John Guest 1/4")   | Tees, elbows, straight unions as needed                                                                               | Push-to-connect at any joint that may need disassembly for service.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 7   | Fiber washers                                | 1/4" BSPP sized (parallel-thread, flat-face seal)                                                                     | Only if a chosen part lands on a BSPP thread. Going all-JG push-fit (regulator + float valve) likely means **zero** threaded joints — buy as needed, replace on disassembly.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 8   | Water test: GH/KH kit (+ optional TDS meter) | One-time use                                                                                                          | [API GH & KH titration kit](https://www.amazon.com/API-TEST-Freshwater-Aquarium-Water/dp/B003SNCHMA) (~$8) measures hardness + alkalinity — the numbers that matter. Claryum doesn't reduce TDS, so a TDS meter (~$15) is only a rough proxy. Pre-flight check.                                                                                                                                                                                                                                                                                                                                                                                              |

### Orderable picks (concrete products)

Every line item in the BoM table above links to a concrete product. Shopping summary for the **value
path** (all John Guest push-fit, 24 V DC solenoid):

| Part                  | Pick                                                   | ~Price |
| --------------------- | ------------------------------------------------------ | ------ |
| Shut-off ball valve   | John Guest PPSV040808W (1/4" push-fit)                 | $8     |
| NC solenoid (24 V DC) | U.S. Solid 1/4" 24 V DC brass NC, Viton                | $16    |
| Smart plug            | Kasa EP25 (4-pack, ~$13 ea)                            | $13    |
| 24 V DC wall-wart     | >=1 A DC supply for the coil                           | $10    |
| Pressure regulator    | JG Micro Pressure Regulator (0-4 bar, no gauge)        | $29    |
| Float valve           | Plastic RO float valve, threaded shank (e.g. LiquaGen) | $10    |
| 1/4" LLDPE tubing     | 25 ft roll                                             | $10    |
| JG push-fit fittings  | tees / elbows / unions + spare collets                 | $15    |
| BSPP fiber washers    | only if a part is BSPP-threaded -- likely none needed  | 0-6    |
| Water test            | API GH/KH titration kit (TDS meter optional)           | $8     |

**Value-path total ~= $120.** Swapping in the gauge'd Chris' Coffee regulator (~$100) pushes it to
~$190. Excludes the reused Claryum filter / cold-water branch.

**Existing infrastructure being reused (no purchase):** dedicated cold-water branch to kitchen,
Aquasana Claryum Direct Connect filter, 1/4" braided output line from filter.

## Installation steps

### 1. Pre-flight (do not skip)

- Run hardness/alkalinity test on Claryum output. Record numbers.
- If outside targets → stop, add softening cartridge to BoM, then resume.

### 2. Plan the route

- Measure from existing 1/4" braided output to where the Mini V2 will sit.
- Service loop (~12" slack) near the machine so it can be pulled forward without disconnecting.
- Avoid 90° kinks in LLDPE — use elbow fittings or wide sweeps.

### 3. Build the regulation stack

In order, downstream of the existing Aquasana output:

1. **Inline shut-off** (close it now while building the rest).
2. **NC solenoid valve** — installed upstream of the regulator and the long run to the reservoir, so
   a downstream hose burst still triggers shut-off when the machine cycles off. Flow arrow on the
   valve body points downstream. Verify thread standard (NPT vs. BSPP) matches the adjacent
   fittings; transition with a brass adapter + PTFE tape (NPT) or fiber washer (BSPP) as needed.
3. **Pressure regulator** — bench-set to ~25 PSI **before** mounting.
4. **1/4" line** continuing to the machine.

Mount the regulator stack against the cabinet wall — don't let it hang from the line. Mount the
solenoid coil-up so any seal weep drips clear of the coil and electrical connection.

**Solenoid wiring** (recommended: smart-plug path):

- Single switched outlet (smart plug) feeds both the machine's power cord and the solenoid coil
  supply.
- If the solenoid is **110 V AC**: wire the coil leads into a small junction box fed from the
  switched outlet. No transformer. Use a proper strain relief and grounded box — this is mains.
- If the solenoid is **24 V DC**: plug a 24 V DC wall-wart into the switched outlet, then run the
  low-voltage leads to the coil. Easier and lower-risk; preferred unless there's a reason not to.
- Result: machine "on" ⇒ solenoid energized ⇒ valve open. Machine "off" or power loss ⇒ solenoid
  de-energized ⇒ valve closed.

### 4. Modify the reservoir for the float valve

- Pull Mini V2 reservoir out.
- **Test-fit before drilling.** Set the float valve roughly in place and confirm the float arm has
  full travel without fouling the tank walls or the existing low-water magnet, and that it can close
  ~1/2" below max-fill. RO float valves are sized for larger tanks — verify it suits this small
  reservoir before committing to a hole.
- Drill a hole in the **lid** (not the wall) for the float-valve thread. Step bit + lubricant; lid
  is plastic, easy.
- Mount the float valve through the lid; tighten with supplied gasket/washer.
- Verify the float arm swings freely without contacting walls or the bottom magnet of the existing
  low-water switch.
- Set float position to close ~1/2" below the existing max-fill line.

### 5. Connect line to float valve

- Route 1/4" LLDPE from regulator output to reservoir.
- Push-to-connect (John Guest) at the float-valve end so the tank can be lifted out for cleaning
  without breaking the joint.
- Re-seat the reservoir.

### 6. Pressurize and verify

- Smart plug **on** (solenoid energized, valve open). Open inline shut-off slowly, watch every
  joint.
- Float valve fills to set level and **closes cleanly** (no oscillation / hammering).
- If hammering: drop regulator setpoint in 5 PSI increments until quiet.
- Drain the tank manually to confirm the existing low-water switch still trips.
- **Solenoid functional check**: with the inline shut-off open, smart plug **off** — confirm no flow
  downstream of the solenoid (watch the float valve; tank should not refill as you draw it down).
  Then smart plug **on** — confirm flow resumes within ~1 second.

### 7. Wet test

- Boilers to temperature. Pull a single shot. Tank refills as level drops; no hammer.
- 30s blank flush. Tank refills concurrently without overfilling.
- 5–10 consecutive shots over 15 minutes. Steady operation.

### 8. Burn-in (24h)

- Leave on the line under static pressure for 24h (machine off OK — line still pressurized).
- Inspect every joint for weep / drip.
- Re-tighten any wet joint; re-test.

## Reserved future enhancements

- **Drain plumb**: drill the drip tray for a hose barb, run silicone hose to a drain on continuous
  downhill slope. Independent workstream.
- **Softening upgrade**: if hardness creeps up (annual re-test), add Pentair Claris or BWT Bestmax
  cartridge upstream of regulator stack, downstream of Claryum.
- **Home Assistant integration of the smart plug**: schedule, away-mode auto-off, leak-sensor
  triggered shutoff. The plug from Phase 1 is already HA-compatible; this is a software-only
  follow-up.

## Exit Criteria

- [ ] Pre-install: hardness ≤60 ppm, alkalinity 40–80 ppm, chloride <30 ppm at Claryum output.
      Numbers recorded.
- [ ] Inline shut-off closes cleanly with full water-flow stop downstream.
- [ ] Regulator gauge reads 20–25 PSI under static line pressure.
- [ ] Float valve fills to set level and closes without hammering.
- [ ] Solenoid: smart-plug off ⇒ no downstream flow; smart-plug on ⇒ flow within ~1 s. Pulling the
      wall outlet (simulated power loss) also closes the valve.
- [ ] Existing low-water switch trips when tank is manually drained.
- [ ] No leaks at any joint after 24 hours of static line pressure.
- [ ] 5+ consecutive shots pulled with steady tank refill.

## Progress

- [x] Researched s1cafe.com / home-barista.com community approaches
- [x] Decided: reservoir float-fill (not inlet plumb) for vibe-pump robustness
- [x] BoM scoped against existing Aquasana Claryum infrastructure
- [ ] Buy parts (incl. NC brass solenoid + smart plug + coil supply)
- [ ] Test water hardness at Claryum output
- [ ] Build regulation stack (shut-off → solenoid → regulator)
- [ ] Wire solenoid via smart plug; bench-test open/close before plumbing
- [ ] Modify reservoir lid; mount float valve
- [ ] Wet test
- [ ] Solenoid power-cycle + power-loss shutoff verified
- [ ] 24h burn-in observation
- [ ] Document as-built (regulator setpoint, line route, water test numbers, solenoid model/coil V)

## Sources

- [LUCCA A53 Mini / Mini Vivaldi — Clive Coffee Help Center](https://support.clivecoffee.com/en/lucca-a53-mini-mini-vivaldi)
- [LUCCA A53 Mini Vibratory Pump Replacement (pump access reference)](https://support.clivecoffee.com/en/la-spaziale-lucca-a53-mini-mini-vivaldi-vibratory-pump-replacement)
- [LUCCA A53 manual (PDF)](https://ep-shopify.s3.amazonaws.com/related-documents/lucca/lucca-a53-manual.pdf)
- [Vivaldi II / Lucca A53 plumb thread — s1cafe.com](https://www.s1cafe.com/viewtopic.php?t=2231)
- [Tank-version Vivaldi plumb conversion — s1cafe.com](https://www.s1cafe.com/viewtopic.php?t=2376)
- [How to plumb the La Spaziale S1 Vivaldi II — home-barista.com](https://www.home-barista.com/espresso-machines/how-to-plumb-la-spaziale-s1-vivaldi-ii-t5386.html)
- [Aquasana Claryum Direct Connect — contaminant reduction spec](https://www.aquasana.com/under-sink-water-filters/claryum-direct-connect-100329886.html)
