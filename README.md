# Beacon

**Privacy-First AI Protection for Vulnerable Communities**

Beacon uses Google's Gemma 4 running entirely on your device to detect scams, explain contracts in plain English, and help you know your rights. No data ever leaves your computer.

---

## The Problem

Americans reported losing over **$10 billion to fraud** in 2023 (FTC) -- and only 5% of fraud gets reported. Seniors lose an average of **$33,915 per scam incident** (FBI IC3). The only mainstream AI scam checker -- Norton Genie -- was shut down in 2024, leaving a gaping void.

Existing solutions require cloud processing, paid subscriptions, or technical expertise. Scammers have adopted AI. Their victims haven't been given AI to fight back.

## The Solution

Beacon is a free, open-source AI tool that runs **100% locally** on your computer. It uses **Gemma 4** via **Ollama** for private, offline-capable analysis across three core tools:

### Scam Scanner
Paste any suspicious email, text, or letter -- or upload a screenshot for multimodal analysis. Beacon gives you:
- **Trust Score** (0-100) with color-coded risk level
- **Scam type** classification (phishing, advance fee, impersonation, and 10 more)
- **Red flags** identified in the message
- **Plain-language explanation** anyone can understand
- **Recommended actions** and safe alternatives

### Contract Reader
Paste any contract, lease, or legal document. Beacon:
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

## Key Features

| Feature | Details |
|---------|---------|
| **Two-stage pipeline** | Instant rule-based pre-screener flags red flags in under 1 second, then Gemma 4 LLM delivers full structured analysis |
| **SSE streaming** | Real-time token-by-token display so users see results as they generate |
| **Multimodal scanning** | Upload screenshots or photos of suspicious texts for Gemma 4 vision analysis |
| **Trusted Contacts** | Add a family member or caregiver who gets alerted when Beacon detects a high-risk scam |
| **10 languages** | English, Spanish, Chinese, Vietnamese, Korean, Tagalog, Arabic, French, Russian, Hindi |
| **PWA** | Installable on desktop and mobile with offline-cached frontend via service worker |
| **Dark mode** | Manual toggle plus automatic OS preference detection |
| **History drawer** | All past analyses saved in localStorage, filterable by type, reloadable |
| **Keyboard shortcuts** | Alt+1-4 switch tabs, Ctrl+Enter submits, Escape closes drawers, Alt+H opens history |
| **Export/print/copy** | Share or save analysis results in multiple formats |
| **Full accessibility** | ARIA landmarks, skip navigation link, screen reader support, keyboard navigable |
| **Animated landing demo** | Typewriter-style scam analysis on the homepage shows Beacon in action |

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
git clone https://github.com/credwine/beacon.git
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
                        +------------------+
                        |   Browser (PWA)  |
                        |  HTML/CSS/JS     |
                        |  Service Worker  |
                        +--------+---------+
                                 |
                                 | SSE streaming
                                 v
                    +------------+-------------+
                    |    FastAPI Async Backend  |
                    |                          |
                    |  1. Rule-based           |
                    |     pre-screener         |
                    |     (instant red flags)  |
                    |                          |
                    |  2. Gemma 4 LLM          |
                    |     (structured output   |
                    |      via function calling)|
                    +------------+-------------+
                                 |
                                 v
                    +------------+-------------+
                    |   Ollama (Gemma 4 E4B)   |
                    |   Local inference only   |
                    |   No data leaves device  |
                    +--------------------------+
```

**Technical highlights:**
- **Two-stage pipeline** -- instant rule-based pre-screening before full LLM analysis
- **SSE streaming endpoints** -- real-time token-by-token results via Server-Sent Events
- **Gemma 4 native function calling** -- structured JSON output (trust scores, risk arrays, red flags)
- **Multimodal vision** -- screenshot and image analysis via Gemma 4's vision capabilities
- **FastAPI async backend** -- non-blocking I/O for responsive UI during inference
- **PWA with service worker** -- installable, offline-cached frontend
- **Zero-dependency frontend** -- vanilla HTML/CSS/JS, no build step
- **Docker Compose** -- one-command deployment with GPU pass-through

## Fine-Tuned Model (Unsloth)

We fine-tuned Gemma 4 E4B specifically for scam detection using [Unsloth](https://github.com/unslothai/unsloth), creating a specialized model that's faster and more accurate at identifying fraud patterns across 13 scam types. The training dataset includes 50+ curated examples.

```bash
# Fine-tune (requires GPU)
pip install -r training/requirements.txt
python training/finetune.py
```

A [Modelfile](training/Modelfile) is included for importing the fine-tuned model into Ollama. Training data and scripts are in `training/`.

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
