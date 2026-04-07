# Beacon: Privacy-First AI Protection for Vulnerable Communities

## Subtitle
Using Gemma 4's local inference, function calling, and vision capabilities to protect the people who need it most -- without ever touching their data.

---

## The Problem Nobody Talks About

Americans reported losing over $10 billion to fraud in 2023 (FTC), and that is only the 5% that gets reported. True losses may exceed $200 billion annually. Seniors lose an average of $33,915 per scam incident (FBI IC3). Behind every number is a real person: a grandmother who lost her savings to a phone scam, an immigrant who signed a predatory lease they could not fully read, a worker fired in retaliation who did not know their rights.

The only mainstream AI scam checker -- Norton Genie -- was shut down in 2024, leaving a gaping void. The tools that remain require cloud processing (your sensitive documents leave your device), paid subscriptions (the people who need it most cannot afford them), or technical expertise (the people who need it most do not have it). Scammers have adopted AI to craft more convincing attacks. Their victims have not been given AI to fight back.

Until now.

## Enter Beacon

Beacon is a free, open-source AI tool powered by Gemma 4 that runs 100% locally on your computer. It provides three core protections:

**Scam Scanner**: Paste any suspicious email, text, or letter -- or upload a screenshot for multimodal analysis. Beacon's two-stage pipeline delivers an instant rule-based pre-screen (red flags within one second) followed by full Gemma 4 analysis using native function calling to produce a structured trust score (0-100), scam type classification, flagged red flags, and a plain-language explanation anyone can understand. Results stream in token-by-token via SSE so users see the analysis forming in real time.

**Contract Reader**: Paste any contract, lease, or legal document. Beacon translates legalese into everyday English, flags predatory clauses, identifies hidden costs, compares terms against fair market standards, and suggests specific questions to ask before signing.

**Rights Navigator**: Describe your situation in your own words. Beacon identifies your applicable legal rights with citations, provides step-by-step action plans, lists free legal aid resources with contact information, and highlights critical deadlines.

All three tools work in 10 languages: English, Spanish, Chinese, Vietnamese, Korean, Tagalog, Arabic, French, Russian, and Hindi -- serving the immigrant communities most targeted by fraud.

## Why Gemma 4 Is the Right Model for This

Beacon's design philosophy is "privacy by architecture, not by policy." This is not a cloud service that promises not to read your data. It is a system where your data physically cannot leave your device. Gemma 4 makes this possible:

**Local-first inference via Ollama**: Gemma 4's E4B variant runs efficiently on consumer hardware (6GB VRAM). This means Beacon works on a typical laptop without a dedicated GPU -- bringing frontier AI protection to hardware that vulnerable communities actually own.

**Native function calling**: Gemma 4's structured output capability is critical for Beacon's scam analysis. Rather than parsing free-text responses, we use function calling to reliably extract trust scores, risk classifications, and red flag arrays. This makes the analysis consistent and machine-parseable while keeping the explanations warm and human.

**Multimodal understanding**: Users can upload screenshots of suspicious texts or photos of physical mail. Gemma 4's vision capabilities mean Beacon protects against both digital and physical-world threats -- critical for elderly users who receive scams on paper.

**Open weights**: Because Gemma 4 is open, we fine-tuned a specialized scam detection model using Unsloth with 50+ curated examples covering 13 scam types. The fine-tuned E4B model achieves higher accuracy on fraud classification while maintaining the same hardware requirements.

## Technical Architecture

Beacon uses a clean, deliberate architecture designed for accessibility and reliability:

**Two-stage pipeline**: Every scam analysis runs through a lightweight rule-based pre-screener first, catching common red flags (urgency pressure, authority impersonation, suspicious URLs) in under one second. This gives users immediate feedback while the full Gemma 4 analysis generates in parallel. The pre-screen results stream instantly via SSE, followed by the LLM's structured analysis token-by-token.

**Backend**: Python FastAPI with async endpoints for each tool plus dedicated SSE streaming endpoints (`/api/stream/scan`, `/api/stream/contract`, `/api/stream/rights`). Each tool uses a specialized system prompt that instructs Gemma 4 to respond via function calling for structured JSON output. The scam scanner prompt includes a comprehensive fraud taxonomy covering 13 scam categories.

**Trusted Contact system**: Users can register a family member or caregiver as a trusted contact. When Beacon detects a high-risk scam (low trust score), it can alert the trusted contact. All data is stored locally in JSON files -- no server, no accounts, no cloud. This feature directly addresses the isolation that makes elderly fraud victims vulnerable.

**Frontend**: A Progressive Web App (PWA) built with vanilla HTML/CSS/JS -- no npm, no webpack, no Node.js required. The service worker caches all static assets for offline use. The app is installable on desktop and mobile, supports dark mode (toggle plus OS preference detection), includes a history drawer (localStorage-backed, filterable by analysis type), offers keyboard shortcuts (Alt+1-4 for tabs, Ctrl+Enter to submit, Escape to close drawers), provides export/print/copy for results, and meets WCAG accessibility standards with ARIA landmarks, skip navigation, and full screen reader support.

**Fine-tuning**: We fine-tuned Gemma 4 E4B using Unsloth with LoRA adapters on curated labeled data. A Modelfile is included for direct Ollama import.

## Challenges We Overcame

**Structured output reliability**: Early iterations sometimes produced malformed JSON. We implemented a multi-layer extraction strategy: function calling first, then JSON block parsing, then brace-matching, with a graceful fallback that still provides useful analysis.

**Speed perception**: LLM inference on consumer hardware takes time. The two-stage pipeline solves this -- users see instant pre-screen results within one second, then watch the full analysis stream in token-by-token. This transformed the experience from "waiting 30 seconds staring at a spinner" to "getting progressively richer results."

**Accessibility at every layer**: Our target users include elderly individuals, immigrants, and people with limited technical experience. Every design decision prioritized clarity: large text, high contrast, simple navigation, plain-language explanations, multilingual support, and zero required technical knowledge.

## Real-World Impact

Beacon addresses a $28.3B problem that disproportionately affects vulnerable populations. One in three seniors is targeted by scams yearly. Immigrants face predatory contracts in a language they are still learning. Low-wage workers do not know their rights when employers violate labor law.

Beacon is free, private, works offline, and speaks 10 languages. It requires no account, no subscription, and no technical expertise. It runs on hardware people already own. The Trusted Contact system means a grandson in another state can be alerted when his grandmother encounters a scam -- closing the isolation gap that predators exploit.

This is exactly the kind of tool that Gemma 4's open, local-first architecture was designed to enable.

## What's Next

- Browser extension for real-time email and website scanning
- Mobile app for on-the-go protection
- Community-contributed scam databases for localized threat detection
- Integration with local legal aid organizations for direct referrals
- Voice input for users who struggle with typing

---

*Track: Main Track / Ollama Special Technology / Digital Equity & Inclusivity*

*Code: https://github.com/credwine/beacon*
