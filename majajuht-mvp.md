# Majajuht — KÜ Management Tool MVP

## What It Is

A lightweight resident CRM for KÜ (korteriühistu) chairmen. Replaces WhatsApp, Excel, and paper notices in the stairwell. Designed for volunteer chairmen who do this work for free and need to spend less time on it.

## Target Market

- ~10,000-16,000 apartment associations in Estonia
- Primary user: volunteer chairman / board member
- Most buildings: 20-60 apartments, Soviet-era blocks
- 97% home ownership rate in Estonia
- Existing tools (Korto, Ühekatuseall, Digimaja, Profit KÜ) are all accounting-first and outdated

## Pricing Model

- €0.30/apartment/month
- 40-apartment building = €12/month (paid from KÜ budget, not chairman's pocket)
- 3-month free trial
- Revenue target: 500 KÜs x 40 avg apartments x €0.30 = €6,000/month = €72K/year

## Tech Stack

- Next.js (frontend + API)
- PostgreSQL (Supabase or Neon)
- Auth: email magic link (no passwords — simplest for non-technical users)
- SMS: Messente API (Estonian provider, ~€0.03/SMS)
- Email: Resend or Postmark
- Hosting: Vercel
- Languages: Estonian + Russian from day 1
- Running cost: under €30/month until 50+ paying KÜs

---

## Feature Priority (Based on Real Chairman Feedback)

### Priority 1: Resident CRM with Instant Lookup

The core of the product. Every resident has a card with full context.

**Resident card contains:**
- Name, apartment number, m², ownership share %
- Phone, email, preferred contact method
- Payment status (paid / debtor / months behind)
- Full interaction history (every message sent/received, every complaint, every request with dates)
- Chairman's private notes (e.g., "always complains about parking", "agreed to pay by March")
- Quick actions: send SMS, send email from template, mark as debtor

**Search by:** name, apartment number, phone, car plate number

**Custom linked lists (flexible data per building):**
- Core: Apartments <-> Residents (always there, standard)
- Vehicles: plate number, make, color -> linked to resident
- MVP allows 1-2 additional custom lists chairman can create:
  - Storage rooms -> linked to apartment
  - Electronic keys -> linked to resident
  - Gate remote IDs -> linked to resident
  - Parking spots -> linked to apartment
  - Whatever this specific building needs

**Lookup flow:**
See a car plate -> search -> instantly see: owner, apartment, phone, debts, last complaints, one click to call or SMS. No digging through separate Excel files.

**Why:** Pavel Zujev's detailed feedback. Currently everything is in separate Excel files. Every resident interaction requires manually searching through multiple spreadsheets.

### Priority 2: Interaction History Per Resident

Every message, email, call note, complaint — logged with timestamp under the resident's card.

**Why:** Константин Иванов's point — "your phone answer can't be attached to a case. There's a question, give an answer, and it's documented." Also helps with "difficult residents" — harder to argue when chairman can say "I answered you on March 14 at 11:23."

### Priority 3: Smart Reply with Data Auto-Fill

Chairman's knowledge base — not a FAQ for residents, but a tool to help the chairman answer faster.

**How it works:**
- Chairman answers a question once about tariffs, repair fund, rules
- System saves it as a reusable reply
- Next time someone asks the same thing — 2 clicks to send the same answer, but with THIS resident's apartment data auto-filled
- Auto-fill variables: resident name, apartment number, m², current tariff, calculated amount (price x m²), previous amount, difference, date of last change
- Optional: attach relevant law citations or charter quotes

**Delayed send feature:**
- Chairman quickly drafts reply from templates
- Sets delay (e.g., send at 21:00)
- Resident thinks it was carefully considered after hours of research
- Psychological hack, costs nothing to build

**Why:** Pavel's idea. Galina's pain with endless repetitive questions. Key insight from Pavel: residents won't self-serve or read FAQs — the tool should help the chairman respond faster, not redirect residents.

### Priority 4: Filtered Mass Messaging (Announcements)

Replace the paper notice on the stairwell wall.

**Features:**
- Create announcement -> choose recipients by filter:
  - All residents
  - Specific stairwell / entrance
  - Specific floor
  - By apartment size (e.g., only 2-room apartments)
  - By custom criteria
- Auto-fill per resident: name, apartment data, calculated amounts
- Example: "Repair fund changes: [price] x [your m²] = [total]. Was: [old amount]. Difference: [+/-]"
- Delivery: email + in-app notification
- Read receipts — chairman sees who opened it, who didn't
- For those who didn't read: one-click "resend" or "send as SMS" fallback
- Announcement archive — resident can never say "I didn't know"

**Why:** Galina Medvedovskaja, Igor Matskevits. Universal need confirmed by multiple chairmen.

### Priority 5: Meeting Invitations + Reminders + Protocol Generation

**Before the meeting:**
- Chairman creates agenda items in the system
- Each item has a type: informational / vote required / election
- For vote items: chairman pre-fills the motion (e.g., "Raise repair fund from €0.40 to €0.50 per m²")
- Invitations go out automatically with agenda
- Reminder 24h before (email + SMS)

**During the meeting (minimal input):**
- Attendance: check off who showed up -> auto-calculate quorum (based on m² shares)
- Per agenda item: tap For / Against / Abstained counts
- Optional: one text field for key discussion notes

**After the meeting:**
- System auto-generates protocol PDF:
  - Date, location, start/end time
  - Attendee list with apartment numbers and m²
  - Quorum confirmation
  - Each agenda item -> discussion summary -> vote result -> decision
  - Signature lines
- Chairman reviews, edits if needed, exports PDF
- Sends to all residents via announcement system

**Written decision procedure (kirjalik otsus) — the real MVP win:**
- Chairman creates proposal + deadline (e.g., 14 days)
- System sends to all residents via email
- Resident clicks: For / Against / Abstain
- System tracks votes, calculates m²-weighted results in real time
- Deadline passes -> result auto-calculated -> protocol auto-generated
- Zero meeting, zero physical presence, fully legal under Estonian law (2023 amendments)

**Why:** Igor, Анатолий Евгеньевич, Galina ("general meetings are coming!"). Note: Korto already has basic voting — this needs to be better integrated into the full workflow, not a standalone feature.

### Priority 6: Document Storage

Simple but critical:
- Upload and categorize: protocols, contracts, annual reports, building plans, charter
- When chairman changes -> everything stays in the system, nothing lost
- Residents can view (read-only) relevant documents
- Solves the handover problem — new chairman gets full history on day 1

### Priority 7: Maintenance Calendar

- Recurring reminders: fire extinguisher check, elevator inspection, insurance renewal, cleaning contract end date
- Log completed work with photos/notes
- Simple contractor contacts list

---

## What Is NOT in MVP

- No accounting/bookkeeping (let Merit/Korto handle that)
- No hardware integration for barriers/locks (phase 2 — Pavel's request)
- No mobile app (responsive web first, app later)
- No payment processing (chairman uses existing invoicing tools)
- No resident self-service portal (based on Pavel's feedback: residents won't use it)

---

## Key Product Insights from User Research

1. **This is a CRM, not an accounting tool.** Every competitor is accounting-first. The gap is management-first.
2. **Residents won't self-serve.** Don't build FAQ pages or knowledge bases for residents. Build tools that help the chairman answer faster.
3. **Every KÜ is different.** Flexible custom lists (linked to apartment/resident) are essential. Rigid fixed fields will always miss something.
4. **Written record is power.** Documentation of every interaction protects the chairman legally and shuts down "I didn't know" arguments.
5. **Elderly residents are a reality.** SMS fallback and the option to print are necessary. But the tool's primary value is freeing chairman's time WITH digital-capable residents so they have time for face-to-face with the elderly.
6. **The chairman is the buyer AND the sales force.** If the tool makes their life easier, they will push the general meeting to approve the expense.

---

## Competitive Landscape

| Tool | Price | Focus | Weakness |
|---|---|---|---|
| Korto.ee | ~€0.10-0.30/apt/month | Accounting + resident portal | Legacy UI (since 2005), accounting-first |
| Ühekatuseall | €0.20/apt/month (full) | Accounting + management | Complex, overwhelming for non-technical chairmen |
| Digimaja | Quote-based | Accounting for haldusfirmad | Targets management companies, not individual KÜs |
| Profit KÜ | License-based | Desktop accounting | Desktop software, database corruption issues, ancient tech |
| Merit KÜ | Part of Merit | Accounting with KÜ bolt-on | Accounting tool first, KÜ features are secondary |

**Our differentiator:** Management-first, not accounting-first. Resident CRM with context. Designed for a non-technical volunteer, not an accountant.

---

## Build Timeline

| Week | Deliverable |
|---|---|
| Week 1 | Auth, resident database (CRUD), resident cards, search, custom lists |
| Week 2 | Announcements with filters, read receipts, email/SMS sending |
| Week 3 | Smart replies with auto-fill, interaction history logging |
| Week 4 | Meetings: create, invite, vote (kirjalik otsus), protocol generation |
| Week 5 | Documents, maintenance calendar, dashboard, Polish UI, deploy |

---

## Go-to-Market

1. **Pavel Zujev** — first beta tester, already engaged, has programming background, manages his own KÜ + works with KÜs professionally (electronic locks/barriers)
2. **Facebook group** — active thread with engaged chairmen, post development updates there
3. **Sergei Nikonov's warning** — this is the 3rd-4th attempt at such a tool. A competitor is already testing in 2 KÜs. Speed matters.
4. **EKYL partnership (month 3-4)** — 1,400 member KÜs. Approach once we have 5-10 real users. Options: "recommended tool" status, demo at training seminars, member discount, or affiliate revenue share.

---

## Open Questions

- Sergei mentioned a competitor already testing in 2 KÜs — who is it? What are they building?
- Smart-ID / Mobile-ID integration for meeting protocols — needed for MVP or phase 2?
- Integration with existing accounting tools (Korto, Merit) — API available?
- GDPR considerations for storing resident personal data
- Pavel's hardware integration (locks, barriers) — which systems are most common in Estonia? What APIs exist?
