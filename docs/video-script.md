# Beacon -- Video Script (3 minutes)

**IMPORTANT:** Based on analysis of past Gemma hackathon winners, the video is
the #1 factor judges evaluate. Every winner told a personal story, showed real
users, and demonstrated offline/on-device capability prominently.

---

## Scene 1: The Problem (0:00 - 0:30)
**[Corey speaking directly to camera, casual setting, warm lighting]**

"My grandmother lost three thousand dollars to a phone scam. Someone called
pretending to be from the IRS, told her she'd be arrested if she didn't pay.
She was terrified. She drove to Walgreens, bought gift cards, and read them
the numbers over the phone."

**[Cut to statistics, clean white text on dark background, appearing one at a time]**

"She's not alone."

- $10 billion in reported fraud losses in 2023
- Only 5% of fraud even gets reported
- Seniors lose an average of $33,915 per scam
- The only AI scam checker -- Norton Genie -- was shut down in 2024

**[Beat]**

"Scammers have AI now. Their victims don't."

---

## Scene 2: Introducing Beacon (0:30 - 0:55)
**[Beacon logo animates in. Music shifts to hopeful.]**
**[Corey, to camera]**

"So I built Beacon. It's free. It's open source. And it runs entirely on your
device -- powered by Google's Gemma 4 AI through Ollama."

**[Quick montage: landing page scrolling, app switching between tabs]**

"No cloud. No subscriptions. No data ever leaves your computer."

**[KEY MOMENT: Corey visibly toggles airplane mode ON on his laptop]**

"Watch this. I just turned on airplane mode. No internet at all."

**[Camera shows airplane mode icon in taskbar]**

"Beacon still works. Because the AI runs right here, on my machine."

---

## Scene 3: Live Demo - Scam Scanner (0:55 - 1:40)
**[Screen recording, Corey narrating]**

"Let me show you. Here's an actual phishing email I got last week."

**[Paste email into Scam Scanner. Instant pre-screen flags appear within 1 second.]**

"Immediately -- before the AI even finishes thinking -- Beacon's rule-based
pre-screener catches three red flags. Urgency pressure, authority
impersonation, and a suspicious URL."

**[Full Gemma 4 results appear with trust score animation]**

"And here's the full AI analysis. Trust score: 5 out of 100. Dangerous."

"It found five red flags, classified this as a phishing attack, and -- this
is the part I built for my grandmother --"

**[Zoom into the explanation text]**

"It explains the danger in plain English. Not technical jargon. Not a scary
warning. Just a clear, warm explanation of why this is dangerous and what
to do instead."

---

## Scene 4: Live Demo - Contract Reader (1:40 - 2:10)
**[Screen recording]**

"But Beacon does more than catch scams. Here's a lease agreement with some
concerning clauses."

**[Paste contract, results appear]**

"Beacon flags the predatory terms -- this landlord is trying to charge for
normal wear and tear, which is illegal in most states. The mandatory
arbitration clause. Hidden fees. And it gives you the exact questions to
ask before signing."

"This is the kind of analysis that costs hundreds of dollars from a lawyer.
Beacon does it for free, on your laptop, in seconds."

---

## Scene 5: Technical Architecture + Screenshot Scanning (2:10 - 2:35)
**[Architecture diagram: Pre-screener -> Gemma 4 -> Structured Output]**

"Under the hood, Beacon uses a two-stage pipeline. First, a lightweight
rule-based pre-screener gives instant feedback. Then Gemma 4's native
function calling produces structured analysis -- trust scores, risk
classifications, and red flag arrays."

**[Quick demo: user uploads a screenshot of a suspicious text message]**

"And because Gemma 4 is multimodal, you can scan screenshots too. Take a
photo of a suspicious text, upload it, and Beacon reads and analyzes it."

"We also fine-tuned a specialized scam detection model using Unsloth."

---

## Scene 6: Vision and Close (2:35 - 3:00)
**[Corey, speaking to camera, genuine and direct]**

"I built Beacon because I believe everyone deserves protection. Not just
people who can afford cybersecurity software. Not just people who understand
technology. Everyone."

"With Gemma 4 running locally, we can put frontier AI directly in the hands
of the people who need it most. No gatekeepers. No subscriptions. No
compromises on privacy."

**[Beat]**

"The AI revolution should protect the people who are falling behind. Not
just help the people who are already doing fine."

**[Beacon logo + tagline appear]**

"Beacon. Your AI guardian. Completely private. Always free."

**[GitHub URL + QR code fade in]**

---

## Production Notes

### Critical Success Factors (from past winners analysis)
1. **Personal story is the hook** -- Corey's grandmother story is authentic and powerful. Lead with it.
2. **Show airplane mode** -- Past winners visibly demonstrated offline capability. This is a key moment.
3. **Two-stage pipeline demo** -- Show the instant pre-screen, then the AI analysis. This demonstrates engineering depth.
4. **Plain-language explanation** -- Zoom into the explanation text. This is the emotional payoff.
5. **Keep it authentic** -- iPhone camera is fine. Natural lighting. Don't over-produce. Past winners used simple setups.
6. **No slides** -- Show the actual app running on a real device. No PowerPoints.

### Equipment
- Screen recording: OBS Studio (free)
- Camera: iPhone or webcam (simple, authentic)
- Microphone: Any decent headset mic or Airpods
- Background music: royalty-free from YouTube Audio Library
- Editing: CapCut, DaVinci Resolve (free), or iMovie

### Shot List
1. Corey to camera -- grandmother story (0:00-0:30)
2. Statistics on dark background (0:15-0:25)
3. Airplane mode toggle (0:45-0:55) -- KEY MOMENT
4. Screen recording: Scam Scanner with pre-screen + full analysis (0:55-1:40)
5. Screen recording: Contract Reader (1:40-2:10)
6. Architecture diagram (2:10-2:20)
7. Screenshot scanning demo (2:20-2:30)
8. Corey to camera -- closing message (2:35-3:00)
9. Logo + links (2:55-3:00)

### Music
- 0:00-0:30: Soft, slightly somber piano (the problem)
- 0:30-3:00: Uplifting, building to resolution (the solution)
- Use a single continuous track if possible for cohesion

### Pacing
- Never stay on one shot for more than 10-15 seconds
- Cut between Corey and screen recordings frequently
- Statistics should animate in one at a time (not all at once)
- The airplane mode moment should have a brief pause for emphasis
