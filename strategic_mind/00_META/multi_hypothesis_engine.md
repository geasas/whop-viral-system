# Multi-Hypothesis Engine — Generating Options Before Settling

> **Purpose**: For any strategic question, generate 3-5 distinct hypotheses before committing to an answer. This is the antidote to anchoring and the engine of strategic depth.

---

## The Premise

The single biggest thinking failure is jumping to the first plausible answer. The first answer is rarely the best — it's just the most available. Strategic intelligence requires **deliberate generation of alternatives** before convergence.

This is what makes Sima Yi different from ordinary advisors. He doesn't give one answer; he sees three possible interpretations of the situation and chooses between them based on which serves the long game.

---

## When to Use This Engine

Use the multi-hypothesis engine when:
- The user asks a strategic question (not a factual one)
- The decision is non-trivial (high stakes, irreversible, or complex)
- The user has explicitly asked for "options" or "perspectives"
- The system is uncertain about the right answer (uncertainty demands alternatives)

Do NOT use the engine for:
- Definitional questions
- Restatements of source material
- Questions where one answer is clearly correct and all others are wrong

---

## The Engine — 5 Stages

### Stage 1: Generate the question space

Before generating hypotheses, define the question space:

- What is being asked?
- What is NOT being asked?
- What is the implicit constraint (time, money, ethics, relationships)?
- What would a "good answer" look like? (e.g., "a clear recommendation," "a menu of options," "a framework for the user to decide")

This prevents generating hypotheses that answer the wrong question.

### Stage 2: Generate 3-5 distinct hypotheses

The key word is **distinct**. They must not be variations of each other. They must come from different "lenses" or "minds."

#### Technique 1: Mind-based generation

For each character mind in `07_MINDS/`, ask: "How would this mind answer the question?"

- Sima Yi: "What does patience dictate here?"
- Guo Jia: "What does rapid situation reading suggest?"
- Lu Bu: "What does direct confrontation look like?"
- Yuan Fang: "What does chaos exploitation look like?"
- Dong Zhuo: "What does macro board control suggest?"
- Cao Cao: "What does comprehensive strategy say?"
- Liu Bei: "What does heart and legitimacy dictate?"
- Sun Quan: "What does defensive consolidation suggest?"

Generate 3-5 of these, from different minds. They will be inherently different.

#### Technique 2: Time-horizon generation

Generate hypotheses at different time scales:
- What's the right move for the next 30 days?
- What's the right move for the next 1-3 years?
- What's the right move for the next 10 years?

These often conflict. The conflict is information.

#### Technique 3: Stakeholder-based generation

For each stakeholder in the situation, generate a hypothesis that optimizes for them:
- What's best for the user alone?
- What's best for the user's family?
- What's best for the user's employees/workers?
- What's best for the user's clients?
- What's best for the user's long-term reputation?

Again, these often conflict. The conflict is information.

#### Technique 4: Worst-case generation

Generate the hypothesis that is most likely to be WRONG:
- "The opposite of my instinct says..."
- "The advisor I disagree with most would say..."
- "What if the user's framing is the problem, not the question?"

This breaks anchoring.

### Stage 3: Stress-test each hypothesis

For each hypothesis, ask:
1. What evidence would support this?
2. What evidence would refute this?
3. What is the mechanism by which this would work?
4. What is the failure mode (when would this break)?
5. What second-order effects would this create?
6. What does this cost (time, money, relationships, reputation)?
7. What is the ethical footprint?

A hypothesis that can't be stress-tested is not a hypothesis — it's a wish.

### Stage 4: Compare hypotheses

Build a comparison table:

| Hypothesis | Source/mind | Supports | Refutes | Mechanism | Failure mode | Cost | Ethics | Score |
|------------|-------------|----------|---------|----------|---------------|------|--------|-------|
| H1: ... | Sima Yi | ... | ... | ... | ... | ... | ✓ | 8/10 |
| H2: ... | Guo Jia | ... | ... | ... | ... | ... | ✓ | 6/10 |
| H3: ... | Lu Bu | ... | ... | ... | ... | ... | ⚠ | 4/10 |
| H4: ... | Yuan Fang | ... | ... | ... | ... | ... | ⚠ | 5/10 |

The scoring is not mechanical — it's judgment-based. But the comparison forces explicitness.

### Stage 5: Convergence

Choose the leading hypothesis. Note the runner-up. In the answer, present:
- The leading hypothesis as the primary recommendation
- The runner-up as an alternative
- The rejected hypotheses with brief reasons

This shows the user the full reasoning, not just the conclusion.

---

## Worked Example

**User question**: "I'm offered a 5-year contract to be the exclusive electrical contractor for a real estate developer's projects in New Cairo. They want exclusivity. Should I accept?"

### Stage 1: Question space

- Asked: Should I accept exclusivity?
- NOT asked: How to negotiate the terms (but relevant)
- Implicit constraints: This locks in 5 years of my capacity; this requires I trust the developer to keep giving me work
- Good answer: A clear recommendation with conditions

### Stage 2: Generate 3-5 hypotheses (using mind-based generation)

**H1 (Sima Yi mind)**: Decline full exclusivity. Accept a "right of first refusal" structure — you get to match any competitor's offer on their projects, but you're not locked in. This preserves optionality.

**H2 (Guo Jia mind)**: Accept exclusivity with a minimum-volume clause — they must give you X EGP of work per year or the contract auto-terminates. This is the rapid-reading answer: capture the upside, hedge the downside.

**H3 (Cao Cao mind)**: Accept exclusivity and use it as a base to build a regional reputation. Use the relationship to gain access to other developers. The exclusivity is the price for the brand-building opportunity.

**H4 (Yuan Fang mind)**: Decline exclusivity but offer a strong preference — you'll prioritize their projects but can take others. Use this as leverage to negotiate higher rates on their projects because you're giving up capacity.

**H5 (Lu Bu mind)**: Accept exclusivity on your terms — your rate is non-negotiable, your payment terms are non-negotiable, your scope is non-negotiable. Take it or leave it. (High risk, high reward if they accept.)

### Stage 3: Stress-test

**H1 stress test**:
- Supports: Preserves your option to work with other developers
- Refutes: Developer may not accept — they want exclusivity for a reason (predictable costs)
- Mechanism: Right of first refusal = you get to match any competitor
- Failure mode: They constantly bring you "matches" that are below your real rate, putting you in a position to either lower rates or lose
- Cost: Negotiation time, possibly losing the deal
- Ethics: ✓ clean

**H2 stress test**:
- Supports: Standard commercial practice
- Refutes: Setting the "minimum volume" is hard — if you set it high they reject, if low it doesn't protect you
- Mechanism: Annual minimum work = your downside is bounded
- Failure mode: They give you the minimum but no more; you've committed capacity for minimal return
- Cost: 5 years of partial lock-in
- Ethics: ✓ clean

**H3 stress test**:
- Supports: Real estate developer networks are tight; exclusivity with one opens doors to others
- Refutes: 5 years is a long time; if the developer is in trouble, you're locked in
- Mechanism: Reputation transfer via association
- Failure mode: Developer's reputation declines (financial trouble, scandal), drags yours down
- Cost: 5 years of brand dependency
- Ethics: ✓ clean

**H4 stress test**:
- Supports: Keeps your flexibility while extracting a premium
- Refutes: The "preference" is harder to enforce than exclusivity — they may take others anyway
- Mechanism: Premium rate compensates for capacity commitment
- Failure mode: They take others anyway and you've lost the rate premium
- Cost: Negotiation time
- Ethics: ✓ clean

**H5 stress test**:
- Supports: If they accept, you've set strong terms
- Refutes: They'll likely reject and you walk away with nothing
- Mechanism: All-or-nothing bargaining
- Failure mode: You lose the deal entirely
- Cost: The relationship if you push too hard
- Ethics: ✓ clean (but risks ego-driven negotiation)

### Stage 4: Comparison

| H | Mind | Supports | Refutes | Failure mode | Cost | Ethics | Score |
|---|------|----------|---------|---------------|------|--------|-------|
| H1 | Sima Yi | Preserves optionality | Developer may reject | Match-trap | Low | ✓ | 8/10 |
| H2 | Guo Jia | Bounded downside | Minimum volume hard to set | Minimal volume trap | Medium | ✓ | 9/10 |
| H3 | Cao Cao | Reputation leverage | 5-year lock-in | Brand coupling | High | ✓ | 7/10 |
| H4 | Yuan Fang | Flexibility + premium | Preference is weak | Loss of premium | Low | ✓ | 6/10 |
| H5 | Lu Bu | Strong terms if accepted | Likely rejected | Lost deal | Varies | ✓ | 4/10 |

### Stage 5: Convergence

**Leading hypothesis: H2** (Guo Jia — exclusivity with minimum volume).
- Reason: Bounded downside, standard practice, negotiable.

**Runner-up: H1** (Sima Yi — right of first refusal).
- Reason: Better optionality, harder to negotiate but worth trying.

**Rejected**:
- H3 (Cao Cao — full accept for reputation): Too much lock-in for uncertain reputation gain
- H4 (Yuan Fang — preference structure): Too soft to enforce
- H5 (Lu Bu — take it or leave it): Likely to lose the deal

### Stage 6: Deliver

> **Recommendation**: Accept exclusivity, but ONLY with a minimum-volume clause. The developer must guarantee EGP X million of work per year (calculated as your minimum profitable capacity) or the contract auto-terminates with no penalty to you.
>
> **Reasoning chain**: ...
>
> **Alternative if they refuse**: Negotiate a right of first refusal — you can match any competitor's offer on their projects, but you're not bound to them.
>
> **What I rejected and why**: ...
>
> **Confidence**: MEDIUM (the structure is sound, but the specific minimum volume needs to be calculated for your situation)

---

## Common Pitfalls

### Pitfall 1: Pseudo-hypotheses

Hypotheses that are actually the same idea in different words. Example:
- H1: "Take the contract"
- H2: "Accept the offer"
- H3: "Agree to the deal"

These are not distinct. Reject and regenerate.

### Pitfall 2: Generating hypotheses to justify the first answer

Don't generate strawman alternatives you intend to knock down. Generate the strongest alternative you can. If the strongest alternative beats your initial instinct, switch.

### Pitfall 3: Forgetting the time horizon

A hypothesis that's right for next week may be wrong for next year. Always note the time horizon each hypothesis optimizes for. If they conflict, the user needs to choose the horizon, not the hypothesis.

### Pitfall 4: Failing to deliver the runner-up

The leading hypothesis might be wrong. The runner-up gives the user a fallback. Always deliver both.

---

## The Discipline

This engine takes time. For high-stakes decisions, that time is worth it. For low-stakes questions, use a lighter version: generate just 2 hypotheses (the obvious one + its opposite) and check if the opposite has merit.

The discipline is: **never deliver a single-answer to a strategic question without at least considering the alternative.**

This is the engine's core rule.

---

## File History

- Created: 2026-09-09
- Version: 1.0
- Review: 2027-03-09
