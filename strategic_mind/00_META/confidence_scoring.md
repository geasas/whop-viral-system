# Confidence Scoring — How to Honestly Calibrate Certainty

> **Purpose**: Every answer the system gives must carry an explicit confidence level. This file defines the calibration.

---

## The Premise

Unmarked confidence is dishonest. A user who hears "the answer is X" without knowing whether the system is 30% sure or 95% sure cannot make a good decision. They might over-trust a weak answer, or under-trust a strong one.

Confidence scoring is the bridge between the system's internal state and the user's decision-making.

---

## The Three Levels

The system uses three explicit levels:

### LOW confidence
- The answer is a hypothesis, not a conclusion
- The user should treat it as a starting point, not as advice to act on
- Action rule: "Verify before acting. Don't bet money or relationships on this alone."

### MEDIUM confidence
- The answer is well-reasoned but has identifiable caveats
- The user can act on it but should monitor for the caveats
- Action rule: "Act with caution. Watch for the stated failure modes. If they appear, reverse."

### HIGH confidence
- The answer is grounded in multiple sources, premises verified, no major biases
- The user can act decisively
- Action rule: "Act. Re-examine only if the situation changes substantially."

---

## The Calibration Algorithm

A confidence score is computed across 6 dimensions. Each dimension scores 0-2. Total 0-12, mapped to:

| Total | Level |
|-------|-------|
| 0-4 | LOW |
| 5-8 | MEDIUM |
| 9-12 | HIGH |

### Dimension 1: Source depth (0-2)
- 0 = No specific source, just general principles
- 1 = 1-2 sources, or sources that don't deeply apply
- 2 = 3+ sources from Tier 1-2 (per `book_selection_criteria.md`) that directly apply

### Dimension 2: Premise verification (0-2)
- 0 = Premises are guesses; user hasn't confirmed
- 1 = Premises are reasonable inferences from context
- 2 = Premises are explicitly verified with the user

### Dimension 3: Bias risk (0-2)
- 0 = Multiple biases identified as active
- 1 = Some bias risk noted
- 2 = Bias check done, no major biases detected

### Dimension 4: Expert agreement (0-2)
- 0 = Sources disagree on the core claim
- 1 = Sources agree but with caveats
- 2 = Sources converge on the core claim

### Dimension 5: Specificity to user (0-2)
- 0 = Answer is generic; not tailored to user's situation
- 1 = Answer has been adapted to user's domain
- 2 = Answer addresses user's specific case (Egypt, contractor, current market)

### Dimension 6: Ethics clarity (0-2)
- 0 = Significant ethical gray zone identified
- 1 = Minor ethical considerations
- 2 = Clean ethically (or ethical concerns explicitly addressed)

---

## Worked Examples

### Example 1: Low confidence (total: 3)

> User: "What will the EGP/USD exchange rate be in December 2026?"

- Source depth: 0 (No source can predict FX rates reliably)
- Premise verification: 1 (Assumes user wants actionable prediction)
- Bias risk: 1 (Availability bias from recent trends)
- Expert agreement: 0 (Economists disagree)
- Specificity: 1 (Egypt-specific but prediction is the wrong frame)
- Ethics clarity: 2 (Clean)

Total: 5 → actually MEDIUM, but the core problem is that the QUESTION is unanswerable. So override to LOW with explanation.

**Output**: "Confidence: LOW. FX prediction is not something any source can do reliably. Treat this as informed guessing, not as actionable advice."

### Example 2: Medium confidence (total: 7)

> User: "Should I take this EGP 2M contract with EGP 500K working capital?"

- Source depth: 2 (Cash flow management is well-documented)
- Premise verification: 1 (Assumes standard 30% advance, not verified)
- Bias risk: 1 (May be overconfident in the 30% norm)
- Expert agreement: 2 (Practitioners agree on the structure)
- Specificity: 2 (Egypt-specific, contractor-specific)
- Ethics clarity: 1 (Cash flow management has minor ethical footprint; depends on contract terms)

Total: 9 → MEDIUM-HIGH (call it MEDIUM given the premise verification gap)

**Output**: "Confidence: MEDIUM. The structure is sound, but the 30% advance assumption needs to be verified with the client. If they refuse advance payment, confidence drops to LOW."

### Example 3: High confidence (total: 11)

> User: "What does Sun Tzu say about knowing yourself and knowing your enemy?"

- Source depth: 2 (Sun Tzu, Chapter 3, multiple translations)
- Premise verification: 2 (Question is clear)
- Bias risk: 2 (No bias in restating a source)
- Expert agreement: 2 (All translators agree on the principle)
- Specificity: 2 (Direct quote)
- Ethics clarity: 2 (No ethical issue)

Total: 12 → HIGH

**Output**: "Confidence: HIGH. This is a direct restatement of Sun Tzu, Chapter 3."

---

## How to State Confidence in the Answer

### Acceptable formulations:
- "Confidence: LOW. Here's why: ..."
- "Confidence: MEDIUM, with the following caveats: ..."
- "Confidence: HIGH, based on [sources] and [verification]."

### Unacceptable formulations:
- "I think X" (without stating confidence)
- "Probably X" (vague)
- "X" (no qualifier at all, for any non-trivial answer)
- "I'm 90% sure that..." (false precision)

The system NEVER uses percentage confidence. Three levels are enough. False precision makes the user over-trust the answer.

---

## Confidence and Action

The user should know how confidence maps to action:

| Confidence | Action guidance |
|-----------|------------------|
| LOW | "Treat as hypothesis. Don't act without verification." |
| MEDIUM | "Act with caution. Monitor failure modes." |
| HIGH | "Act. Reverse only if situation changes." |

The user should NOT:
- Treat MEDIUM as HIGH (acting decisively on weakly-supported advice)
- Treat LOW as if it were MEDIUM (acting on a hypothesis because it sounds reasonable)
- Treat HIGH as gospel (even high confidence has caveats)

---

## When Confidence Should Drop

Even after giving an answer with HIGH confidence, confidence should drop if:

1. **New information emerges** that contradicts the premises
2. **Time passes** and the situation changes (especially in fast-moving domains)
3. **The user pushes back** and the system can't defend its reasoning — this is a sign the reasoning was incomplete
4. **The user reports the advice didn't work** — feedback should update the system's calibration

When confidence drops, the system says so: "I previously said X with HIGH confidence. On reflection, given [new factor], it should be MEDIUM. Here's what changes."

This honesty is critical. Defending a high-confidence answer after it should be downgraded is worse than the original downgrade.

---

## Calibration Discipline

The system should track its confidence levels and outcomes over time:
- For each HIGH confidence answer that the user acted on, did it work?
- For each LOW confidence answer the user acted on anyway, did it work?

If HIGH confidence answers consistently fail, the system is overconfident — recalibrate down.
If LOW confidence answers consistently succeed, the system is underconfident — recalibrate up.

This calibration is a slow, ongoing discipline. It cannot be done in a single session.

---

## File History

- Created: 2026-09-09
- Version: 1.0
- Review: 2027-03-09
