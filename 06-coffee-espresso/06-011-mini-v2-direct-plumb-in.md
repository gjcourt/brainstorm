---
title: 'Mini Vivaldi II Direct Plumb-In via Reservoir Float-Fill'
number: '06-011'
category: 'coffee-espresso'
difficulty: 'Easy'
time_commitment: '1-2 days'
target_skills: 'Water Plumbing, Pressure Regulation, BSP Fittings'
status: 'Planned'
depends_on:
  - hardware/lucca-a53-mini
---

# Mini Vivaldi II Direct Plumb-In via Reservoir Float-Fill

## Description

Convert the **La Spaziale Mini Vivaldi II** (Clive's **LUCCA A53 Mini** rebadge — vibratory pump,
currently tank-fed) to a plumbed setup that's **robust** — meaning low-maintenance, reversible, and
respectful of the vibe pump's design constraints.

The s1cafe.com / home-barista.com community converged answer for vibe-pump Mini V2 plumb-in is
**reservoir float-fill, not inlet-side direct plumb**: the line keeps the existing tank topped up
via a mechanical float valve; the pump still gravity-feeds from the tank exactly as
factory-designed. This preserves pump life (5–10+ years vs 1–2 years on inlet plumb), keeps the
existing low-water float **switch** as dry-run protection, and is fully reversible without internal
modification.

**Out of scope (deliberately):**

- Drain plumbing for the drip tray — keep removable for now.
- Auto-shutoff solenoid — deferred to a future enhancement; the plan reserves a spot in the line
  where it would go.
- Pump replacement / rotary conversion — explicitly not desired.

## Approach: reservoir float-fill

```text
[Aquasana Claryum output, 1/4" braided]
        │
        ├─ 1/4" inline shut-off (ball valve) ── for service isolation
        │
        ├─ [future: NC solenoid here]         ── reserved spot, not installed yet
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
4. Reversible: disconnect at the regulator, refill manually, machine is back to stock.
5. Pressure-tolerant: even if the regulator fails high (60+ PSI), filling a tank doesn't hurt
   anything.

## Pre-flight: verify source-water hardness

The **Aquasana Claryum is a contaminant/taste filter (chlorine, chloramine, PFAS, lead, etc.) — it
does not soften water.** It does not remove calcium / magnesium hardness or significantly reduce
alkalinity. La Spaziale boilers don't auto-flush, so scale matters here.

**Do this before installing anything:**

1. Hardness test strip ($5 hardware store) or TDS meter.
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

All threads on the espresso side are **BSP, not NPT**. Single-use fiber washers on every joint that
gets disassembled.

| #   | Item                                       | Spec                                                                | Notes                                                                                                |
| --- | ------------------------------------------ | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1   | 1/4" inline shut-off ball valve            | Full-port, push-to-connect or compression                           | Local cutoff for service. Don't rely on the house valve.                                             |
| 2   | (Reserved) NC solenoid                     | 24VAC or line-voltage, 1/4", normally-closed                        | **Not installed in this phase.** Reserved gap in the regulation stack.                               |
| 3   | Pressure regulator                         | 1/4" inlet/outlet, gauge'd, set to ~25 PSI                          | Watts U5B-LF (3/8") with 1/4" step adapters works; or a smaller in-line 1/4" regulator if available. |
| 4   | Reservoir float valve                      | 1/4" male thread inlet (RO-style brass), with quarter-turn shut-off | Mounts through a hole drilled in the **tank lid**. Set to close ~1/2" below max-fill mark.           |
| 5   | 1/4" LLDPE polyethylene tubing             | Length: filter output → machine + ~12" service loop                 | Espresso aftermarket standard. Routes easier than braided; takes John Guest fittings cleanly.        |
| 6   | Push-to-connect fittings (John Guest 1/4") | Tees, elbows, straight unions as needed                             | Push-to-connect at any joint that may need disassembly for service.                                  |
| 7   | Fiber washers                              | 1/4" BSP sized                                                      | One per joint; replace on every disassembly.                                                         |
| 8   | Hardness test strip / TDS meter            | One-time use                                                        | Pre-flight check. ~$5–25.                                                                            |

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
2. **Empty space reserved for future solenoid** — leave ~3" of straight line.
3. **Pressure regulator** — bench-set to ~25 PSI **before** mounting.
4. **1/4" line** continuing to the machine.

Mount the regulator stack against the cabinet wall — don't let it hang from the line.

### 4. Modify the reservoir for the float valve

- Pull Mini V2 reservoir out.
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

- Open inline shut-off slowly, watch every joint.
- Float valve fills to set level and **closes cleanly** (no oscillation / hammering).
- If hammering: drop regulator setpoint in 5 PSI increments until quiet.
- Drain the tank manually to confirm the existing low-water switch still trips.

### 7. Wet test

- Boilers to temperature. Pull a single shot. Tank refills as level drops; no hammer.
- 30s blank flush. Tank refills concurrently without overfilling.
- 5–10 consecutive shots over 15 minutes. Steady operation.

### 8. Burn-in (24h)

- Leave on the line under static pressure for 24h (machine off OK — line still pressurized).
- Inspect every joint for weep / drip.
- Re-tighten any wet joint; re-test.

## Reserved future enhancements

- **Solenoid auto-shutoff**: splice into the reserved gap in the regulation stack. NC solenoid wired
  to machine power so the line is depressurized whenever the machine is off. Insurance against a 3
  a.m. float-valve failure flooding the kitchen. ~$30–60 in parts.
- **Drain plumb**: drill the drip tray for a hose barb, run silicone hose to a drain on continuous
  downhill slope. Independent workstream.
- **Softening upgrade**: if hardness creeps up (annual re-test), add Pentair Claris or BWT Bestmax
  cartridge upstream of regulator stack, downstream of Claryum.

## Exit Criteria

- [ ] Pre-install: hardness ≤60 ppm, alkalinity 40–80 ppm, chloride <30 ppm at Claryum output.
      Numbers recorded.
- [ ] Inline shut-off closes cleanly with full water-flow stop downstream.
- [ ] Regulator gauge reads 20–25 PSI under static line pressure.
- [ ] Float valve fills to set level and closes without hammering.
- [ ] Existing low-water switch trips when tank is manually drained.
- [ ] No leaks at any joint after 24 hours of static line pressure.
- [ ] 5+ consecutive shots pulled with steady tank refill.

## Progress

- [x] Researched s1cafe.com / home-barista.com community approaches
- [x] Decided: reservoir float-fill (not inlet plumb) for vibe-pump robustness
- [x] BoM scoped against existing Aquasana Claryum infrastructure
- [ ] Buy parts
- [ ] Test water hardness at Claryum output
- [ ] Build regulation stack
- [ ] Modify reservoir lid; mount float valve
- [ ] Wet test
- [ ] 24h burn-in observation
- [ ] Document as-built (regulator setpoint, line route, water test numbers)

## Sources

- [LUCCA A53 Mini / Mini Vivaldi — Clive Coffee Help Center](https://support.clivecoffee.com/en/lucca-a53-mini-mini-vivaldi)
- [LUCCA A53 Mini Vibratory Pump Replacement (pump access reference)](https://support.clivecoffee.com/en/la-spaziale-lucca-a53-mini-mini-vivaldi-vibratory-pump-replacement)
- [LUCCA A53 manual (PDF)](https://ep-shopify.s3.amazonaws.com/related-documents/lucca/lucca-a53-manual.pdf)
- [Vivaldi II / Lucca A53 plumb thread — s1cafe.com](https://www.s1cafe.com/viewtopic.php?t=2231)
- [Tank-version Vivaldi plumb conversion — s1cafe.com](https://www.s1cafe.com/viewtopic.php?t=2376)
- [How to plumb the La Spaziale S1 Vivaldi II — home-barista.com](https://www.home-barista.com/espresso-machines/how-to-plumb-la-spaziale-s1-vivaldi-ii-t5386.html)
- [Aquasana Claryum Direct Connect — contaminant reduction spec](https://www.aquasana.com/water-filtration-systems/under-counter-water-filters/claryum-direct-connect-water-filter-system)
