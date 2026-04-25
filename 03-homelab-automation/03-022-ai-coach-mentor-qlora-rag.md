---
title: 'AI Coach & Mentor — QLoRA Fine-Tuned Qwen3-32B with RAG Book Corpus'
number: '03-022'
category: 'homelab-automation'
difficulty: 'Hard'
time_commitment: 'Months'
target_skills: 'QLoRA Fine-Tuning, RAG Pipeline, Vector Embeddings, DPO Alignment, Qdrant, BGE-M3, Axolotl'
status: 'Not Started'
---

# AI Coach & Mentor — QLoRA Fine-Tuned Qwen3-32B with RAG Book Corpus

## Description

A personal coach and mentor AI trained on a curated library of books spanning
productivity, mindset, professional development, and domain-specific subjects.
The system uses a hybrid approach: fine-tuning teaches the reasoning patterns
and communication style of great coaches/authors; RAG retrieves accurate
passages and citations at inference time.

Sibling project of 03-021 (personal assistant) and 03-023 (homelab agent).
Runs as a separate LoRA adapter on the shared Qwen3-32B base.

---

## Why Hybrid (Fine-Tune + RAG), Not Fine-Tune Alone

Fine-tuning on books alone risks hallucinating specific quotes and passages.
RAG retrieves accurately. Fine-tuning gives the model the reasoning patterns
and coaching tone of the source material.

```
Fine-tune → coaching style, reasoning depth, communication tone
RAG       → accurate quotes, specific frameworks, chapter references
```

---

## Model Architecture

**Shared base:** Qwen3-32B (4-bit QLoRA) — same base as 03-021 and 03-023
**This adapter:** coach-mentor LoRA weights
**Embedding model:** BGE-M3 (fine-tuned on your corpus) — GPU 1
**Vector store:** Qdrant (or pgvector via existing CNPG cluster)
**Context window:** 128K tokens (Qwen3-32B) — can load large book chunks

---

## Book Corpus

Curate a library of books across relevant domains. Examples:

Productivity / Systems:
- Atomic Habits (Clear), Deep Work (Newport), Getting Things Done (Allen)
- The One Thing (Keller), Essentialism (McKeown)

Mindset / Performance:
- Mindset (Dweck), The Inner Game of Tennis (Gallwey), Flow (Csikszentmihalyi)
- Can't Hurt Me (Goggins), Extreme Ownership (Willink)

Professional / Leadership:
- High Output Management (Grove), The Hard Thing About Hard Things (Horowitz)
- Good to Great (Collins), Turn the Ship Around (Marquet)

Add domain-specific books relevant to your professional focus.

Storage: 32TB NVMe — embed entire corpus, no size concerns.

---

## Training Data

Phase 1 — Continued pre-training on book corpus:
- Raw book text chunked into training examples
- Teaches writing style, reasoning patterns, vocabulary of source material

Phase 2 — Supervised fine-tune:
- Q&A pairs derived from book content
- Coaching dialogue examples (question → thoughtful response with frameworks)
- ~10,000–20,000 examples

Phase 3 — DPO alignment:
- Rank responses: prefer those that cite sources, ask clarifying questions,
  challenge assumptions vs. give surface-level answers

---

## RAG Pipeline

```
User query → BGE-M3 embed → Qdrant similarity search → top-k passages → LLM context → response
```

Embedding model: BGE-M3 (fine-tuned on your corpus for better domain precision)
Chunk strategy: 512-token overlapping chunks with book/chapter metadata
Re-ranking: BGE reranker or E5-Mistral-7B for precision

---

## Training Stack

| Tool | Purpose |
|---|---|
| Axolotl | QLoRA training orchestrator |
| UnSloth | Training speedup |
| DeepSpeed ZeRO-2 | Multi-GPU |
| LlamaIndex / LangChain | RAG pipeline construction |
| Qdrant | Vector store |

Estimated training time on 2x 4090s: 8–16 hours per iteration

---

## Exit Criteria

- [ ] Full book corpus ingested, chunked, and embedded in Qdrant
- [ ] BGE-M3 fine-tuned on corpus
- [ ] RAG pipeline returning accurate passage retrieval with citations
- [ ] Coach/mentor LoRA trained and loaded in vLLM
- [ ] DPO alignment pass complete
- [ ] Mentor can answer questions with specific book/framework references
- [ ] Voice interface (via 03-021 voice pipeline)

## Progress

- [ ] Hardware operational
- [ ] Book corpus curated and digitized
- [ ] Embedding pipeline built
- [ ] Vector store populated
- [ ] Training data generated from corpus
- [ ] First LoRA training run
- [ ] DPO pass
- [ ] RAG integration
- [ ] End-to-end test with voice
- [ ] Documentation
