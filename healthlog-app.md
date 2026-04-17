# HealthLog — AI Personal Health Journal App

## What It Is

A mobile app (iOS + Android) that helps people with recurring health issues understand what's causing their bad days. Users log daily symptoms, mood, sleep, energy and medications — AI analyzes patterns and talks to them about it every day. Not a passive logging tool — an active daily health companion.

## Core Value Proposition

> "An AI that learns your health patterns and talks to you about them every day — so you finally understand why you feel the way you feel."

## Target Audience

- People 30-55 with at least one chronic or recurring health issue (migraines, fatigue, anxiety, chronic pain, perimenopause, ADHD, autoimmune conditions)
- Proactive about their health but frustrated that doctors can't see the full picture
- Currently tracking nothing, or tracking in Notes/spreadsheets
- US market primary, global secondary

## Pricing Model

- 7-day free trial, no credit card required at signup
- Monthly: $6.99/month
- Yearly: $49.99/year (promoted as "best value — save 40%")
- Revenue via RevenueCat (handles iOS + Android billing)
- Apple/Google take 30% (15% after year 1 for small developers)

## Revenue Projections

| Month | Downloads/mo | Subscribers | MRR |
|---|---|---|---|
| 1 | 500 (seeded) | 15-25 | ~$150 |
| 3 | 1,000-2,000 | 80-150 | ~$800 |
| 6 | 3,000-5,000 | 300-500 | ~$2,800 |
| 12 | 5,000-10,000 | 800-1,500 | ~$8,000 |
| 18 | 8,000-15,000 | 1,500-3,000 | ~$15,000 |

---

## Tech Stack

- **Framework:** Expo (React Native) — one codebase for iOS + Android
- **Database:** Supabase (PostgreSQL) — free tier until scale
- **Auth:** Supabase Auth (email magic link, Apple Sign-In, Google Sign-In)
- **AI:** Claude API (Anthropic) — daily check-ins, weekly insights, pattern analysis
- **Voice transcription:** Whisper API (OpenAI) — for voice note logging
- **Subscriptions:** RevenueCat — free until $2.5K MRR
- **Push notifications:** Expo Notifications
- **Analytics:** PostHog (open source, self-hostable)
- **Hosting:** Supabase (backend), Expo EAS (builds)
- **iOS builds:** Expo EAS Build (no Mac required)

### Accounts needed

- Apple Developer: $99/year
- Google Play: $25 one-time
- Expo EAS: $3/month (or free tier)
- RevenueCat: free until $2.5K MRR
- Supabase: free tier
- Claude API: ~$5-20/month at low usage

**Total launch cost: ~$130**

---

## Key Differentiators vs Competitors

| App | Problem |
|---|---|
| Daylio | Mood only, no AI insights, no health context |
| Bearable | Complex, overwhelming, no AI conversation |
| Symple | Medical-feeling, no retention hooks, just logging |
| CareClinic | Feature bloat, not AI-first |
| **HealthLog** | AI talks to you daily, finds patterns, generates stories |

**The gap:** Every competitor is a passive logging tool. We are an active daily conversation. The AI remembers everything and proactively surfaces insights rather than waiting for users to dig through charts.

---

## Core Features

### 1. AI Daily Check-in (Primary Retention Hook)

Instead of opening to a blank log form, the app opens with a personalized AI message based on previous entries:

> "Yesterday you had a headache and low energy. Did you sleep differently last night? Let's see if there's a connection."

Or:

> "You've logged 5 days in a row 🔥 — based on your last week, today might be a high-energy day. Here's why..."

**Flow:**
- App opens → AI greeting with observation or question
- User responds to AI prompt OR taps "Log today"
- Quick log (under 30 seconds for returning users)
- AI acknowledges the entry with a micro-insight: "Your energy today (7/10) is higher than your Wednesday average (5.4/10)"

**Why it matters:** Transforms the app from a chore into a conversation. Users feel heard. Creates daily habit through curiosity, not guilt.

### 2. Daily Log Entry

Fast, minimal friction. Under 30 seconds for a returning user.

**Fields:**
- Mood slider (😞 to 😄, 1-10)
- Energy slider (Low to High, 1-10)
- Sleep hours (tap +/-)
- Symptoms (tap from personal list or add new)
  - Headache (with severity: mild / moderate / severe)
  - Fatigue
  - Nausea
  - Anxiety
  - Brain fog
  - Joint pain
  - + any custom symptom user creates
- Medications taken today (tap to confirm each from personal medication list)
- Free text notes (optional)
- Voice note option → auto-transcribed

**Smart defaults:**
- App remembers usual logging time, sends reminder at that time
- Yesterday's medications pre-checked (tap to uncheck if skipped)
- Common symptoms shown first based on user's history

### 3. Weekly Health Story (Weekly Retention Hook)

Every Sunday, AI generates a personalized narrative — not charts, a human-readable story:

> "This was a tough week for you. You had 3 low-energy days, all following nights under 6 hours of sleep. But Wednesday was your best day — 8 hours of sleep, no symptoms, and you noted feeling focused. Your Magnesium adherence dropped to 60% this week — and interestingly, your headache count doubled compared to last week."

**Key design decisions:**
- Prose narrative, not bullet points or charts
- Specific numbers make it feel personal and trustworthy
- Delivered as a push notification: "Your weekly health story is ready"
- Shareable as screenshot (drives organic word of mouth)
- Saved permanently in "Stories" tab

### 4. Streak System with Real Value Unlocks

Not just a counter — streak unlocks meaningful features:

| Streak | Unlock |
|---|---|
| 3 days | Basic pattern detection enabled |
| 7 days | First AI insight generated |
| 14 days | Correlation analysis unlocked (sleep vs energy, food vs symptoms) |
| 30 days | Full health report — doctor-ready PDF export |
| 60 days | Predictive insights ("tomorrow might be a low-energy day based on your patterns") |

**Streak break handling:**
- Gentle AI message, no guilt: "We lost 2 days — want to fill them in quickly?"
- Retroactive logging allowed for past 3 days
- "Streak freeze" purchasable (monetization add-on)

### 5. Trends & Pattern Analysis

**Charts available:**
- Mood over time (line chart, 7/30/90 day views)
- Symptom frequency calendar (heatmap)
- Sleep vs energy correlation scatter
- Medication adherence bar chart
- Top triggers this month

**AI correlation detection:**
- Automatically finds statistically significant patterns
- "Your headaches occur on days following less than 6 hours of sleep — 83% correlation"
- "4 of your 6 headaches this month were on days you noted skipping lunch"
- Minimum 14 days of data before correlations shown (avoids false positives)

### 6. Medication Reminders with Context

Not a generic alarm — a contextual reminder:

> "Time for Magnesium 💊 — you've taken it 6 days in a row. On those days, your headache score averaged 2.1 vs 4.3 on missed days. Keep it up."

**Medication setup:**
- Name, dose, frequency, time
- Track as: prescription / supplement / OTC
- Link to symptoms (optional: "I take this for migraines")
- Adherence statistics tracked and shown

### 7. Doctor Report Export

30-day PDF export formatted for a medical appointment:

- Summary of symptoms by frequency and severity
- Medication adherence rates
- Sleep averages
- Identified patterns and correlations
- Timeline view of worst days

**Why this matters:** Patients forget their symptoms between appointments. A clean PDF that shows patterns makes the 15-minute doctor visit actually useful. This feature is a primary conversion driver — users upgrade specifically to get this.

### 8. AI Chat (Ask Anything)

Within the Insights tab, users can ask the AI questions about their own data:

> "Why do I feel worse on Mondays?"
> "Is my Magnesium actually helping?"
> "What was my best week this month and why?"

AI answers using only the user's own data, not generic health advice. Responses cite specific logged entries:

> "Your Mondays tend to follow Sundays where you logged later bedtimes (average 1:30am vs 11pm on other nights). Your sleep on Sunday nights averages 5.8 hours vs your weekly average of 7.1 hours."

---

## Screen Structure

```
Bottom Navigation:
[🏠 Home] [➕ Log] [📊 Trends] [💡 Insights]

Home Tab:
- AI daily greeting / check-in prompt
- Today's log summary (or "Log today" CTA if not done)
- This week's insight card (tap to expand)
- 7-day mood strip
- Quick access: Medications | Trends

Log Tab (modal, opens from + button):
- Mood slider
- Energy slider
- Sleep hours
- Symptom selector
- Medication checklist
- Notes / voice
- Save button

Trends Tab:
- Time range selector (7d / 30d / 90d)
- Mood chart
- Symptom frequency
- Sleep chart
- Top triggers
- Correlations found
- Export PDF button (Pro)

Insights Tab:
- Weekly health story (latest)
- Previous stories archive
- AI pattern cards
- Ask AI chat input
- Streak tracker with unlock milestones
```

---

## Retention Strategy

### Daily (open every day)
- AI greeting is personalized — curious what it says today
- Medication reminders with context
- Streak protection

### Weekly (Sunday)
- Push notification: "Your weekly health story is ready"
- Story is shareable → organic spread

### Monthly
- 30-day report unlock (if streak maintained)
- Monthly summary notification: "You had 3 fewer headaches than last month"

### Passive (don't need to open)
- Patterns surface over time — returning after a break shows "Here's what changed while you were gone"

---

## What Is NOT in MVP

- No social/community features (phase 2 — needs user base)
- No wearable integration / Apple Health sync (phase 2)
- No doctor-facing portal (phase 3)
- No family/caregiver sharing (phase 2)
- No web version (mobile only)
- No Android widgets v1 (iOS widget only via WidgetKit)
- No AI medical advice — AI only analyzes user's own logged data, never diagnoses

---

## ASO Strategy (App Store Discovery)

### Primary keywords to target
- "symptom tracker"
- "health journal"
- "mood tracker"
- "migraine tracker"
- "medication tracker"
- "AI health"
- "chronic illness tracker"
- "daily health log"

### App title formula
**"HealthLog: AI Symptom & Mood Tracker"**
— primary keyword in title, AI differentiator visible

### Growth phases

**Phase 1 — Seed (Month 1):**
- Reddit: r/migraine, r/ChronicPain, r/ADHD, r/Anxiety, r/Fibromyalgia
- Facebook chronic illness groups
- Product Hunt launch
- Goal: 500 downloads + 30 reviews at 4.5+ stars

**Phase 2 — Organic (Month 2-6):**
- Improve ASO based on search term data
- Localize to Spanish, German, Portuguese
- Respond to every review
- Share weekly health stories as TikTok/Instagram content

**Phase 3 — Paid (Month 6+, only when profitable):**
- Apple Search Ads (best ROI for App Store)
- Target: people searching for specific condition trackers

---

## Build Timeline

| Week | Deliverable |
|---|---|
| Week 1 | Expo setup, auth (Supabase), daily log screen, symptom/medication setup |
| Week 2 | Home screen, AI daily check-in (Claude API), streak system |
| Week 3 | Trends tab, basic charts, correlation detection logic |
| Week 4 | Weekly health story generation, insights tab, AI chat |
| Week 5 | Paywall (RevenueCat), doctor PDF export, push notifications |
| Week 6 | Polish, App Store screenshots, ASO metadata, submit both stores |

---

## Legal & Compliance

- **Not a medical device.** App is a personal journaling and pattern-recognition tool.
- All AI responses based solely on user's own logged data — no medical diagnosis
- Disclaimer on onboarding: "HealthLog is not a medical device and does not provide medical advice. Always consult your doctor."
- HIPAA: Not required for a consumer wellness app (only required for covered healthcare entities). Standard privacy policy sufficient.
- GDPR: Required for EU users. Data deletion on request, clear privacy policy, no selling data.
- App Store health category guidelines: wellness app, not medical device category

---

## Open Questions

- App name: HealthLog / Patterned / Feelio / Daywell / Tracewell — needs decision
- Minimum data before AI check-ins are personalized (day 1 must work with zero history)
- Voice note transcription: include in free tier or Pro only?
- Retroactive logging: how many days back allowed?
- Should we integrate Apple HealthKit (step count, heart rate) from day 1 or phase 2?
- Localization: launch in English only or include Estonian + Russian from day 1?
