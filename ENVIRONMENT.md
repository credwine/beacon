# Beacon -- Environment & Reproducibility Guide

## Runtime Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.10+ | Tested on 3.11.9 |
| Ollama | 0.20.0+ | Required for Gemma 4 support |
| OS | Windows 11, Linux, macOS | Cross-platform |
| RAM | 8 GB minimum | 16 GB recommended for smooth inference |
| GPU | Optional | NVIDIA GPU with 6+ GB VRAM improves speed; CPU inference works but slower |

## Quick Start (Inference Only)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install and start Ollama
# https://ollama.com/download

# Pull Gemma 4 model (one-time, ~9.6 GB download)
ollama pull gemma4:e4b

# Start Beacon
python run.py
```

## Fine-Tuning Requirements

Fine-tuning requires a CUDA-capable GPU. Tested on:

| Hardware | VRAM | Training Time |
|----------|------|---------------|
| NVIDIA RTX 4090 | 24 GB | ~5 minutes |
| NVIDIA T4 (Kaggle free) | 16 GB | ~10 minutes |
| NVIDIA A100 | 40 GB | ~2 minutes |

```bash
# Install training dependencies
pip install -r training/requirements.txt

# Run fine-tuning
python training/finetune.py

# Import fine-tuned model into Ollama
ollama create beacon-scam-detector -f training/Modelfile
```

## Docker Deployment

```bash
docker compose up
```

Starts both Beacon (port 8000) and Ollama (port 11434) with GPU passthrough.

## Python Dependencies (Runtime)

- fastapi 0.115.0
- uvicorn 0.30.6
- httpx 0.27.2
- pydantic 2.9.2
- python-multipart 0.0.12
- jinja2 3.1.4
- aiofiles 24.1.0

## Python Dependencies (Training)

- unsloth 2024.12+
- datasets 3.0.0+
- transformers 4.46.0+
- trl 0.12.0+
- torch 2.1.0+

## Model Variants

| Ollama Tag | Download | VRAM (Q4) | Active Params | HuggingFace ID |
|------------|----------|-----------|---------------|----------------|
| gemma4:e2b | 7.2 GB | 4 GB | 2.3B | google/gemma-4-E2B |
| gemma4:e4b | 9.6 GB | 6 GB | 4.5B | google/gemma-4-E4B |
| gemma4:26b | 18 GB | 18 GB | 3.8B (MoE) | google/gemma-4-26B-A4B |
| gemma4:31b | 20 GB | 20 GB | 30.7B | google/gemma-4-31B |

Default model: `gemma4:e4b` (configurable via `GEMMA_MODEL` environment variable).

## Tested Platforms

- Windows 11 Pro (NVIDIA RTX GPU)
- Ubuntu 22.04 (NVIDIA T4, Kaggle environment)
- Docker (NVIDIA Container Toolkit)
