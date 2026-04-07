# Beacon

**Privacy-First AI Protection for Vulnerable Communities**

Beacon uses Google's Gemma 4 running entirely on your device to detect scams, explain contracts in plain English, and help you know your rights. No data ever leaves your computer.

---

## The Problem

Americans reported losing over **$10 billion to fraud** in 2023 (FTC) -- and only 5% of fraud gets reported. Seniors lose an average of **$33,915 per scam incident** (FBI IC3). The only mainstream AI scam checker -- Norton Genie -- was shut down in 2024, leaving a gaping void.

Existing solutions require cloud processing (your sensitive documents leave your device), paid subscriptions (the people who need it most can't afford it), or technical expertise (the people who need it most don't have it). Scammers have adopted AI. Their victims haven't been given AI to fight back.

## The Solution

Beacon is a free, open-source AI tool that runs **100% locally** on your computer. It uses **Gemma 4** via **Ollama** for private, offline-capable analysis:

### Scam Scanner
Paste any suspicious email, text, or letter. Beacon analyzes it instantly and tells you:
- **Trust Score** (0-100) with color-coded risk level
- **Scam type** classification (phishing, advance fee, impersonation, etc.)
- **Red flags** identified in the message
- **Plain-language explanation** anyone can understand
- **Recommended actions** and safe alternatives

### Contract Reader
Upload any contract, lease, or legal document. Beacon:
- Translates legalese into **plain English**
- Flags **predatory clauses** and hidden fees
- Compares terms to **fair market standards**
- Suggests **questions to ask** before signing

### Rights Navigator
Describe your situation and get:
- **Applicable legal rights** with citations
- **Step-by-step action plans**
- **Free legal aid resources** and hotlines
- **Important deadlines** you shouldn't miss

## Privacy Guarantee

- **No cloud, ever.** All AI processing happens on your device via Ollama.
- **No account required.** No sign-up, no login, no tracking.
- **No data collection.** Nothing is stored, logged, or transmitted.
- **Fully open source.** Every line of code is auditable.
- **Works offline.** Once set up, no internet connection needed.

## Quick Start

### Prerequisites
- [Python 3.10+](https://python.org)
- [Ollama](https://ollama.com/download)

### Install

```bash
# 1. Clone the repo
git clone https://github.com/forgeDev-studio/beacon.git
cd beacon

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull Gemma 4 (one-time, ~3GB download)
ollama pull gemma4:e4b

# 4. Start Beacon
python run.py
```

Open http://localhost:8000 in your browser.

### Docker (Alternative)

```bash
docker compose up
```

This starts both Beacon and Ollama with GPU support.

## Architecture

```
Browser (HTML/JS)  -->  FastAPI Backend  -->  Ollama (Gemma 4)
                         |                      |
                    Structured JSON         Local inference
                    responses with          (no data leaves
                    function calling        your device)
```

**Technical highlights:**
- **Gemma 4 function calling** for structured scam analysis output
- **FastAPI** async backend for responsive UI
- **Ollama** for local model serving with GPU acceleration
- **Zero-dependency frontend** -- vanilla HTML/CSS/JS, no build step
- **Docker Compose** for one-command deployment

## Fine-Tuned Model (Unsloth)

We fine-tuned Gemma 4 E4B specifically for scam detection using [Unsloth](https://github.com/unslothai/unsloth), creating a specialized model that's faster and more accurate at identifying fraud patterns.

```bash
# Fine-tune (requires GPU)
pip install unsloth datasets transformers trl
python training/finetune.py
```

The fine-tuned model and training data are available in `training/`.

## Model Variants

| Model | Download | VRAM (Q4) | Active Params | Best For |
|-------|----------|-----------|---------------|----------|
| `gemma4:e2b` | 7.2 GB | 4 GB | 2.3B | Mobile, embedded, low-end laptops |
| `gemma4:e4b` | 9.6 GB | 6 GB | 4.5B | Laptops (recommended) |
| `gemma4:26b` | 18 GB | 18 GB | 3.8B (MoE) | Desktop with GPU, best quality/speed ratio |
| `gemma4:31b` | 20 GB | 20 GB | 30.7B | High-end GPU, maximum quality |

Configure via environment variable:
```bash
GEMMA_MODEL=gemma4:e4b python run.py
```

## Tracks

This project was built for the [Gemma 4 Good Hackathon](https://kaggle.com/competitions/gemma-4-good-hackathon):

- **Main Track** -- Overall impact and technical execution
- **Ollama Special Technology Track** -- Local-first AI via Ollama
- **Digital Equity & Inclusivity Impact Track** -- Protecting vulnerable communities

## Built With

- [Gemma 4](https://deepmind.google/models/gemma/gemma-4/) -- Google's open AI model
- [Ollama](https://ollama.com) -- Local model serving
- [Unsloth](https://github.com/unslothai/unsloth) -- Efficient fine-tuning
- [FastAPI](https://fastapi.tiangolo.com) -- Async Python backend

## License

MIT License. See [LICENSE](LICENSE).

## Team

Built by [Forge Dev.studio](https://forgedev.studio)

---

*Beacon: Because everyone deserves protection, not just those who can afford it.*
