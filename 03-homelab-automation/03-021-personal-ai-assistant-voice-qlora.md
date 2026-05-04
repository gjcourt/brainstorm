---
title: 'Personal AI Assistant with Voice — QLoRA Fine-Tuned Qwen3-32B'
number: '03-021'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Months'
target_skills:
  'QLoRA Fine-Tuning, STT/TTS Pipeline, vLLM Serving, LoRA Adapter Hot-Swap, Python, Axolotl,
  UnSloth'
status: 'Not Started'
---

# Personal AI Assistant with Voice — QLoRA Fine-Tuned Qwen3-32B

## Description

Build a fully local, voice-enabled personal AI assistant — a Jarvis-style system running on
dedicated GPU hardware. The assistant is a QLoRA fine-tuned adapter on top of a shared Qwen3-32B
base model, trained on personal data to match your communication style, preferences, knowledge, and
context.

Voice interaction is symmetric: wake word → STT → LLM → streaming TTS, running entirely on local
hardware with sub-1s perceived latency.

This is one of three sibling projects sharing the same base model and hardware:

- **03-021** (this project): Personal assistant adapter
- **03-022**: Coach/mentor adapter
- **03-023**: Homelab autonomous agent adapter

---

## Hardware

| Component | Spec                                                     |
| --------- | -------------------------------------------------------- |
| GPUs      | 2x RTX 4090 (48GB VRAM total)                            |
| RAM       | 196GB DDR5                                               |
| Storage   | 32TB 710T NVMe                                           |
| Network   | 2x QSFP NIC                                              |
| OS        | Bare metal (not Kubernetes — GPU passthrough complexity) |

GPU assignment:

- GPU 0: vLLM serving Qwen3-32B base + active LoRA adapter
- GPU 1: Voice pipeline (Whisper + Kokoro) + BGE-M3 embeddings

---

## Model Architecture

**Shared base:** Qwen3-32B (4-bit QLoRA, ~20GB VRAM) **This adapter:** personal-assistant LoRA
weights **Serving:** vLLM with LoRA hot-swap — all three adapters served from one running instance

Why one base + three adapters vs three separate models:

- Base loaded once, adapters swap in milliseconds
- No cross-contamination between personas
- Retrain individual adapters without touching the base
- Leaves GPU 1 free for voice pipeline

---

## Voice Pipeline

```text
Mic → OpenWakeWord → faster-whisper (large-v3-turbo) → LLM (active LoRA) → streaming tokens → Kokoro-82M TTS → speakers
```

| Component              | Model/Tool                    | Notes                            |
| ---------------------- | ----------------------------- | -------------------------------- |
| Wake word              | OpenWakeWord                  | Always-on, CPU only              |
| STT                    | faster-whisper large-v3-turbo | RTF ~0.3x, GPU 1                 |
| TTS                    | Kokoro-82M                    | Real-time on CPU, natural output |
| Voice clone (optional) | F5-TTS                        | Train on ~10min of your voice    |
| Streaming              | Sentence boundary → TTS queue | Sub-1s perceived latency         |

---

## Training Data

- Personal conversation history and preferences
- Communication style examples (emails, notes, messages)
- Obsidian vault / personal notes
- Calendar and task context
- Homelab knowledge base (for general context — deep homelab capability is 03-023)

Target dataset size: 1,000–5,000 high-quality examples (quality >> quantity)

Fine-tuning method:

1. QLoRA supervised fine-tune (style, preferences, context)
2. DPO pass (rank responses to match preferred communication style)

---

## Training Stack

| Tool             | Purpose                             |
| ---------------- | ----------------------------------- |
| Axolotl          | Training orchestrator, QLoRA config |
| UnSloth          | 2-5x training speedup, lower VRAM   |
| DeepSpeed ZeRO-2 | Multi-GPU optimizer state sharding  |

Estimated training time on 2x 4090s: 2–4 hours per iteration

---

## Exit Criteria

- [ ] vLLM serving Qwen3-32B base on GPU 0 with LoRA hot-swap
- [ ] Voice pipeline end-to-end: wake word → STT → LLM → TTS
- [ ] Personal assistant LoRA trained and loaded
- [ ] Sub-1s perceived response latency (streaming TTS)
- [ ] Optional: F5-TTS voice clone trained on George's voice
- [ ] Persistent conversation context across sessions

## Progress

- [ ] Hardware operational (NAS/workstation build)
- [ ] vLLM + Qwen3-32B baseline serving
- [ ] Voice pipeline standalone test
- [ ] Training data curation
- [ ] First LoRA training run
- [ ] DPO alignment pass
- [ ] Integration and end-to-end test
- [ ] Documentation
