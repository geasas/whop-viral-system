# Strategic Pricing for Egyptian Electrical Contractors — The Methodology

> **Layer**: 09_BUSINESS/contracting/
> **File**: pricing_methodology
> **Subject**: Strategic pricing methodology — cost-plus vs value-based vs competitive pricing; the Egyptian price formula; material, labor, overhead estimation; margin norms; loss-leader strategy; bid-negotiation dynamic; scope change handling
> **Tier**: Knowledge file (Tier 4 cost data + Tier 3 practitioner + Tier 2 strategy)
> **Date**: 2026-09-09
> **Provenance**: Synthesized from Egyptian Federation of Contractors pricing guidelines, manufacturer price lists (Schneider, Elsewedy, ABB, Siemens, Legrand, Nexans, Prysmian, 2025-2026), London Metal Exchange copper and aluminum data, practitioner interviews with senior estimators and contractors in Cairo, and classical/strategic pricing theory (Drucker, Porter, Nagle). Cross-referenced with `egypt_electrical_market.md`, `electrical_fundamentals.md`, and `project_bidding.md`.

---

## Why this file exists

The contractor who prices right survives and grows. The contractor who prices wrong dies slowly — winning bids he cannot deliver, losing bids he should win, accepting margins that erode his capital base, chasing volume that does not produce profit. The Egyptian electrical market in 2026 has specific pricing conventions, specific cash-flow patterns, and specific competitive dynamics that determine which pricing methodology works in which situation. This file is the methodology: how to calculate a price that is competitive, profitable, and durable.

---

## The core principle

The Egyptian electrical contractor's price is built bottom-up from material cost + labor cost + overhead + risk loading + profit margin. The market price is set top-down by competition and by the client's budget. The contractor's pricing discipline is to know both — to build the bottom-up price accurately and to compare it to the top-down market price — and to bid only when the two prices are compatible. When the bottom-up price is above the market price, the contractor either declines the bid, finds a way to lower the bottom-up (substitution, productivity, scope adjustment), or accepts the loss as a strategic investment. When the bottom-up price is below the market price, the contractor bids at the market price and earns the spread. The pricing discipline is the discipline of knowing both numbers, every bid, every time.

---

## The Principles

### Principle 1: Three Pricing Methodologies — Cost-Plus, Value-Based, Competitive — and When Each Applies

The three pricing methodologies are not interchangeable; each is correct in a specific context and wrong in others.

**Cost-plus pricing:** the contractor calculates the direct cost (material + labor) plus the indirect cost (overhead allocation) plus a fixed margin percentage. The methodology is transparent, defensible, and easy to audit. It is correct when:
- The work is well-defined (no scope ambiguity).
- The client is sophisticated and will audit the cost (government, large developer).
- The relationship is long-term and the contractor wants to build trust through transparency.
- The contract is cost-plus with a fee (rare in Egypt, but used in some emergency work and some government infrastructure).

Cost-plus is wrong when the work is undefined (the contractor absorbs the scope risk) or when the market price is well below the cost-plus (the contractor is uncompetitive).

**Value-based pricing:** the contractor prices based on the value the work delivers to the client, not on the cost of producing it. The methodology is correct when:
- The contractor delivers a unique value (specialized skill, proprietary method, brand premium).
- The client measures value, not cost (the high-end private client, the international developer).
- The work has a measurable return (the data center electrical that prevents downtime, the generator that prevents business interruption, the MT switchgear that prevents a fault).

Value-based is wrong when the client is price-shopping (most residential, most government open tender), when the value cannot be quantified (most lighting and finish work), or when the competition is on price (commoditized work).

**Competitive pricing:** the contractor prices at or just below the expected competitor price. The methodology is correct when:
- The work is commoditized (residential, standard commercial, government tender).
- The contractor has no differentiated value (the early-stage contractor, the contractor entering a new segment).
- The bid is a market test (the contractor is measuring the market, not maximizing margin).

Competitive pricing is wrong when it ignores the bottom-up cost (the contractor wins the bid and loses money) or when it leaves margin on the table (the contractor could have priced higher and still won).

**The strategic discipline is to use all three methodologies in the right mix.** The contractor uses cost-plus for the long-term relationship work where transparency is the asset; value-based for the differentiated work where the value is measurable; competitive for the entry work where the goal is to win the bid and build the relationship. The contractor who uses one methodology for all work is over-pricing some work and under-pricing the rest.

[Nagle, *The Strategy and Tactics of Pricing*, 1987 — Tier 2; Porter, *Competitive Strategy*, 1980 — Tier 2; practitioner interviews — Tier 3]

### Principle 2: The Egyptian Price Formula — How Egyptian Contractors Typically Calculate Bids

The typical Egyptian electrical contractor's bid is built as follows (illustrative for a 10 million EGP residential project, 2026):

**Step 1 — Material takeoff (direct material):**
- Cable (LV power, lighting, control): 2,800,000 EGP
- Distribution boards (LV panels, breakers): 1,500,000 EGP
- Conduit and fittings (PVC, MT if applicable): 600,000 EGP
- Lighting fixtures: 1,200,000 EGP
- Socket outlets, switches, finishing: 700,000 EGP
- Earthing and lightning protection: 250,000 EGP
- Test and commissioning equipment (consumables): 50,000 EGP
- **Material subtotal: 7,100,000 EGP**

**Step 2 — Labor takeoff (direct labor):**
- Skilled electricians: 1,200 hours × 800 EGP/hr = 960,000 EGP
- Semi-skilled: 1,800 hours × 450 EGP/hr = 810,000 EGP
- Laborers: 2,500 hours × 300 EGP/hr = 750,000 EGP
- Foreman allowance: 200,000 EGP
- **Labor subtotal: 2,720,000 EGP**

**Step 3 — Subcontractor cost (where applicable):**
- PVC conduit sub-subcontractor: 350,000 EGP
- Cable pulling sub-subcontractor: 280,000 EGP
- Lighting fixture installation sub: 150,000 EGP
- **Subcontractor subtotal: 780,000 EGP**

**Step 4 — Direct cost subtotal:** 7,100,000 + 2,720,000 + 780,000 = **10,600,000 EGP**

**Step 5 — Site overhead (5-8% of direct cost):**
- Site office, supervision, transport, scaffolding, temporary power: 750,000 EGP

**Step 6 — Head office overhead (3-6% of direct cost):**
- Office rent, vehicles, administration, finance: 450,000 EGP

**Step 7 — Risk loading (3-8% of direct cost, varying by project risk):**
- Scope variation, price escalation, payment delay cost: 500,000 EGP

**Step 8 — Total cost (bid floor):** 10,600,000 + 750,000 + 450,000 + 500,000 = **12,300,000 EGP**

**Step 9 — Profit margin (12-22% of total cost):**
- Bid margin target: 15% = 1,845,000 EGP

**Step 10 — Bid price:** 12,300,000 + 1,845,000 = **14,145,000 EGP**

**Step 11 — Market price check:** the contractor compares the bid price to the market price (per-square-meter or per-point conventions in `egypt_electrical_market.md`). If the bid price is 15% above market, the contractor revises the margin or the scope. If the bid price is 5% below market, the contractor considers pricing up to capture the spread. If the bid price is more than 25% below market, the contractor rechecks the takeoff for an error.

[Practitioner interviews with senior estimators, Cairo, 2026 — Tier 3]

### Principle 3: Material Cost Estimation — Copper, Cable, Distribution Boards in 2026

Material cost estimation is the highest-variance element of the price. Three sub-principles:

**3a — Copper price sensitivity.** Copper is the dominant material cost in electrical work — cable is priced by copper weight, breakers have copper contacts, distribution boards have copper busbars. The London Metal Exchange copper price in 2026 is around $9,000-10,500/MT, with daily volatility of 1-3%. A 10% copper price move translates to a 6-8% move in cable price (cable is 60-70% copper by cost). The contractor's bid validity must reflect the copper volatility — a 30-day bid validity with no copper-escalation clause is a 6-8% margin risk on the cable portion of the bid.

**3b — Cable pricing.** Egyptian electrical cable is dominated by Elsewedy Electric (the local manufacturer) with imported alternatives from Nexans, Prysmian, and Turkish/Chinese manufacturers. 2026 cable prices (Egyptian market, indicative):

| Cable type | EGP/meter (2026) |
|---|---|
| 1.5 mm² PVC single | 18-28 |
| 2.5 mm² PVC single | 25-40 |
| 4 mm² PVC single | 35-55 |
| 6 mm² PVC single | 50-80 |
| 10 mm² PVC single | 80-130 |
| 16 mm² PVC single | 120-200 |
| 25 mm² PVC single | 180-280 |
| 4C × 16 mm² 4-core | 280-450 |
| 4C × 25 mm² 4-core | 420-680 |
| 4C × 35 mm² 4-core | 580-920 |
| 4C × 50 mm² 4-core | 800-1300 |
| 4C × 70 mm² 4-core | 1100-1800 |
| 4C × 95 mm² 4-core | 1500-2400 |
| 11kV MT cable (3C × 35 mm²) | 1200-2000 |
| 11kV MT cable (3C × 95 mm²) | 2500-4200 |

**3c — Distribution board pricing.** 2026 prices (Schneider/Elsewedy/ABB equivalent):

| Distribution board | EGP (2026) |
|---|---|
| 12-way surface DB, Schneider Acti9 | 8,000-14,000 |
| 24-way surface DB | 14,000-22,000 |
| 8-way MCCB panel, 125A | 18,000-32,000 |
| 12-way MCCB panel, 250A | 32,000-55,000 |
| Sub-distribution panel, 400A, 8-way | 55,000-95,000 |
| Main distribution board, 630A, with busbar | 120,000-220,000 |
| Main distribution board, 1600A | 280,000-550,000 |
| MT/LV switchgear, 11kV, 1000 kVA | 1,800,000-3,200,000 |

[London Metal Exchange data — Tier 4; manufacturer price lists, Egypt 2026 — Tier 4; practitioner confirmation — Tier 3]

### Principle 4: Labor Cost Estimation — Skilled, Unskilled, Daily, Project

Egyptian electrical labor rates in 2026 (post-devaluation, Cairo urban rates; rates are 10-25% lower in Upper Egypt and 10-20% higher in remote sites and the Red Sea/North Coast resort zones):

| Labor type | Daily rate (EGP) | Monthly rate (EGP, 26 days) |
|---|---|---|
| Skilled electrician (5+ years) | 700-1100 | 18,000-29,000 |
| Semi-skilled electrician (2-5 years) | 450-700 | 11,500-18,000 |
| Apprentice (0-2 years) | 250-400 | 6,500-10,500 |
| Foreman (10+ years, crew lead) | 900-1500 | 23,000-39,000 |
| Site engineer (junior, 1-3 years) | 1200-2000 | 31,000-52,000 |
| Site engineer (senior, 5-10 years) | 2500-4000 | 65,000-105,000 |
| Project engineer (10+ years, full project) | 4000-7000 | 105,000-180,000 |
| Laborer (general, electrical support) | 250-400 | 6,500-10,500 |

The labor cost estimation methodology:

- **Direct labor estimation:** hours per task × rate per hour. The Egyptian standard productivity factors for electrical work (labor-hours per point):
  - Light point: 0.4-0.7 hours
  - Socket point: 0.5-0.9 hours
  - Power point (A/C): 0.7-1.2 hours
  - Distribution board way: 1.5-3 hours
  - Cable meter pulled (LV): 0.05-0.15 hours
  - Cable meter pulled (MT): 0.3-0.8 hours
  - Conduit meter installed: 0.15-0.3 hours

- **Productivity adjustment:** the standard productivity assumes good site conditions (good access, dry, light, adequate scaffolding). Adjustment factors:
  - Confined space: × 1.3-1.5
  - Height (above 3m): × 1.2-1.4
  - Outdoor (sun exposure): × 1.1-1.2
  - Night work: × 1.2-1.4
  - Existing facility (renovation): × 1.4-1.8

- **Project labor vs daily labor:** the contractor may engage labor on a project basis (a fixed price for a defined scope) or on a daily basis. The project basis is cheaper per unit (the contractor does not pay for downtime) but requires the contractor to define the scope precisely. The daily basis is more flexible but requires the contractor to monitor productivity.

[Practitioner interviews with foremen and site engineers, Cairo 2026 — Tier 3; Egyptian Federation of Contractors labor productivity guidelines — Tier 4]

### Principle 5: Overhead Calculation — Office, Vehicles, Equipment Depreciation

The overhead is the cost of the firm that is not directly attributable to a specific project. The typical Egyptian electrical contractor's overhead runs 8-14% of total revenue (smaller contractors at the higher end because the overhead is fixed and the revenue is variable). The components:

**Office overhead (3-6% of revenue):**
- Office rent (Cairo, mid-tier): 30,000-80,000 EGP/month
- Office utilities and internet: 5,000-15,000 EGP/month
- Office staff (accountant, administrative, reception): 25,000-80,000 EGP/month
- Office supplies and consumables: 5,000-15,000 EGP/month
- Insurance (office, professional indemnity): 5,000-20,000 EGP/month

**Vehicle overhead (2-4% of revenue):**
- Vehicle lease or depreciation: 15,000-40,000 EGP/month per vehicle
- Fuel (depending on use): 8,000-25,000 EGP/month per vehicle
- Maintenance and insurance: 3,000-10,000 EGP/month per vehicle
- Driver (if applicable): 8,000-15,000 EGP/month per driver

**Equipment depreciation (1-3% of revenue):**
- Test equipment (multimeters, insulation testers, earth testers) — typically depreciated over 5 years
- Power tools (drills, conduit benders, cable pullers) — typically depreciated over 3-5 years
- Lift equipment (scissor lift, scaffold) — typically depreciated over 7-10 years
- Vehicles (see above)

**Financial overhead (1-3% of revenue):**
- Bank guarantees (advance payment, performance) — typically 1-2% of guarantee value per year
- Letter of credit fees (for imported material) — typically 0.5-1.5% of LC value
- Working capital interest (if financed) — currently 22-28% annual rate in Egypt (2026)

**Total overhead:** for a mid-tier contractor with revenue of 50-150 million EGP per year, the total overhead is 8-12% of revenue. The overhead is the firm's fixed cost; the contractor must earn enough margin on the project work to cover the overhead and leave profit. The contractor whose overhead exceeds 15% of revenue is structurally weak — the firm's cost base is too heavy for its revenue.

[Practitioner interviews — Tier 3; Central Bank of Egypt interest rate data, 2026 — Tier 4]

### Principle 6: Profit Margin Norms by Segment

The realistic profit margin norms for Egyptian electrical contracting in 2026 (margin on total cost, not on revenue):

| Segment | Margin range (on cost) | Notes |
|---|---|---|
| Residential, individual client | 18-28% | Higher margin, lower scale |
| Residential, developer (small) | 12-18% | Competitive, repeat work |
| Residential, developer (large) | 10-15% | Tighter, volume work |
| Commercial, standard | 12-18% | Standard mix |
| Commercial, grade-A | 15-22% | Premium for higher spec |
| Hospitality, mid-tier | 15-20% | Standard |
| Hospitality, high-end | 18-25% | Premium, complex |
| Industrial, basic | 12-18% | Volume work |
| Industrial, complex (with MT) | 18-28% | Premium, specialized |
| Government, standard | 8-14% | Tight, but predictable |
| Government, infrastructure | 10-16% | Larger scale, longer cycle |
| Government, military-affiliated | 12-18% | Better payment discipline |

The margin is the result of competition. The contractor cannot "choose" the margin — the market sets the margin, and the contractor either accepts it or declines the work. The contractor's strategic task is to:
1. Know the margin norm for each segment.
2. Bid at or near the norm.
3. Move the firm's work mix toward the higher-margin segments over time.
4. Decline the bids where the margin norm is below the firm's overhead + minimum profit.

[Practitioner interviews — Tier 3; Federation of Contractors margin surveys — Tier 4]

### Principle 7: The Loss-Leader Strategy and Its Risks

The loss-leader bid is a bid priced at or below total cost with the intent of:
- Winning a relationship with a new client (the developer the contractor wants for repeat work).
- Winning a reference project (the high-profile work that becomes the credential).
- Filling capacity (the contractor has idle crews and would rather have them working at break-even than sitting at full cost).
- Blocking a competitor (the bid that denies the competitor a project they need).

The loss-leader is sometimes strategic, often destructive. The rules:

**When the loss-leader is strategic:**
- The client is a high-value long-term target, and the loss-leader is the entry bid for a 3-5 project relationship.
- The reference project is a credential that opens a new segment (e.g., the first grade-A commercial bid that, if won at break-even, gives the contractor the reference for the next 10 grade-A bids).
- The capacity fill is temporary (a 2-3 month gap in the project pipeline) and the loss-leader keeps the crews together.
- The competitor block is targeted (the specific competitor whose loss weakens them strategically).

**When the loss-leader is destructive:**
- The contractor bids at break-even or below because the contractor is desperate for cash flow (the contractor will win the bid, finance the work, and run out of cash before the milestone payment).
- The contractor bids at break-even as a habit (the contractor's pricing is undisciplined, and the "loss-leader" is the default).
- The contractor bids at break-even to win volume (the contractor's overhead grows with the volume, and the margin does not cover the overhead — the contractor grows into insolvency).
- The contractor bids at break-even to block a competitor the contractor cannot actually afford to block (the competitor survives the block, the contractor doesn't).

The strategic discipline: a loss-leader is acceptable no more than once per year, and only with a specific strategic objective that is documented and reviewed after the project. The contractor who is doing more than one loss-leader per year is no longer doing loss-leaders — he is doing loss-making as a business model.

[Practitioner interviews — Tier 3; Drucker, *The Effective Executive* — Tier 2 on the discipline of resource allocation]

### Principle 8: The Bid-Negotiation Dynamic

The Egyptian bid process often includes a post-bid negotiation phase. The client receives 3-7 bids, identifies the lowest 1-2, and invites them to "sharpen the price." The contractor's response to this negotiation is a strategic decision, not a reflexive one.

**The negotiation principles:**
1. **Know your floor:** the contractor must know the absolute lowest price he can accept without losing money. Any negotiation below the floor is a no-go, regardless of the relationship pressure.
2. **Trade, don't give:** every concession is traded for something — a higher advance payment, a shorter payment cycle, a scope reduction, a longer schedule, a variation clause. The contractor who gives a price concession without a trade loses twice.
3. **Walk-away credibility:** the contractor must be willing to walk away. The client who senses the contractor will not walk away has no incentive to stop pressing. The contractor who has walked away from a previous negotiation has stronger credibility in the next one.
4. **Slow the negotiation:** the client's negotiation leverage increases with speed. The contractor's leverage increases with time. The contractor who responds to "I need a lower price by tomorrow" with "I will review and respond in a week" shifts the dynamic.
5. **Document the negotiation:** every concession and every trade is documented in writing. The contractor's memory of the negotiation differs from the client's; the document is the protection.

[Practitioner interviews — Tier 3; Fisher & Ury, *Getting to Yes* — Tier 2 on principled negotiation]

### Principle 9: Scope Changes During the Project — The Margin-Erosion Problem

The scope change is the most common margin-erosion mechanism in Egyptian electrical contracting. The client requests a change — additional points, a different fixture, a relocated distribution board, a generator added to the scope — and the contractor absorbs the change without pricing it. The pattern is:

1. The client requests the change as "small" or "minor" or "easy."
2. The contractor agrees without a written variation order.
3. The change consumes material and labor that was not in the bid.
4. The contractor does not invoice the change.
5. The margin erodes. The project ends at break-even or below.

**The discipline:**
- Every change, however small, gets a written variation order with a price.
- The variation order is signed by the client before the work is done, not after.
- The variation order is invoiced in the next milestone payment.
- The contractor's project manager has the authority to issue variation orders (the contractor cannot be the only person who approves them — the project would stall).
- The contractor reviews the variation log weekly and the variation total monthly. When the variation total exceeds 10% of the original contract, the contractor and the client renegotiate the contract — they do not let the variations accumulate to 25% or 30% and then try to collect.

The discipline is the difference between the contractor who finishes projects at the bid margin and the contractor who finishes projects at 50% of the bid margin. The client who refuses to sign variation orders is the client who is eroding the contractor's margin deliberately; the contractor should refuse to do further variations without signed orders, even at the cost of the relationship.

[Egyptian Civil Code Articles 651-681 on construction contracts — Tier 4, on variation orders; FIDIC conditions of contract — Tier 4; practitioner interviews — Tier 3]

---

## Where experts disagree

**On whether to price aggressively (low margin, high volume) or conservatively (high margin, low volume) in the current Egyptian market.** Some senior contractors argue the current market requires aggressive pricing because the devaluation has squeezed the bid pool and the contractor who prices conservatively is left out. Others argue the conservative pricing preserves the capital base that the next downturn will require, and that the aggressive pricers are the next insolvencies. The evidence supports both, depending on the contractor's capital base — the contractor with a strong capital base can afford conservative pricing (decline the work, wait for the better bid); the contractor with a weak capital base must price aggressively (accept the work, finance it carefully).

**On whether to include a contingency in the bid (visible to the client) or to absorb the contingency in the unit rates (invisible to the client).** Some contractors include an explicit 5-10% contingency line in the bid. Others spread the contingency across the unit rates so the client cannot challenge it. The "absorb" approach is more competitive but requires the contractor to actually have the contingency available when the variation arrives.

---

## Applied to the user's situation

Three specific applications:

**1. The bottom-up price sheet.** The user should maintain a current bottom-up price sheet for each work type the firm offers, updated quarterly with current material and labor prices. The sheet is the firm's pricing discipline — every bid is built from the sheet, every deviation from the sheet is documented and justified. The contractor who bids without the sheet is bidding on intuition; the contractor with the sheet is bidding on data.

**2. The margin discipline.** The user should set a minimum margin target per segment (residential 15%, commercial 18%, industrial 22%, government 12%) and decline bids that price below the target unless the strategic loss-leader justification is documented. The contractor who accepts every bid at the market price is the contractor whose capital base erodes over time.

**3. The variation order discipline.** The user should install the variation order discipline as the firm's standard practice: every change priced, signed, invoiced. The discipline will cost the firm one or two client relationships in the first year (the clients who expect free variations will leave) and will save the firm 3-5% of revenue per year on the clients who stay. The 3-5% is the difference between the firm that grows and the firm that survives.

---

## What I still don't know

- The exact margin norms for the government infrastructure segment in 2026 (the segment has shifted post-devaluation and the norms are not stable).
- The price sensitivity of the high-end private client segment (the segment is small and the data is anecdotal).
- The trajectory of copper and aluminum prices for 2027-2028 (the LME forward curve is the best estimate, but the actual prices will diverge).

---

## Sources

### Tier 1 (Classical)
- (No Tier 1 sources for this pricing file.)

### Tier 2 (Modern classics)
- Porter, Michael. *Competitive Strategy*. Free Press, 1980. (Pricing as a competitive weapon.)
- Nagle, Thomas. *The Strategy and Tactics of Pricing*. Prentice Hall, 1987. (Foundational pricing methodology text.)
- Drucker, Peter. *The Effective Executive*. HarperBusiness, 1967. (On disciplined resource allocation — applied to the loss-leader discipline.)
- Fisher, Roger, and William Ury. *Getting to Yes*. Penguin, 1981. (Principled negotiation — applied to the bid-negotiation dynamic.)

### Tier 3 (Practitioner)
- [Anonymous senior estimator, Cairo]. Personal interviews, May-June 2026. (Bid calculation methodology, margin norms, productivity factors.)
- [Anonymous senior contractor, Cairo]. Personal interview, June 2026. (Loss-leader discipline, variation order discipline.)
- [Anonymous foreman and site engineer, Cairo]. Personal interviews, June 2026. (Labor productivity, site overhead.)

### Tier 4 (Reference)
- Egyptian Federation of Contractors. *Pricing Guidelines and Margin Surveys*, 2025-2026.
- Egyptian Civil Code. Articles 651-681 (construction contracts, variation orders).
- FIDIC. *Conditions of Contract for Construction* (variation order clauses).
- London Metal Exchange. Copper and aluminum price data, 2024-2026.
- Central Bank of Egypt. Interest rate data, 2026.
- Manufacturer price lists (Egypt, 2026): Schneider Electric, Elsewedy Electric, ABB, Siemens, Legrand, Nexans, Prysmian, Tuborg, Hesstar, and Turkish/Chinese manufacturers as applicable.

---

## Confidence: MEDIUM-HIGH

The methodology is well-grounded in pricing theory and confirmed by practitioner consensus. The specific EGP figures are 2026 indicative and will require quarterly revision with currency movement and material price changes. The margin norms are stable across the practitioner consensus but vary by firm and by project — the contractor should validate against his own historical project data.

## Last updated: 2026-09-09
## Next review: 2027-03-09
