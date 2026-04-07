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

**[Quick montage: landing page scrolling, dark mode toggle, language selector
switching to Spanish, app switching between tabs]**

"No cloud. No subscriptions. No data ever leaves your computer. It works in
ten languages, installs as an app on your phone or desktop, and even has a
dark mode."

**[KEY MOMENT: Corey visibly toggles airplane mode ON on his laptop]**

"Watch this. I just turned on airplane mode. No internet at all."

**[Camera shows airplane mode icon in taskbar]**

"Beacon still works. Because it's a PWA -- the whole interface is cached
offline -- and the AI runs right here, on my machine."

---

## Scene 3: Live Demo - Scam Scanner (0:55 - 1:40)
**[Screen recording, Corey narrating]**

"Let me show you. Here's an actual phishing email I got last week."

**[Paste email into Scam Scanner. Instant pre-screen flags appear within 1 second.]**

"Immediately -- before the AI even finishes thinking -- Beacon's rule-based
pre-screener catches three red flags. Urgency pressure, authority
impersonation, and a suspicious URL. That's the two-stage pipeline: instant
feedback first, then the full AI analysis streams in token by token."

**[Full Gemma 4 results stream in with trust score animation]**

"Trust score: 5 out of 100. Dangerous."

"It found five red flags, classified this as a phishing attack, and -- this
is the part I built for my grandmother --"

**[Zoom into the explanation text]**

"It explains the danger in plain English. Not technical jargon. Not a scary
warning. Just a clear, warm explanation of why this is dangerous and what
to do instead."

**[Click the screenshot upload button, upload an image of a suspicious text]**

"And because Gemma 4 is multimodal, you can upload screenshots too. Take a
photo of a suspicious text, drop it in, and Beacon reads and analyzes it."

---

## Scene 4: Live Demo - Contract Reader + Trusted Contacts (1:40 - 2:10)
**[Screen recording]**

"But Beacon does more than catch scams. Here's a lease agreement with some
concerning clauses."

**[Paste contract, results stream in]**

"Beacon flags the predatory terms -- this landlord is trying to charge for
normal wear and tear, which is illegal in most states. The mandatory
arbitration clause. Hidden fees. And it gives you the exact questions to
ask before signing."

"This is the kind of analysis that costs hundreds of dollars from a lawyer.
Beacon does it for free, on your laptop, in seconds."

**[Quick cut: open Trusted Contacts panel, show adding a contact]**

"And here's something I built specifically for families. You can add a
trusted contact -- a son, daughter, caregiver -- and when Beacon detects
a dangerous scam, they get notified. Because the people targeted by fraud
are often isolated, and this closes that gap."

---

## Scene 5: History, Accessibility, and Architecture (2:10 - 2:35)
**[Screen recording: open history drawer with Alt+H]**

"Every analysis is saved in your history drawer -- stored locally, never in
the cloud. You can filter by type, reload past analyses, and export or print
any result."

**[Architecture diagram: Pre-screener -> Gemma 4 -> Structured Output via SSE]**

"Under the hood, Beacon uses a two-stage pipeline. A lightweight rule-based
pre-screener gives instant feedback, then Gemma 4's native function calling
produces structured analysis -- trust scores, risk classifications, and red
flag arrays -- streamed via Server-Sent Events."

"We also fine-tuned a specialized scam detection model using Unsloth,
trained on 50-plus examples covering 13 scam types."

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
2. **Show airplane mode** -- Past winners visibly demonstrated offline capability. The PWA angle makes this even stronger -- the whole UI works, not just the AI.
3. **Two-stage pipeline demo** -- Show the instant pre-screen, then the streaming AI analysis. This demonstrates engineering depth.
4. **Dark mode + language switch montage** -- Quick visual proof of polish and inclusivity. Don't dwell, just flash it.
5. **Trusted Contacts** -- This is a differentiator. Show it. It connects back to the grandmother story.
6. **History drawer** -- A quick Alt+H open is visual proof the app has depth.
7. **Plain-language explanation** -- Zoom into the explanation text. This is the emotional payoff.
8. **Keep it authentic** -- iPhone camera is fine. Natural lighting. Don't over-produce. Past winners used simple setups.
9. **No slides** -- Show the actual app running on a real device. No PowerPoints.

### Equipment
- Screen recording: OBS Studio (free)
- Camera: iPhone or webcam (simple, authentic)
- Microphone: Any decent headset mic or Airpods
- Background music: royalty-free from YouTube Audio Library
- Editing: CapCut, DaVinci Resolve (free), or iMovie

### Shot List
1. Corey to camera -- grandmother story (0:00-0:30)
2. Statistics on dark background (0:15-0:25)
3. Quick montage: dark mode toggle, language selector, tabs (0:30-0:40)
4. Airplane mode toggle (0:45-0:55) -- KEY MOMENT
5. Screen recording: Scam Scanner with pre-screen + streaming analysis (0:55-1:25)
6. Screen recording: Screenshot upload for multimodal scan (1:25-1:40)
7. Screen recording: Contract Reader with streaming results (1:40-2:00)
8. Screen recording: Trusted Contacts panel (2:00-2:10)
9. Screen recording: History drawer open via Alt+H (2:10-2:18)
10. Architecture diagram (2:18-2:30)
11. Corey to camera -- closing message (2:35-3:00)
12. Logo + links (2:55-3:00)

### Music
- 0:00-0:30: Soft, slightly somber piano (the problem)
- 0:30-3:00: Uplifting, building to resolution (the solution)
- Use a single continuous track if possible for cohesion

### Pacing
- Never stay on one shot for more than 10-15 seconds
- Cut between Corey and screen recordings frequently
- Statistics should animate in one at a time (not all at once)
- The airplane mode moment should have a brief pause for emphasis
- The dark mode / language montage should be fast cuts (2-3 seconds each)
