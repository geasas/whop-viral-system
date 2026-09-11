# The Iterative Refinement Loop — Plan, Build, Review, Hunt, Fix, Repeat

> **Layer**: 00_META/
> **File**: iterative_refinement_loop
> **Purpose**: A single answer is rarely the best answer. The best answer emerges from a structured cycle of planning, building, reviewing, hunting for flaws, fixing, and repeating. This file is the protocol for that cycle.
> **Created**: 2026-09-10
> **Version**: 1.0
> **Review**: 2027-03-10
> **Maximum iterations**: 4 (per user direction — beyond this lies paralysis)

---

## The Premise

Most strategic advice is produced in a single pass: the system reads the question, thinks, writes an answer, sends it. This is fast but produces shallow answers. The first answer is rarely the best answer — it's just the first answer.

The Iterative Refinement Loop is the system's discipline for producing deep answers through structured repetition. Each iteration improves the answer. After 4 iterations (the user-defined maximum), the answer is delivered.

This is not "trying again." It is a specific sequence of operations applied to the answer to improve it in different ways.

---

## The 6 Stages of the Loop

The loop has 6 stages. Each stage has a specific purpose and a specific output. The loop runs a maximum of 4 times. Each iteration produces a measurable improvement.

### Stage 1: Plan

**Purpose**: Before building, plan what the answer should be.

**Activities**:
- State the reframed question (from `deep_question_understanding.md`)
- Identify the minds that apply
- Identify the knowledge layers that apply
- Sketch the answer structure: introduction, analysis, options, recommendation, second-order effects, confidence, sources
- Estimate the answer length and depth
- Identify what evidence is needed

**Output**: A one-paragraph plan for the answer.

**Example**: For "Should I take this EGP 5M contract?":
- Minds: Sima Yi (long-game), Cao Cao (multi-stakeholder), Guo Jia (decisive if window closing)
- Knowledge layers: 09_BUSINESS/contracting/cash_flow_zero_capital.md, 09_BUSINESS/contracting/pricing_methodology.md, 05_POSITION/asymmetric_strategy.md
- Structure: Diagnose the situation → Analyze the cash flow → Identify the 3 options (take, decline, negotiate) → Recommend with conditions → Identify failure modes → Confidence
- Evidence needed: typical advance payment norms in Egypt 2026, cash flow cycle for similar projects

### Stage 2: Build

**Purpose**: Write the first draft of the answer based on the plan.

**Activities**:
- Write the answer following the structure from Stage 1
- Cite sources with tier annotations per `research_protocol.md` Stage 6
- Apply the minds explicitly (e.g., "Sima Yi's perspective on this is X because Y")
- Include the failure modes and second-order effects
- State the confidence level

**Output**: A complete first draft of the answer.

**Example**: A 2000-word answer covering diagnosis, analysis, options, recommendation, failure modes, confidence.

### Stage 3: Review

**Purpose**: Read the answer as if you were the user. Identify what's missing, what's confusing, what's unconvincing.

**Activities**:
- Read the answer end-to-end
- Identify gaps: what should be in the answer that isn't?
- Identify confusions: what would the user misunderstand?
- Identify weak arguments: what wouldn't convince a skeptic?
- Identify missing perspectives: which minds weren't invoked but should have been?
- Identify missing sources: what claims aren't backed?

**Output**: A list of improvements to make.

**Example**: Review notes:
- "Gap: didn't address the spiritual dimension (is taking this contract tawakkul or recklessness?)"
- "Confusion: the term 'working capital' wasn't defined — user might mean different things"
- "Weak argument: the claim that 'Egyptian contractors typically negotiate 20% advance' needs a source"
- "Missing perspective: didn't invoke Liu Bei for the relationship dimension with this client"
- "Missing source: the 4:1 capital-to-project ratio recommendation needs citation"

### Stage 4: Hunt (Vulnerability Hunting)

**Purpose**: Try to break the answer. Find the flaws actively, not passively. See `vulnerability_hunting.md` for the full protocol.

**Activities**:
- Apply the 5 vulnerability types: logical, factual, ethical, strategic, operational
- Apply the Red Team exercise: try to argue the opposite conclusion
- Apply the Smart Critic exercise: what would the most intelligent critic say?
- Apply the Stress Test: what conditions would make this answer wrong?

**Output**: A list of vulnerabilities found.

**Example**: Vulnerabilities:
- "Logical vulnerability: assumes the 20% advance is guaranteed — what if client refuses?"
- "Factual vulnerability: the 4:1 ratio recommendation is from US construction, may not apply to Egypt"
- "Ethical vulnerability: didn't address whether the contract terms are fair to the client"
- "Strategic vulnerability: didn't consider what competitors will do if I take this project"
- "Operational vulnerability: didn't address whether my team has the capacity for this project size"

### Stage 5: Fix

**Purpose**: Address the vulnerabilities found in Stage 4 and the improvements identified in Stage 3.

**Activities**:
- Add the missing content identified in Stage 3
- Address each vulnerability from Stage 4 (either by fixing the argument, by adding caveats, or by acknowledging the limit)
- Re-cite sources where claims were unsupported
- Re-invoke minds where perspectives were missing
- Re-write weak arguments more strongly

**Output**: An improved version of the answer.

### Stage 6: Iterate (or Converge)

**Purpose**: Decide whether to loop again or deliver.

**Decision criteria**:
- If the answer has improved substantially AND there are still clear improvements to make → loop again (return to Stage 3: Review)
- If the answer has improved substantially AND no clear improvements remain → deliver
- If the answer has not improved substantially from the previous iteration → deliver (further iteration is not productive)
- If you've reached the 4-iteration maximum → deliver (the discipline prevents paralysis)

**Maximum iterations**: 4 (per user direction). Beyond 4 iterations, the marginal improvement is typically less than the cost of additional time.

---

## The 4-Iteration Pattern

Here is what typically happens across 4 iterations:

### Iteration 1: The First Draft

The first draft is the "obvious" answer. It covers the main points but has gaps, weak arguments, and unaddressed perspectives. It's the answer most systems would deliver as final.

**Typical word count**: 1500-2500 words.
**Typical quality**: 60% of optimal.

### Iteration 2: The Deepening

After Review and Hunt, the second iteration adds:
- Missing perspectives (minds that weren't invoked)
- Missing sources (claims that weren't cited)
- Failure modes that weren't addressed
- Second-order effects that weren't considered

**Typical word count**: 2500-4000 words.
**Typical quality**: 75% of optimal.

### Iteration 3: The Stress Test

After another Review and Hunt, the third iteration:
- Addresses the strongest counter-arguments
- Adds the conditions under which the answer would be wrong
- Acknowledges the limits of the analysis
- Adds the ethical and spiritual dimensions

**Typical word count**: 4000-5500 words.
**Typical quality**: 88% of optimal.

### Iteration 4: The Polish

The final iteration:
- Tightens the language (removes redundancy)
- Strengthens the weakest arguments
- Adds the final source citations
- Refines the confidence calibration
- Adds the "what I still don't know" section

**Typical word count**: 4000-6000 words (sometimes shorter than iteration 3 due to tightening).
**Typical quality**: 92-95% of optimal.

**Note**: 100% is never reached. There is always more that could be done. The 4-iteration cap prevents the pursuit of perfection from becoming procrastination.

---

## Convergence Criteria

The loop converges (stops) when one of these is true:

1. **Maximum iterations reached**: 4 iterations completed.
2. **Diminishing returns**: the improvement from the latest iteration was minor (less than 10% better than the previous).
3. **No clear next improvement**: the Review and Hunt stages produced no actionable items.
4. **Time budget exceeded**: if a time budget was set (e.g., "answer within 30 minutes"), the loop stops when the budget is exhausted.

The system explicitly states which convergence criterion applied: "I delivered this answer after 3 iterations because the fourth iteration produced no significant improvement."

---

## When to Use the Loop

### Use the loop for:
- High-stakes decisions (financial, strategic, ethical, irreversible)
- Multi-faceted questions (where multiple minds and layers apply)
- Questions where the user has explicitly asked for depth
- Questions where the first answer would be too simple

### Skip the loop for:
- Definitional questions ("What does riba mean?")
- Restatements of source material ("What did Sun Tzu say about terrain?")
- Quick calibration questions ("Is this normal?")
- Single-step factual questions ("What is the Federation of Contractors classification grade 4?")

For these, a single-pass answer is appropriate.

### The discipline: matching the loop depth to the question.

A 5-minute question gets a single pass. A 30-minute question gets 2 iterations. A 2-hour question gets 4 iterations. The user's question signals the appropriate depth.

---

## The Loop in Practice: A Worked Example

**User question**: "I'm offered a 5-year exclusive contract with a major developer. Should I accept?"

### Iteration 1

**Plan**: Diagnose (high-stakes, multi-year, multi-stakeholder) → Minds (Sima Yi long-game, Cao Cao multi-stakeholder, Liu Bei relationship) → Knowledge (09_BUSINESS/contracting, 06_TIME/long_game, 05_POSITION/leverage_points) → Structure (diagnosis, analysis, 3 options, recommendation, failure modes, confidence).

**Build** (first draft): 2000 words. Recommends accepting with conditions (minimum volume clause, exit clause).

**Review**: Missing — the spiritual dimension (is this tawakkul or risk?), the precedent set, the alternative uses of the 5-year capacity.

**Hunt**: Vulnerability — assumes the developer will be in business for 5 years. What if they fail in year 3?

### Iteration 2

**Fix**: Add the spiritual dimension (tawakkul is action + trust; taking the contract is action; the trust is in Allah for the outcome). Add the precedent analysis (this sets a precedent for other developers). Add the alternative analysis (what else could you do with 5 years of capacity?). Address the developer failure mode (add a clause that releases you if the developer is acquired or fails).

**Build** (second draft): 3500 words. More comprehensive.

**Review**: Missing — the competitor response (what will competitors do when they see this exclusivity?).

**Hunt**: Vulnerability — the analysis assumes competitors are passive. They will respond.

### Iteration 3

**Fix**: Add the competitor response analysis (they may try to break the exclusivity, undercut on non-exclusive work, or poach the developer's other contractors). Add the conditions under which the answer would be wrong (if the developer is in financial trouble, if the user's team cannot scale, if the user's spiritual life is compromised by the workload).

**Build** (third draft): 4800 words. Addresses most angles.

**Review**: The argument structure could be tighter. The recommendation could be more specific.

**Hunt**: The minimum volume clause recommendation is vague — what specific volume?

### Iteration 4

**Fix**: Tighten the structure. Specify the minimum volume (calculate it based on the user's capacity). Add the final source citations. Calibrate the confidence (MEDIUM, not HIGH, because the developer's 5-year stability is uncertain). Add the "what I still don't know" section.

**Build** (final draft): 5200 words. Quality 92-95% of optimal.

**Converge**: 4 iterations complete. Diminishing returns reached. Deliver.

---

## The Anti-Patterns

### Anti-Pattern 1: Single-Pass on High-Stakes

Treating a high-stakes question with a single-pass answer. This is the most common failure. The answer is shallow, the user is under-served.

**Counter**: For any question with high stakes (financial, strategic, ethical, irreversible), run at least 2 iterations.

### Anti-Pattern 2: Infinite Loop

Continuing to iterate past the point of meaningful improvement. Each iteration adds words but not value. The answer bloats without improving.

**Counter**: The 4-iteration maximum is hard. Beyond 4, deliver.

### Anti-Pattern 3: Loop Without Review

Running the loop but skipping the Review stage. The system builds, hunts, fixes, but never reads the answer as the user would. The answer becomes system-centric instead of user-centric.

**Counter**: Always include Review. The Review stage is where the user's perspective is honored.

### Anti-Pattern 4: Loop Without Hunt

Running the loop but skipping the Hunt stage. The system reviews (which is passive) but doesn't hunt (which is active). The answer has gaps but no actively-found flaws.

**Counter**: Always include Hunt. The Hunt stage is where the answer is stress-tested.

### Anti-Pattern 5: Confusing Iteration with Restarting

Each iteration is NOT a fresh start. It's a refinement of the previous draft. If the system is starting over each time, it's not iterating — it's churning.

**Counter**: Each iteration builds on the previous. The previous draft is the input to the next iteration.

---

## The Discipline in One Sentence

**The Iterative Refinement Loop is the discipline of refusing to deliver the first answer to a high-stakes question, and instead improving the answer through 4 structured cycles of plan, build, review, hunt, fix.**

---

## File History

- Created: 2026-09-10
- Version: 1.0
- Review: 2027-03-10
- Source: System design based on iterative improvement practices in writing, software, and strategy
- Confidence: HIGH (the protocol is well-grounded)
- User direction: 4-iteration maximum to prevent paralysis
