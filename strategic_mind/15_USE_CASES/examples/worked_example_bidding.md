# Worked Example — Bidding on an EGP 5M New Cairo Residential Tower

> **Layer**: 15_USE_CASES/examples/
> **File**: worked_example_bidding
> **Subject**: A complete end-to-end walkthrough of the system's 7-step pipeline applied to a real Egyptian contractor bid decision — situation, first instinct, mind routing, hypothesis generation, analysis, recommendation, follow-up, post-decision audit.
> **User context**: Egyptian electrical contractor, halal-only, mid-stage (Stage 3 of the expansion arc — roughly EGP 9-12M annual revenue, 3-4 active projects, working capital EGP 800K-1.2M).
> **Provenance**: Synthesized 2026-09-10 from `09_BUSINESS/contracting/project_bidding.md`, `09_BUSINESS/contracting/pricing_methodology.md`, `09_BUSINESS/contracting/cash_flow_zero_capital.md`, `09_BUSINESS/contracting/client_psychology_egypt.md`, `00_META/multi_hypothesis_engine.md`, `00_META/confidence_scoring.md`, `00_META/self_audit_protocol.md`, and the minds of Guo Jia (`07_MINDS/guo_jia/`), Sima Yi (`07_MINDS/sima_yi/`), Cao Cao (`07_MINDS/cao_cao/`), Liu Bei (`07_MINDS/liu_bei/`).
> **Tier**: Tier 5 (worked example) drawing on Tier 3 (practitioner patterns) + Tier 4 (Egyptian regulatory context).
> **Date**: 2026-09-10

---

## Why this file exists

This file is the worked example the user studies when learning how the system processes a real bid decision. Bidding is the contractor's primary commercial act (see `09_BUSINESS/contracting/project_bidding.md`), and the bid decision is the highest-frequency high-stakes decision the contractor makes. A contractor who bids 15-20 times a year and wins 4-6 of those bids will, over a 5-year horizon, make 75-100 bid decisions and win 20-30. Each bid decision commits working capital, crew capacity, and management bandwidth for 6-18 months. The bid decision is the unit of strategic contracting.

This file exists so the user can see what the system does with a real bid question — not a textbook bid question, but the kind of bid question the user actually faces in October 2026 in New Cairo, with a real client, a real competitor set, and a real cash-flow constraint. The example is composite (anonymized from several real bid patterns) but every number, every competitor behavior, and every cash-flow assumption is realistic for the Egyptian market in 2026.

---

## The situation

It is the second week of October 2026. The user — an Egyptian electrical contractor at Stage 3 of the expansion arc — receives a tender invitation for the electrical works of a residential tower in New Cairo.

**Project facts**:

- **Client**: A mid-tier private developer (call them "Developer X"). Developer X has completed 3 mid-size residential projects in New Cairo and 6th of October City in the past 7 years. One of those projects (a 2023 launch in 6th of October) was delayed 14 months but completed. No project has been abandoned. Developer X is not a top-tier developer (Talaat Moustafa, Palm Hills, SODIC) but is a credible mid-tier player.
- **Project**: A 14-story residential tower, 90 units, on a 3,200 m² plot in New Cairo's 5th District (the western side, off Road 9). The tower is in the third construction phase (the structural shell is 60% complete; the developer's previous electrical contractor defaulted after 5 months over a payment dispute).
- **Scope**: Full electrical works — main distribution panels, rising mains, apartment metering, lighting, power, lightning protection, low-current (intercom, fire alarm, CCTV). The bid is a re-tender of the defaulted contractor's scope.
- **Value**: EGP 5.0M (the consultant's estimate; the previous contractor's contract was EGP 4.6M, so the consultant has adjusted upward by ~9% for inflation and scope additions).
- **Duration**: 10 months from notice to proceed. The developer wants to hand over units to buyers in Q2 2028, so the electrical works must complete by end-July 2027.
- **Payment terms**: 20% advance against bank guarantee, 65% progress (monthly certifies against executed work), 10% on completion and handover, 5% retention for 6 months after handover (released against the same bank guarantee).
- **Bid bond**: EGP 250K (5% of bid value), refundable on contract signature.
- **Performance bond**: EGP 500K (10% of contract value), held for the duration of the project plus the retention period.
- **Liquidated damages**: 0.1% of contract value per day of delay, capped at 10% of contract value.
- **Competitor set (likely)**: Three contractors — (a) a larger New Cairo contractor who bid and lost the original tender; (b) a 6th of October contractor with a relationship with the consultant; (c) a smaller contractor who is rumored to be desperate for work (his last project finished 4 months ago and his pipeline is empty).

**User's current state**:

- **Pipeline**: 3 active projects (a 6-month EGP 1.8M apartment building in Maadi at month 4, a 9-month EGP 2.4M villa compound in New Cairo at month 2, a 4-month EGP 900K office fit-out in Heliopolis at month 1).
- **Working capital**: EGP 1.0M liquid, plus EGP 350K due from the Maadi project at month 5 (next certify).
- **Crew**: 1 senior site engineer (committed 60% to the Maadi project, 40% to the villa compound), 2 junior engineers (split across the 3 projects), 14 electricians (full utilization, with 4 borrowed subcontractor crews available for short-term peaks).
- **Strategic position**: Stage 3 of the expansion arc — building the New Cairo private-developer client base as the foundation for the move into real estate development (Stage 5).

**The bid deadline**: 18 days from now (last week of October 2026). Bid preparation will take 10-12 days of the estimator's and the user's time.

---

## The user's first instinct (and the system's audit)

The user's first instinct, formed within 10 minutes of reading the tender: **"This is a 5M project from a credible developer — that's nearly 60% of my annual revenue. I have to bid. Let me start the technical proposal."**

This is the classic contractor's first instinct on a credible bid. It is also the instinct that has ruined contractors for 2000 years. The instinct treats the bid as an opportunity (correct, in the abstract) and skips the bid-decision discipline (incorrect, in the concrete).

**The system's audit of the first instinct** (the audit the system runs silently before responding):

1. **Anchoring bias**: The user has anchored on the EGP 5M number and on the developer's name. Both are salient. Neither is decision-relevant in isolation.
2. **Optimism bias**: "I have to bid" assumes the bid is winnable and that winning is good. Neither is verified.
3. **Sunk-cost framing**: The user has invested nothing in this bid yet, but the framing "I have to" suggests the bid is already a foregone conclusion. The system rejects the framing.
4. **Cash flow blindness**: The instinct does not consider the working capital cycle. EGP 5M with 20% advance means EGP 4M financed through progress payments over 10 months — with retention of 5% (EGP 250K) locked for 16 months. The user's working capital is EGP 1.0M. The math does not work without explicit cash-flow planning.
5. **Crew blindness**: The instinct does not consider whether the firm has a senior site engineer to dedicate to a 10-month, EGP 5M project. The current senior site engineer is 100% committed. The user would need to (a) pull him off Maadi or the villa (compromising those projects), (b) hire a new senior site engineer (3-4 months lead time, EGP 20-25K/month), or (c) run the project himself (which compromises his firm-wide management).
6. **Re-tender blindness**: The instinct does not consider that this is a re-tender of a defaulted contractor. The previous contractor defaulted over a payment dispute. The default tells the user something about the developer's payment behavior under stress. The instinct ignores the signal.
7. **Strategic-fit blindness**: The instinct does not check whether this project fits the firm's strategic direction (build a New Cairo private-developer client base as the foundation for real-estate development in Stage 5). It might fit; it might not. The instinct does not ask.

The system's response to the first instinct: **"Stop. Before you start the technical proposal, run the bid decision framework."** The system then walks the user through the seven-step pipeline.

---

## Mind routing — which minds apply, why

The system routes this question to four minds, in this order of priority:

### Mind 1: Guo Jia — rapid situation reading

**Why Guo Jia**: This is a time-bounded decision (18 days) with a competitor set the user must read fast. Guo Jia's discipline is to read the situation before the competitor reads it. The competitor who is "desperate for work" (the third competitor) is the competitor who will underprice. The competitor with the consultant relationship (the second) is the competitor who will score well on technical. The larger New Cairo competitor (the first) is the competitor who bid and lost last time and may have corrected his reading. Guo Jia reads all three.

**What Guo Jia sees**:
- The desperate competitor is the most likely winner on price, but the most likely to default. If the user bids at a fair price and the desperate competitor wins and defaults, the user gets the re-tender at a better price in 4-6 months. This is a real option, not a consolation.
- The consultant-relationship competitor is the technical-favorite. He will win on technical score but lose on price if his margin expectation is high. The user's path to beating him is to be close on technical (within 5 points) and meaningfully better on price (8-12% lower).
- The larger competitor who lost the original tender has the most information. He bid EGP 4.6M last time and lost to the defaulting contractor (who presumably bid lower). He knows the consultant, the developer, and the project. He is the most dangerous competitor — not because of price, but because of information. The user should consider whether to bid at all if this competitor's reading is "I want this one."

### Mind 2: Sima Yi — long-game patience

**Why Sima Yi**: This is a strategic-fit question, not a tactical-bid question. The user is at Stage 3 of the expansion arc. The strategic objective is to build a 3-project relationship with a New Cairo private developer, not to win a single EGP 5M bid. Sima Yi asks: "Is this developer the right developer to build the relationship with?"

**What Sima Yi sees**:
- The developer is mid-tier with one delayed project and no abandoned projects. The 14-month delay is a yellow flag, not a red flag. The defaulting contractor's payment dispute is a red flag worth investigating — was the dispute the developer's fault (slow payment, scope changes, variations refused) or the contractor's fault (overcommitted, under-resourced, walked off)?
- The strategic value of this bid is not the EGP 5M. The strategic value is the relationship: if this bid succeeds and the user delivers well, the developer may invite the user to bid on his next 2-3 projects directly (negotiated, not tendered). That path is worth EGP 15-25M of revenue over 4 years. The bid is an audition.
- The strategic risk: if the user bids, wins, and the developer's payment behavior under stress is poor (the re-tender signal), the user may be the next defaulting contractor. Sima Yi demands the pre-bid investigation include a specific check on the previous contractor's default cause.

### Mind 3: Cao Cao — multi-stakeholder integration

**Why Cao Cao**: This bid involves the developer, the consultant, the three competitors, the user's existing clients (whose projects may be compromised if the user wins), the user's crew (whose capacity is the binding constraint), the user's bank guarantee provider (the bid bond and performance bond tie up EGP 500K-750K of credit for 16 months), and the user's family (the bid commits working capital that affects family reserves). Cao Cao integrates all stakeholders.

**What Cao Cao sees**:
- The crew constraint is the most binding. The user cannot run 4 active projects with 1 senior site engineer. Winning this bid requires hiring a second senior site engineer. The decision is not "bid / not bid" — it is "bid AND hire" or "not bid." The bid and the hire are a coupled decision.
- The bank guarantee constraint is the second binding. The bid bond (EGP 250K) and the performance bond (EGP 500K) tie up EGP 750K of bank credit. The user's current bank credit line is EGP 1.5M (the standard limit for a contractor of his classification). The user already has EGP 600K of credit committed to the villa compound's performance bond. The user has EGP 900K of credit remaining. The bid would consume 83% of remaining credit. This leaves no room for another bid for 10 months.
- The existing-client constraint is the third binding. If the user pulls his senior site engineer off Maadi (month 4 of 6), the Maadi project slips. If the user pulls him off the villa compound (month 2 of 9), the villa project slips. The relationship cost of slipping either is real.

### Mind 4: Liu Bei — relationship and reputation

**Why Liu Bei**: The bid is an audition (per Sima Yi). The audition is for a 3-project relationship. Liu Bei's question: "What does the user's behavior in this bid signal to the developer about the user as a long-term partner?"

**What Liu Bei sees**:
- A bid that is technically excellent and commercially reasonable signals a serious partner. A bid that is technically careless or commercially aggressive signals a transactional contractor. The user should bid in a way that signals long-term intent: the technical proposal should be detailed, the program should be realistic, the materials should be specified by brand and quality, and the commercial proposal should be priced at a fair margin (12-15%), not at a win-at-all-costs margin (5-8%).
- The bid process itself is a relationship signal. If the user attends the pre-bid site visit, asks informed questions, follows up with the consultant on technical clarifications, and submits early (not in the last hour), the user signals the kind of partner who will communicate well during the project. If the user submits late with sloppy clarifications, the user signals the kind of partner who will be hard to reach during the project.
- The user's reputation in the market is also at stake. Three competitors will see the user bid (or not bid). If the user bids and wins at a fair price, the user's market reputation as a credible mid-tier competitor strengthens. If the user bids and wins at an aggressive price (5-8%), the user trains competitors to underprice next time.

---

## Hypothesis generation — 4 hypotheses

Per `00_META/multi_hypothesis_engine.md`, the system generates 4 hypotheses before settling on a recommendation. Each hypothesis comes from a different mind and must be distinct.

### Hypothesis 1 (from Guo Jia): "Bid aggressively, win, and execute"

**The hypothesis**: Bid at a 10-12% margin (competitive), win on a combination of technical strength and acceptable price, dedicate a newly-hired second senior site engineer to the project, finance the cash-flow gap with the 20% advance plus supplier credit on materials, and use the win to establish the developer relationship.

**Assumptions**:
- The user can hire a senior site engineer in 6-8 weeks (the lead time for the hire is shorter than the bid-to-mobilization window).
- The developer's payment behavior under stress is acceptable (assumed; not verified).
- The user can secure the bid bond and performance bond without breaching his bank credit limit.
- The 20% advance plus 65% progress covers the working capital cycle (assumed; not modeled).

**Failure modes**:
- The hire fails (no suitable candidate found in 6-8 weeks) → the user must run the project himself, compromising the firm.
- The developer pays slowly under stress → the user becomes the next defaulting contractor.
- The bid loses → the user has spent 12 days of estimator time and EGP 250K of bid bond for nothing.

### Hypothesis 2 (from Sima Yi): "Decline this bid, bid on the developer's next project directly (negotiated)"

**The hypothesis**: Decline this bid (the re-tender risk is too high, the crew constraint too binding), but use the decline to position for a negotiated bid on the developer's next project. The decline is not a no — it is a "we cannot give this bid the attention it deserves given our current commitments; we would welcome a direct conversation about your next project."

**Assumptions**:
- The developer has a next project in the pipeline (the user has not verified this).
- The developer will respect a contractor who declines with a stated reason (this is the Liu Bei assumption — heart-based legitimacy).
- The user's current pipeline can be executed without taking this bid (the user is not financially desperate).
- The next project will be negotiable rather than tendered (assumed; not verified).

**Failure modes**:
- The developer's next project is 18-24 months away (too long for the strategic arc).
- The developer takes the decline as a rejection and does not invite the user to the next project.
- The user's pipeline has a gap in 6-9 months (the Maadi project finishes at month 6, the office fit-out at month 4) and the user has nothing to fill it.

### Hypothesis 3 (from Cao Cao): "Bid at a 16-18% margin with a re-tender risk premium, and walk if the bid loses"

**The hypothesis**: Bid, but at a 16-18% margin (not the competitive 10-12%), justified by the re-tender risk (the previous contractor defaulted over payment), the crew overload (the user is paying a premium to hire), and the bank credit consumption (the user is paying an opportunity cost on the credit line). If the bid loses (likely, given the desperate competitor will underprice), the user has spent 12 days and EGP 250K to gather market intelligence — the developer's response to the user's price tells the user something about the developer's price sensitivity for the next negotiation.

**Assumptions**:
- The 16-18% margin is defensible to the consultant on the basis of risk (the re-tender default, the liquidated damages cap of 10%).
- The user can absorb the EGP 250K bid bond for 60-90 days without cash-flow pain.
- The user values the market intelligence from the loss more than the bid cost.
- The user has a credible story for the higher margin (the re-tender risk premium).

**Failure modes**:
- The bid loses by a wide margin (the user's price is 25%+ above the winner) — the user learns nothing about the developer's price sensitivity (the price was non-competitive, not informative).
- The bid wins at 16-18% — the user has committed to a project at a margin that, while high, requires the crew, the bank credit, and the cash-flow management to execute. The high margin does not eliminate the execution risk.

### Hypothesis 4 (from Liu Bei): "Bid at a 13-14% margin with a relationship-building technical proposal, accept the higher risk of losing, and use the bid as a relationship audition regardless of outcome"

**The hypothesis**: Bid at a 13-14% margin (a fair margin that respects the user's costs and the developer's price sensitivity), invest 60% of the bid preparation time in the technical proposal (the detailed method statement, the program, the materials specification, the project team CVs), attend the pre-bid visit, ask informed questions, submit early, and follow up with the consultant. The bid is an audition for the relationship; winning is a bonus.

**Assumptions**:
- The user has the 10-12 days of preparation time available (the user's existing projects can absorb the time cost).
- The technical proposal quality will be visible to the consultant and the developer (the consultant's technical scoring is rigorous; not assumed).
- The user can hire a second senior site engineer in time to execute if the bid wins (same as Hypothesis 1's assumption).

**Failure modes**:
- The bid loses on price (the desperate competitor underbids) — the user has spent the time and the bid bond, with no revenue outcome. The relationship value of the bid process depends on the developer's perception of the user's professionalism, which is not guaranteed.
- The bid wins — the user has the same execution risk as Hypothesis 1, but at a 13-14% margin instead of a 10-12% margin. The execution risk is unchanged; the margin is slightly more comfortable.

---

## The analysis (per 03_ANALYSIS)

The system applies `03_ANALYSIS/power_dynamics.md`, `03_ANALYSIS/interests_behind_positions.md`, and `03_ANALYSIS/leverage_detection.md` to the four hypotheses.

### Power dynamics

The developer has more power than the user. The developer has the project, the capital, and the choice of contractor. The user has the labor and the bid. In a re-tender, the developer's power is reduced (the previous contractor defaulted; the developer is under time pressure to deliver by Q2 2028). The user's power is enhanced by the re-tender situation, but only if the user is one of 2-3 credible bidders (which he is).

The consultant has power disproportionate to his commercial stake. The consultant's technical scoring can disqualify the user before price is considered. The consultant's relationship with the second competitor is a power asymmetry the user must offset with technical quality.

### Interests behind positions

The developer's stated position: "We want a quality contractor at a fair price, on the original schedule." The developer's interest: deliver the units by Q2 2028, avoid another default, preserve reputation with buyers. The interest behind the position is the schedule risk — the developer is more time-sensitive than price-sensitive. This favors Hypothesis 4 (the user who signals reliability and schedule discipline) over Hypothesis 1 (the user who signals aggressive price).

The consultant's stated position: "We will evaluate technically and commercially per the standard scoring." The consultant's interest: protect his reputation with the developer, avoid recommending another defaulting contractor, favor a contractor he knows (the second competitor). The interest behind the position is reputational self-protection. This favors Hypothesis 4 (the user who invests in the technical proposal and the consultant relationship) over Hypothesis 1.

The competitors' positions: bid to win. Their interests: the desperate competitor needs cash flow; the consultant-relationship competitor needs the margin; the larger competitor needs the strategic New Cairo presence. The desperate competitor's interest makes him the most aggressive on price and the most likely to default again — which would trigger another re-tender in 4-6 months.

### Leverage detection

The user's leverage points:
- The user's New Cairo presence (one project already in New Cairo, in the same district as the bid project — a proximity advantage for site supervision and consultant access).
- The user's Stage 3 strategic position (the user is building a developer-relationship base; this developer is exactly the kind of mid-tier private developer the user needs).
- The user's halal constraint as a positioning asset (the user can credibly commit to no short-cuts on materials substitution, which the developer will value after a default).
- The re-tender context (the user can position as the reliable alternative to the defaulting contractor, not as the cheapest option).

The user's leverage gaps:
- The user has no prior relationship with this consultant (the second competitor does).
- The user has no prior relationship with this developer (no incumbent advantage).
- The user has no capacity headroom (the user must hire to execute — this is a negotiation weakness if the developer senses it).

---

## The recommendation (with confidence level, with counter-evidence)

**Recommendation: Hypothesis 4 — bid at a 13-14% margin, with a relationship-building technical proposal, accept the higher risk of losing, and treat the bid as a relationship audition regardless of outcome.**

**Confidence: MEDIUM (5 of 12 on the `00_META/confidence_scoring.md` scale).**

**Why MEDIUM, not HIGH**:
- The premise verification is incomplete (the previous contractor's default cause has not been verified; the developer's next-project pipeline has not been verified).
- The competitor analysis is based on inference, not direct intelligence.
- The user's hiring lead time is an assumption, not a verified market fact.

**Why MEDIUM, not LOW**:
- The structure of the recommendation (bid with a relationship emphasis, accept the loss as a positive outcome) is robust to most unknowns. If the default cause was the contractor's fault, the re-tender risk is low and the user's bid is safer. If the default cause was the developer's fault, the relationship-audition value of the bid is even higher (the user demonstrates professionalism to a developer who needs to see it). The recommendation is robust in both cases.
- The strategic fit is verified — the developer is the kind of mid-tier New Cairo private developer the user's Stage 3 expansion requires.

**Counter-evidence (the case against the recommendation)**:
- If the user's working capital is more constrained than stated (the user has under-reported family reserves committed), the EGP 250K bid bond is a non-trivial commitment for a probable loss. The recommendation should be downgraded to "decline" if the working capital is below EGP 800K.
- If the user's senior site engineer is more committed than stated (the Maadi project is in a critical phase at month 4-5), the user cannot spare the time to lead the technical proposal. The recommendation should be downgraded to "bid at a thinner technical level, accept lower technical score" — which weakens the relationship-audition value.
- If the user has a credible alternative bid opportunity in the next 30 days (a direct invitation from a developer with whom the user already has a relationship), the user should not consume the bank credit on this bid. The recommendation should be downgraded to "decline" in favor of the alternative.

**The conditional path**:

- **Pre-bid investigation (days 1-3)**: Verify the previous contractor's default cause via the Federation of Contractors' informal channel. If the default cause is the developer's payment behavior under stress, downgrade the recommendation to "decline with a relationship-preserving message." If the default cause is the contractor's overcommitment, proceed.
- **Hiring check (days 1-5)**: Identify 2-3 senior site engineer candidates via the user's network. If no credible candidate emerges in 5 days, downgrade to "decline" — the execution risk is too high.
- **Bid preparation (days 6-15)**: Invest 60% of preparation time in the technical proposal, 40% in the commercial. Attend the pre-bid visit. Ask 3-4 informed questions. Submit on day 14 (not day 18).
- **Bid submission (day 18)**: Submit at a 13-14% margin with a detailed technical proposal, a realistic program, brand-specified materials, and a project team CV that signals competence.
- **Post-bid (day 19 onward)**: If the bid wins, execute. If the bid loses, follow up with the consultant — "we'd welcome feedback on our bid; we'd like to be considered for the next project." This is the relationship-audition follow-through that converts a loss into a future win.

---

## The follow-up — what to monitor, what to do if conditions change

The recommendation does not end with the bid submission. The follow-up is a structured monitoring plan.

### If the bid wins

- **Week 1**: Mobilize the new senior site engineer. Confirm the bank guarantee. Begin the project.
- **Month 1-3**: Monitor the developer's payment cycle against the contract. If the first progress payment is more than 15 days late, escalate formally (written notice, copy the consultant). If the second progress payment is more than 30 days late, the user is in the early-warning pattern of the previous defaulting contractor — initiate a frank conversation with the developer about payment schedule, before the working capital gap becomes critical.
- **Month 4-6**: Monitor the consultant's variation order pattern. If the consultant is issuing variations that increase scope without price adjustment, the user is being softened for a margin squeeze. Document every variation, price every variation, and submit variation orders weekly (not at the end).
- **Month 7-9**: Monitor the developer's handover schedule. If the developer is pushing for early handover to capture buyer payments, the user is being pressured to compress the final commissioning phase. Hold the schedule; do not compress safety or testing.
- **Month 10**: Complete. Hand over. Submit the close-out documentation. Begin the 6-month retention period.
- **Month 16**: Release the retention. If the developer is late releasing the retention (a common pattern), follow up weekly, not monthly.

### If the bid loses

- **Day 21-30**: Request a debrief from the consultant. The consultant may or may not provide one (private developers are not obligated). If a debrief is provided, listen for the technical score (was the technical proposal competitive?) and the commercial gap (was the price close or far?). Do not argue the decision.
- **Month 1-3**: Follow up with the developer directly (via the user's contact, if any). The message: "We appreciate the opportunity to bid. We would welcome a direct conversation about your next project." Do not request a second chance on this project.
- **Month 3-12**: Monitor the developer's next project pipeline. If the developer launches a new project in 6-12 months, request a direct invitation to bid (negotiated, not tendered). The audition has value only if the user uses the audition.

### If conditions change

- **If the user's working capital drops below EGP 800K before bid submission**: Withdraw the bid. The execution risk exceeds the strategic value.
- **If the user's senior site engineer resigns before bid submission**: Withdraw the bid. The hiring lead time becomes the project's critical path.
- **If the developer changes the payment terms before bid submission (e.g., reduces the advance from 20% to 10%)**: Re-evaluate the working capital cycle. The 10% advance increases the user's financing burden by EGP 500K for 5-6 months. If the user cannot finance this, withdraw.
- **If the bid bond requirement increases before submission (e.g., from 5% to 10%)**: Re-evaluate. The increased bid bond consumes EGP 500K of bank credit, leaving EGP 400K for the next 10 months.

---

## The post-decision audit — what went right, what went wrong

The post-decision audit runs at 3 points: at bid submission (the decision audit), at bid outcome (the result audit), and at project completion (the execution audit). This section describes the audit framework the user runs at each point.

### The decision audit (at bid submission, day 18)

The user, after submitting the bid, runs a self-audit on the decision process:

1. **Did the system apply the bid decision framework's six filters?** Yes — strategic fit (verified), capacity fit (verified, contingent on hire), financial fit (verified, contingent on bank credit), competitive fit (verified), risk fit (verified, contingent on default-cause investigation), pipeline fit (verified).
2. **Did the user anchor on the first instinct?** No — the user's first instinct was "I have to bid." The system's audit rejected the instinct and walked through the framework.
3. **Did the user generate multiple hypotheses?** Yes — four hypotheses from four minds.
4. **Did the user verify the premises?** Partially — the default cause was investigated; the hire lead time was checked. The developer's next-project pipeline was not verified (the user did not have access). This is the gap.
5. **Did the user push back on the system's recommendation?** The user should: "Is 13-14% really the right margin? Why not 12% to be more competitive?" The system's response: 12% erodes the re-tender risk premium; 14% preserves it. The user can verify the margin by modeling the cash flow at 12% vs 14% — if 12% leaves the user no working capital buffer for a 30-day payment delay, 12% is too thin.
6. **Did the user ask the meta-question?** The user should ask: "What should I be asking that I am not?" The system's likely response: "The user has not asked about the developer's relationship with the buyer payment schedule — if the developer's buyers are paying in installments that track construction milestones, the developer's cash flow is more predictable, and the user's payment risk is lower. The user should ask the developer (or the consultant) about the buyer payment schedule."

### The result audit (at bid outcome, day 30-45)

If the bid wins:
- The user has a project to execute. The audit shifts from decision quality to execution quality. The first execution audit runs at month 1 (mobilization complete? hire complete? first payment received?).

If the bid loses:
- The user has spent 12 days and EGP 250K of bid bond for 60-90 days. The audit question: "Was the loss informative?" The loss is informative if the user learned the developer's price sensitivity, the consultant's technical scoring threshold, or the competitor's bidding pattern. The loss is uninformative if the user's price was non-competitive (a wide gap) and the technical proposal was not scored. The user should request the debrief precisely to make the loss informative.

### The execution audit (at project completion, month 10)

The execution audit runs against the original recommendation. The audit questions:

1. **Did the user's hypothesis (relationship audition) play out?** Did the developer behave as a long-term prospect (early discussions of the next project, prompt payment through the project, professional consultant interaction) or as a transactional client (no next-project discussion, payment delays, scope-creep pressure)?
2. **Did the margin hold?** The 13-14% margin was the budget. Did the actual margin hold at 12%+ (acceptable) or compress to 8-10% (warning) or below 8% (failure)?
3. **Did the hire work?** The second senior site engineer — was the hire successful, was the engineer productive, was the engineer retained post-project? A good hire at the senior site engineer level is a long-term asset; a bad hire is a project-long drag.
4. **Did the user's strategic position improve?** The bid was an audition for the Stage 3 → Stage 4 transition. Did the user exit the project with a stronger New Cairo private-developer client base, or with the same client base plus one project of revenue?

The execution audit's output is a set of calibrated learnings that update the user's bid decision framework for the next bid. The system incorporates the learnings into the user's personal pattern file (the system's self-evolving layer).

---

## Closing note

This worked example is one bid. The user will face 15-20 similar bids in the next 12 months. The discipline that this example teaches — stop the first instinct, route to the right minds, generate multiple hypotheses, audit the premises, recommend with confidence and counter-evidence, monitor the follow-up, audit the result — is the discipline that turns 15-20 bids into a coherent strategic arc rather than a series of disconnected commercial events. The bid is the unit of strategic contracting. The user who masters the bid unit masters the contracting business.

---

## File History

- Created: 2026-09-10
- Version: 1.0
- Review: 2027-03-10
