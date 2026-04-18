# Brainstorm Agent Guidelines

## Repository Overview

Brainstorm is a curated collection of 100 multidisciplinary engineering and skill-building project ideas, organized by category. Projects span software, hardware, woodworking, finance, and music — calibrated for someone with strong existing software skills (Go, Kubernetes, Docker).

## Repository Structure

```
01-audio-midi/         ← audio, MIDI, DSP project ideas
02-woodworking/        ← woodworking and fabrication projects
03-homelab-automation/ ← home lab and automation projects
04-finance-analysis/   ← financial modeling and analysis projects
05-piano/              ← piano and music theory projects
06-coffee-espresso/    ← espresso and coffee projects
07-cross-disciplinary/ ← projects combining multiple domains
README.md              ← overview and difficulty scale
update_prefixes.py     ← script to renumber/reorder project prefixes
Makefile               ← convenience targets
```

## Difficulty Scale

- **Easy (1–2 days)**: Leverages existing skills (Go, basic K8s, simple ESPHome/HA, basic woodworking).
- **Medium (1–4 weeks)**: Combines multiple disciplines; introduces new concepts.
- **Hard (months)**: Ambitious; stretches into low-level domains (C/C++, RTOS, DSP, advanced finance/music theory).

## Working With This Repo

- Each category directory contains markdown files describing individual projects.
- To add a new project: create a markdown file in the appropriate category directory following the existing format.
- To renumber project prefixes after reordering: `python update_prefixes.py`
- Use the `Makefile` for any automation tasks defined there.

## Notes

- This is a personal ideas/planning repo — no CI or tests.
- Cross-disciplinary projects (`07-cross-disciplinary/`) intentionally combine concepts from multiple categories.
