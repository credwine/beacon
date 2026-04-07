# Beacon: Privacy-First AI Protection for Vulnerable Communities

## Subtitle
Using Gemma 4's local inference and function calling to protect the people who need it most -- without ever touching their data.

---

## The Problem Nobody Talks About

Americans lost $28.3 billion to fraud in 2023. Behind that number are real people: a grandmother who lost her savings to a phone scam, an immigrant who signed a predatory lease they couldn't read, a worker fired in retaliation who didn't know their rights.

The people most vulnerable to exploitation are the least likely to have tools that protect them. Enterprise fraud detection exists for banks and corporations. Consumer solutions require cloud processing (your sensitive documents leave your device), paid subscriptions (the people who need it most can't afford it), or technical expertise (the people who need it most don't have it).

What if everyone had a guardian angel for the digital world -- one that never sleeps, never judges, and never shares your secrets?

## Enter Beacon

Beacon is a free, open-source AI tool powered by Gemma 4 that runs 100% locally on your computer. It provides three core protections:

**Scam Scanner**: Paste any suspicious email, text, or letter. Beacon instantly analyzes it using Gemma 4's native function calling to produce a structured trust score (0-100), identify the scam type, flag specific red flags, and explain the danger in plain language anyone can understand.

**Contract Reader**: Paste any contract, lease, or legal document. Beacon translates legalese into everyday English, flags predatory clauses, identifies hidden costs, compares terms against fair market standards, and suggests specific questions to ask before signing.

**Rights Navigator**: Describe your situation in your own words. Beacon identifies your applicable legal rights with citations, provides step-by-step action plans, lists free legal aid resources with contact information, and highlights critical deadlines.

## Why Gemma 4 Is the Right Model for This

Beacon's design philosophy is "privacy by architecture, not by policy." This isn't a cloud service that promises not to read your data. It's a system where your data physically cannot leave your device. Gemma 4 makes this possible:

**Local-first inference via Ollama**: Gemma 4's E4B variant runs efficiently on consumer hardware (6GB VRAM). This means Beacon works on a typical laptop without GPU -- bringing frontier AI protection to hardware that vulnerable communities actually own.

**Native function calling**: Gemma 4's structured output capability is critical for Beacon's scam analysis. Rather than parsing free-text responses, we use function calling to reliably extract trust scores, risk classifications, and red flag arrays. This makes the analysis consistent and machine-parseable while keeping the explanations warm and human.

**Multimodal understanding**: Users can analyze screenshots of suspicious texts or photos of physical mail. Gemma 4's vision capabilities mean Beacon protects against both digital and physical-world threats.

**Open weights**: Because Gemma 4 is open, we could fine-tune a specialized scam detection model using Unsloth. Our fine-tuned E4B model achieves higher accuracy on fraud classification while maintaining the same hardware requirements.

## Technical Architecture

Beacon uses a clean, minimal architecture designed for accessibility and reliability:

```
Browser (HTML/CSS/JS)  -->  FastAPI Backend  -->  Ollama (Gemma 4 E4B)
```

**Backend**: Python FastAPI handles three API endpoints (/api/scan, /api/contract, /api/rights). Each endpoint wraps a specialized service that constructs domain-specific system prompts and leverages Gemma 4's function calling for structured JSON responses. The async architecture ensures responsive UI even during inference.

**Frontend**: Vanilla HTML/CSS/JS with zero build dependencies. This was a deliberate choice: no npm, no webpack, no Node.js required. Anyone can clone the repo and run it. The UI is fully accessible (WCAG compliant, screen-reader friendly, keyboard navigable) with responsive design for mobile devices.

**System prompts**: Each tool uses a carefully engineered system prompt that instructs Gemma 4 to respond in structured JSON. The scam scanner prompt includes a comprehensive fraud taxonomy covering 12 scam categories, while the contract reader prompt encodes knowledge of fair market terms for common document types.

**Fine-tuning**: We fine-tuned Gemma 4 E4B using Unsloth with LoRA adapters on a curated dataset of labeled scam/legitimate messages. The resulting model runs at the same speed on the same hardware but achieves better precision on fraud classification, reducing false positives that could erode user trust.

## Challenges We Overcame

**Structured output reliability**: Early iterations sometimes produced malformed JSON. We implemented a multi-layer extraction strategy: function calling first, then JSON block parsing, then brace-matching, with a graceful fallback that still provides useful analysis.

**Accessibility**: Our target users include elderly individuals and people with limited technical experience. Every design decision prioritized clarity: large text, high contrast, simple navigation, plain-language explanations, and zero required technical knowledge.

**Trust calibration**: A scam scanner is only useful if people trust it. We calibrated trust scores extensively against known scam datasets, ensuring that legitimate messages (like real shipping notifications) score above 80 while obvious scams score below 20. The middle ground (40-60) explicitly communicates uncertainty rather than false confidence.

## Real-World Impact

Beacon addresses a $28.3B problem that disproportionately affects vulnerable populations. One in three seniors is targeted by scams yearly. Immigrants face predatory contracts in a language they're still learning. Low-wage workers don't know their rights when employers violate labor law.

Beacon is free, private, and works offline. It requires no account, no subscription, and no technical expertise. It runs on hardware people already own. It is exactly the kind of tool that Gemma 4's open, local-first architecture was designed to enable.

## What's Next

- Browser extension for real-time email and website scanning
- Mobile app for on-the-go protection
- Community-contributed scam databases for localized threat detection
- Multi-language support for immigrant communities
- Integration with local legal aid organizations for direct referrals

---

*Track: Digital Equity & Inclusivity / Main Track / Ollama Special Technology*

*Code: https://github.com/credwine/beacon*
