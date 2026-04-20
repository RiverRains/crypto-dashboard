# Majajuht — KÜ Management Tool MVP

## What It Is

A modern resident CRM and building management platform for KÜ (korteriühistu) chairmen. Matches Korto's core features, wins on AI-powered chairman tools, and is simple enough for anyone to onboard in 15 minutes.

## Positioning

> "Korto for people who gave up on Korto. Same features, modern UX, AI built in from day one."

Korto has been around since 2005 and covers the market — but plenty of chairmen still don't use it. The gap isn't features, it's complexity, onboarding friction, and zero AI/CRM layer. We are the alternative for everyone who looked at Korto and said "not for me."

## Target Users

- **Primary:** Self-managing KÜ chairmen (volunteer, unpaid or minimally paid, non-technical)
- **Secondary:** Haldusfirmad (management companies) managing multiple buildings
- **Phase 3:** Residents via companion mobile app

## Market

- ~10,000-16,000 apartment associations in Estonia
- ~50-80 new KÜs formed per year from new construction
- 97% home ownership rate
- One real competitor: Korto (since 2005, accounting-first, complex onboarding)
- Estonian + Russian equally polished from day 1 (critical for Lasnamäe, Mustamäe, Ida-Virumaa)

## Pricing

- €0.30/apartment/month
- 40-apartment building = €12/month (paid from KÜ budget, not chairman's pocket)
- 6 months free for buildings onboarded via developer partnerships
- 3-month free trial for direct signups
- Revenue target: 500 KÜs × 40 avg apartments × €0.30 = €6,000/month = €72K/year

## Tech Stack

- **Frontend + API:** Next.js
- **Database:** Supabase (PostgreSQL)
- **Auth:** Email magic link (no passwords — simplest for non-technical users)
- **AI:** Claude API (smart replies, auto-fill, interaction summaries)
- **SMS:** Messente API (~€0.03/SMS, Estonian provider)
- **Email:** Resend or Postmark
- **Hosting:** Vercel
- **Languages:** Estonian + Russian from day 1
- **Running cost:** Under €30/month until 50+ paying KÜs

---

## The Three Pillars

### Pillar 1: Match Korto's Core Features (Table Stakes)

Must exist to be taken seriously. Not better than Korto — just present and working.

- Announcements with email + SMS delivery
- Meter readings (residents submit, chairman sees)
- Invoice view per resident
- Document storage (protocols, contracts, annual reports)
- Voting + auto-generated protocols
- Resident and apartment cards

### Pillar 2: Win on AI Layer (Our Differentiator)

What Korto doesn't have. Why chairmen switch.

- **Instant universal search** — type car plate, name, phone, apartment number → see everything related instantly. No menus, no navigation.
- **Resident context panel** — when a resident contacts you, see their full history: last messages, outstanding debts, previous complaints, notes — all in one place before you reply
- **Smart reply templates with auto-fill** — answer a question once, reuse forever. System auto-inserts this resident's name, m², current tariff, calculated amount, previous amount, difference, date of last change
- **Delayed send** — draft a reply instantly, schedule it to send later. Resident thinks you carefully considered their complaint overnight.
- **Interaction log per resident** — every message, call note, complaint, request logged with timestamp. Legal protection + "I answered you on March 14 at 11:23"
- **Custom linked lists** — every building is different. Chairman creates their own lists (car plates, storage rooms, gate remote IDs, electronic keys, parking spots) and links them to apartments or residents. Search across all lists simultaneously.
- **AI-suggested replies** — based on the incoming message and resident history, AI suggests a response using past answers as templates

### Pillar 3: Win on Simplicity (Our Moat Against Korto's Complexity)

- Onboarding in 15 minutes — no accounting knowledge required
- No mandatory accounting setup before you can use the tool
- AI-guided setup: "What's your building address? How many apartments?" — app does the rest
- Mobile-first responsive design (works on phone without a dedicated app)
- Clean, modern UI — not a 2005 design refreshed

---

## Feature Priority (Build Order)

### Week 1: Core Data Layer
- Auth (email magic link)
- Building setup wizard (address, apartments, m² per apartment)
- Resident directory with apartment cards
- Search: name, apartment number, phone, car plate
- Custom linked lists (create list → define fields → link to apartment/resident)

### Week 2: Communications
- Announcements with filters (all / by stairwell / by floor / by apartment size)
- Email delivery with read receipts
- SMS fallback for unread announcements
- Announcement archive

### Week 3: AI Layer
- Interaction log per resident (manual entry + auto-log from sent messages)
- Smart reply templates with variable auto-fill
- AI-suggested reply based on message content + resident history
- Delayed send feature
- Resident context panel (full history visible when composing a message)

### Week 4: Meetings + Voting
- Meeting creation with agenda
- Invitation send (email + SMS reminder 24h before)
- Written decision procedure (kirjalik otsus) — fully digital voting with deadline
- Attendance tracking + quorum auto-calculation (based on m² shares)
- Vote counting (m²-weighted)
- Auto-generated protocol PDF
- Protocol archive

### Week 5: Documents + Polish + Deploy
- Document storage with categories
- Meter readings (resident submission via link, no login required)
- Maintenance calendar with recurring reminders
- Dashboard: unread messages, upcoming events, debtors summary
- Mobile responsive polish
- Deploy to production

---

## What Is NOT in MVP

- No accounting/bookkeeping (let Merit/Korto handle that — we are not replacing their accountant)
- No mobile app (responsive web first — companion app is phase 2)
- No hardware integration for barriers/locks (phase 2 — Pavel's request)
- No payment processing (chairman uses existing invoicing tools)
- No haldusfirma multi-building dashboard (phase 2)

---

## Key Product Insights from User Research

1. **This is a CRM, not an accounting tool.** Every competitor is accounting-first. The gap is management-first with AI context.
2. **Residents won't self-serve.** Don't redirect residents to read FAQs. Give the chairman tools to respond faster.
3. **Every KÜ is different.** Flexible custom lists are essential. Rigid fixed fields will always miss something.
4. **Written record is power.** Every interaction logged = legal protection + proof = "I answered you on March 14."
5. **Elderly residents are a reality.** SMS fallback, option to print. But the tool's value is freeing chairman time with digital-capable residents.
6. **The chairman is buyer AND sales force.** If the tool makes their life easier, they push the general meeting to approve the expense.
7. **Korto exists but has gaps.** People are asking for alternatives in Facebook groups despite Korto existing for 20 years. The gap is UX, onboarding complexity, and zero AI.
8. **Pavel's insight:** Residents don't read FAQs or look up documents. They contact the chairman directly. The tool must help the chairman respond fast — not redirect residents.

---

## Competitive Landscape

| Tool | Price | Focus | Weakness |
|---|---|---|---|
| Korto.ee | ~€0.10-0.30/apt/month | Accounting + management | Since 2005, complex onboarding, no AI, accounting-first |
| Ühekatuseall | €0.20/apt/month | Accounting + management | Complex, designed for power users |
| Digimaja | Quote-based | Accounting for haldusfirmad | Targets management companies, not individual KÜs |
| Profit KÜ | License-based | Desktop accounting | Desktop-only, database corruption issues, ancient |
| Merit KÜ | Part of Merit | Accounting with KÜ bolt-on | Accounting tool first, KÜ is secondary |

**Our differentiator:** Management-first, AI-powered, simple onboarding, modern UX. Accounting is not our job.

---

## Go-to-Market Strategy

Four channels that feed each other:

### Channel 1: Facebook Groups (Now — Free)
- Active thread already running with engaged chairmen
- Pavel Zujev: first beta tester, has programming background, manages his own KÜ
- Post progress updates as we build — community becomes invested
- Target: 3-5 test KÜs from this group for validation

### Channel 2: Developer Partnerships (Month 4+)
**The idea:** Pre-install Majajuht in new buildings. When developer hands over a building to the new KÜ, the management system comes pre-loaded with all apartment data, m², and building info. The new chairman gets access on day one, no setup needed.

**Why this works:**
- New KÜ has zero existing habits or tool loyalty
- Developer looks professional — modern digital handover
- Marketing angle for developer: "Smart building management included"
- Zero cost to developer — we give 6 months free, then KÜ pays at €0.30/apt/month
- For us: pre-loaded data, 100% adoption rate, zero CAC

**Who to approach (not construction companies — they build and leave):**
- **Property developers (arendajad):** Merko Ehitus, YIT Eesti, Bonava, Hepsor, Endover, Fund Ehitus, Pro Kapital, Lumi Capital — start with smaller ones first
- **Haldusfirmad handling new building handovers:** Kvatro, Stell, FORUS, Onest Haldus
- **Volume:** ~50-80 new KÜs formed per year in Estonia from new construction

**The pitch to developers:**
> "When you hand over the building, the new KÜ gets a ready-to-use management platform with all apartment data already loaded. Your buyers see a professional digital building from day one. Costs you nothing — we charge the KÜ €0.30/apartment/month after 6 months free."

**Condition:** Approach only after working MVP with real users and a live demo. A demo with real building data closes this deal — a PowerPoint doesn't.

### Channel 3: EKYL Partnership (Month 4+)
- 1,400 member KÜs — direct access to chairmen who already pay for membership
- Options: "recommended tool" status on website, demo at training seminars, member discount, affiliate revenue share (10-15%)
- Approach only after 5-10 real paying KÜs as proof

### Channel 4: Haldusfirmad Multi-Building Dashboard (Month 6+)
- Companies like Kvatro manage 22,000+ apartments — they need a different tool than a single KÜ
- Multi-building portfolio view, bulk communications, unified resident search across all buildings
- B2B pricing: €200-500/month per management company
- Korto is built per-KÜ — no proper multi-building management layer exists

---

## Revenue Scenarios

| Scenario | KÜs | Avg apartments | MRR | ARR |
|---|---|---|---|---|
| Year 1 (organic only) | 100 | 40 | €1,200 | €14,400 |
| Year 1 + 1 developer deal (10 buildings) | 200 | 40 | €2,400 | €28,800 |
| Year 2 (organic + 3 developer partners) | 500 | 40 | €6,000 | €72,000 |
| Year 3 + haldusfirma deals | 1,000 KÜs + 3 firms | — | €15,000+ | €180,000+ |

---

## Build Timeline

| Week | Deliverable |
|---|---|
| Week 1 | Auth, building setup wizard, resident directory, search, custom lists |
| Week 2 | Announcements with filters, email/SMS delivery, read receipts, archive |
| Week 3 | Interaction log, smart reply templates, AI auto-fill, delayed send, context panel |
| Week 4 | Meetings, kirjalik otsus voting, quorum calculation, protocol PDF generation |
| Week 5 | Documents, meter readings, maintenance calendar, dashboard, deploy |

---

## Phase 2 (Post-MVP)

- **Resident companion mobile app** (Expo/React Native): submit meter readings, view invoices, vote, read announcements, report issues. Chairman manages via web, residents use mobile.
- **Haldusfirma multi-building dashboard:** manage 50-200 buildings from one view
- **Hardware integrations:** barriers, electronic locks, gate remotes (Pavel's request)
- **Smart-ID / Mobile-ID integration** for legally binding digital protocol signatures

---

## Open Questions

- Sergei mentioned a competitor already testing in 2 KÜs — who is it?
- Smart-ID / Mobile-ID for protocol signatures — MVP or phase 2?
- GDPR: what personal data can we store about residents (ID codes, contact info)? Need legal clarity.
- Which developers to approach first — who has the most new buildings completing in 2026?
- Pavel's hardware integrations — which barrier/lock systems are most common in Estonian new buildings? What APIs exist?
- Should accounting integration (read-only Korto/Merit data) be in MVP or phase 2?
