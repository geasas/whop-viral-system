# The Thinking Loop — The Complete Pipeline from Question to Best Answer

> **Layer**: 00_META/
> **File**: the_thinking_loop
> **Purpose**: This is the master protocol that integrates all other protocols into a single pipeline: from receiving the question to delivering the best answer the system can produce. This is the system's operating manual in one file.
> **Created**: 2026-09-10
> **Version**: 1.0
> **Review**: 2027-03-10

---

## The Premise

The system has many protocols:
- Deep Question Understanding
- Self-Audit
- Multi-Hypothesis Engine
- Iterative Refinement Loop
- Vulnerability Hunting
- Confidence Scoring
- Mind Routing
- Domain Routing
- Knowledge Gap Protocol

Each is a discipline. But they only produce value when integrated into a single pipeline. This file is that integration.

The Thinking Loop is the master pipeline. Every user question enters the loop. Every answer exits the loop. The loop is what makes the system more than the sum of its parts.

---

## The 12 Stages of the Thinking Loop

The loop has 12 stages. Each stage has a specific input, a specific activity, and a specific output. The stages flow into each other. The loop can iterate (return to earlier stages) up to 4 times for high-stakes questions.

### Stage 0: Question Reception and Initial Framing

**Input**: The user's question (text).

**Activity**:
- Receive the question verbatim.
- Note the surface features (length, specificity, urgency, emotional tone).
- Note the user's likely state (calm, anxious, urgent, exploratory).
- Initial framing: is this a high-stakes or low-stakes question?

**Output**: A question intake note.

**Example**: "User asks: 'Should I take this EGP 5M contract?' — short, direct, high-stakes (financial), user state seems decisive (not anxious, not exploratory). Likely wants a structured analysis."

### Stage 1: Deep Question Understanding

**Input**: The question intake note.

**Activity**: Run the 7 dimensions from `deep_question_understanding.md`:
1. Literal question
2. Implicit question
3. Contextual question
4. Hidden question
5. Counter-intent
6. Risk profile
7. Scope

Apply the 3-tier understanding test (restatement, prediction, counterfactual).

Reframe the question into the actual question the system will answer.

**Output**: The reframed question, with all 7 dimensions documented.

**Example**: Reframed question — "Given the user's expansion phase and EGP 500K capital, is taking a EGP 5M contract a sound strategic acceleration or financially reckless over-extension? What conditions make it sound, and what failure modes if conditions aren't met?"

### Stage 2: Situation Diagnosis

**Input**: The reframed question.

**Activity**: Run `12_DECISION/situation_diagnosis.md`:
- What kind of decision is this? (strategic, tactical, operational, ethical, personal)
- What is the time horizon? (immediate, short, medium, long, generational)
- What is the stake? (reversible vs irreversible)
- What are the parties involved?

**Output**: A diagnostic summary.

**Example**: "Strategic decision (multi-year implications), medium-to-long time horizon, partially irreversible (reputation and 5-year commitment), multiple stakeholders (user, team, client, family, competitors)."

### Stage 3: Mind and Domain Routing

**Input**: The diagnostic summary.

**Activity**: Run `12_DECISION/mind_routing.md` and `12_DECISION/domain_routing.md`:
- Which character minds apply? (typically 2-3 for high-stakes questions)
- Which knowledge domains apply? (business, personal, strategic, ethical, learning)
- Should multiple minds be synthesized? (see `12_DECISION/multi_mind_synthesis.md`)

**Output**: A routing decision — which minds and which knowledge layers to invoke.

**Example**: "Minds: Sima Yi (long-game patience), Cao Cao (multi-stakeholder), Liu Bei (relationship dimension). Domains: 09_BUSINESS (cash flow, pricing), 05_POSITION (leverage), 06_TIME (long-game), 10_PERSONAL (spiritual dimension), 14_ETHICS (halal)."

### Stage 4: Hypothesis Generation

**Input**: The reframed question, the routing decision.

**Activity**: Run `00_META/multi_hypothesis_engine.md`:
- Generate 3-5 distinct hypotheses using different minds.
- For each hypothesis: state the claim, the supporting evidence, the refuting evidence, the mechanism, the failure mode, the cost, the ethical footprint.
- Stress-test each hypothesis.
- Compare hypotheses.
- Choose the leading hypothesis and the runner-up.

**Output**: A hypothesis comparison with a leading hypothesis.

**Example**: Hypotheses:
- H1 (Sima Yi): Decline full exclusivity, accept with conditions. (Leading.)
- H2 (Guo Jia): Accept with minimum volume clause. (Runner-up.)
- H3 (Cao Cao): Accept for reputation, then expand.
- H4 (Yuan Fang): Decline and offer preference structure.
- H5 (Lu Bu): Accept on strict terms only.

### Stage 5: Knowledge Retrieval

**Input**: The leading hypothesis, the routing decision.

**Activity**: Pull from the relevant layers:
- 01_CORE: foundational principles
- 02_PERCEPTION: how to read the situation
- 03_ANALYSIS: how to dissect the dynamics
- 04_PSYCHOLOGY: human nature patterns
- 05_POSITION: where the user sits
- 06_TIME: when to move
- 07_MINDS: the specific minds (e.g., sima_yi/worldview.md, sima_yi/signature_moves.md)
- 08_STRATEGY: classical principles
- 09_BUSINESS: domain knowledge (cash flow, pricing, market)
- 10_PERSONAL: spiritual and personal dimensions
- 11_LEARNING: if the question involves learning new things
- 13_CASES: analogous cases
- 14_ETHICS: ethical constraints

For each piece of knowledge, cite the source (with tier annotation per `research_protocol.md`).

**Output**: A knowledge base for the answer, with sources.

### Stage 6: Planning

**Input**: The hypothesis, the knowledge base, the reframed question.

**Activity**: Plan the answer:
- State the answer structure: introduction, diagnosis, analysis, options, recommendation, second-order effects, failure modes, confidence, sources, gaps.
- Identify which minds will be invoked explicitly.
- Identify which knowledge will be cited.
- Estimate the answer length.
- Decide whether to iterate (high-stakes: yes, plan for 4 iterations; low-stakes: no, single pass).

**Output**: A one-paragraph plan for the answer.

### Stage 7: Building (First Draft)

**Input**: The plan.

**Activity**: Write the first draft of the answer:
- Follow the planned structure.
- Cite all sources with tier annotations.
- Apply the minds explicitly.
- Include failure modes and second-order effects.
- State the confidence level.

**Output**: The first draft of the answer.

### Stage 8: Review

**Input**: The first draft.

**Activity**: Read the draft as the user would:
- Identify gaps (what should be in the answer that isn't?)
- Identify confusions (what would the user misunderstand?)
- Identify weak arguments (what wouldn't convince a skeptic?)
- Identify missing perspectives (which minds weren't invoked but should have been?)
- Identify missing sources (what claims aren't backed?)

**Output**: A list of improvements to make.

### Stage 9: Vulnerability Hunting

**Input**: The first draft.

**Activity**: Run `00_META/vulnerability_hunting.md`:
- Apply the 5 vulnerability types (logical, factual, ethical, strategic, operational).
- Apply the 4 hunting exercises (Red Team, Smart Critic, Stress Test, Inversion).
- Compile the vulnerability list, prioritized by severity.

**Output**: A list of vulnerabilities to address.

### Stage 10: Fixing and Iterating

**Input**: The improvements list (Stage 8) and the vulnerabilities list (Stage 9).

**Activity**:
- Address each improvement and vulnerability.
- Either fix (modify the answer), hedge (add a caveat), acknowledge (state the limit), or defend (if the vulnerability is not actually a flaw).
- Re-read the answer end-to-end.

**Iteration decision**:
- If substantial improvements were made AND clear improvements remain → loop back to Stage 8 (Review).
- If substantial improvements were made AND no clear improvements remain → proceed to Stage 11.
- If minimal improvements were made → proceed to Stage 11.
- If 4 iterations reached → proceed to Stage 11 (per `iterative_refinement_loop.md`).

**Output**: The improved draft.

### Stage 11: Final Audit

**Input**: The improved draft.

**Activity**: Run `00_META/self_audit_protocol.md`:
- The Premise Check: are all premises stated?
- The Multiple-Hypothesis Check: were alternatives considered?
- The Source Check: are all claims sourced?
- The Counterfactual Check: what would make this wrong?
- The Bias Check: which biases might be active?
- The Ethics Check: does this cross any red line?
- The Confidence Check: what confidence level is honest?

Apply `00_META/confidence_scoring.md` to calibrate confidence.

**Output**: The audited answer, with confidence level.

### Stage 12: Delivery

**Input**: The audited answer.

**Activity**: Deliver the answer to the user in the structured format:
1. **Reframed question** (what I understood you to ask, with a request to correct if wrong)
2. **Diagnosis** (what kind of decision this is)
3. **Reasoning** (which minds I used, why, and the analysis)
4. **Multiple options** (with pros, cons, risks)
5. **Recommendation** (the leading hypothesis, with the runner-up as alternative)
6. **Second-order effects** (what happens after)
7. **Confidence level** (low/medium/high, with explanation)
8. **Source provenance** (which files, which sources)
9. **Vulnerabilities considered** (the major ones, briefly)
10. **What I still don't know** (explicit gaps)
11. **Follow-up suggestions** (what to monitor, what to ask next)

**Output**: The final answer delivered to the user.

---

## The Loop in Iteration

For high-stakes questions, the loop iterates. The iteration pattern:

- **First pass**: Stages 0-12. Produces a first answer.
- **Second pass**: Stages 8-11 again (Review, Hunt, Fix, Audit). Improves the answer.
- **Third pass**: Stages 8-11 again. Further improves.
- **Fourth pass**: Stages 8-11 again. Final polish.

After the fourth pass, deliver (Stage 12). The 4-iteration maximum is per `iterative_refinement_loop.md` and prevents paralysis.

For low-stakes questions, the loop runs once: Stages 0-12, with lighter versions of Stages 8-11.

---

## Worked Example

**User question**: "Should I take this EGP 5M contract with EGP 500K capital?"

### Stage 0: Question Reception

Short, direct, high-stakes (5M is 10x capital), user seems decisive.

### Stage 1: Deep Understanding

- Literal: should the user bid on a EGP 5M project with EGP 500K capital?
- Implicit: is this a smart risk or reckless?
- Context: expansion phase, halal constraint, Egyptian market 2026
- Hidden: what if payment delays? What else could the capital do? What precedent?
- Counter-intent: not asking to lie, not asking to abandon other work
- Risk: high financial, medium reputational, high strategic
- Scope: deep analysis warranted (high-stakes)

Reframed question: "Given the user's expansion phase and EGP 500K capital, is taking a EGP 5M contract a sound strategic acceleration or financially reckless over-extension? What conditions make it sound, and what failure modes if conditions aren't met?"

### Stage 2: Diagnosis

Strategic decision, multi-year horizon, partially irreversible (reputation), multiple stakeholders.

### Stage 3: Routing

Minds: Sima Yi (long-game), Cao Cao (multi-stakeholder), Liu Bei (relationship), Guo Jia (decisive if window closing).
Domains: 09_BUSINESS/contracting/cash_flow_zero_capital.md, 09_BUSINESS/contracting/pricing_methodology.md, 05_POSITION/asymmetric_strategy.md, 10_PERSONAL/spiritual/rizq_and_tawakkul.md, 14_ETHICS/red_lines.md.

### Stage 4: Hypotheses

- H1 (Sima Yi + 09_BUSINESS cash flow): Take the contract IF client agrees to 25% advance + supplier credit + subcontractor deferral. Decline otherwise.
- H2 (Guo Jia): Take the contract NOW if the window is closing, with strict cash flow conditions.
- H3 (Cao Cao): Take the contract AND simultaneously build the capital base through other work.
- H4 (Yuan Fang): Decline; offer a partnership structure that shares the risk.
- H5 (Liu Bei): Take only if the client relationship is worth the financial risk.

Leading: H1 (the conditional acceptance). Runner-up: H4 (the partnership structure).

### Stage 5: Knowledge Retrieval

Pull from:
- 09_BUSINESS/contracting/cash_flow_zero_capital.md — the "client's money" model
- 09_BUSINESS/contracting/pricing_methodology.md — typical project margins
- 07_MINDS/sima_yi/worldview.md — patience as weapon
- 07_MINDS/sima_yi/signature_moves.md — Refusing Battle to Win the War
- 05_POSITION/asymmetric_strategy.md — when weaker, change the game
- 10_PERSONAL/spiritual/rizq_and_tawakkul.md — the spiritual dimension of risk
- 14_ETHICS/red_lines.md — ethical constraints on negotiation

### Stage 6: Plan

Structure:
1. Reframed question
2. Diagnosis (high-stakes, multi-year, multi-stakeholder)
3. The 5 hypotheses (briefly)
4. The leading hypothesis with reasoning (cash flow structure analysis)
5. The runner-up (partnership structure)
6. The conditions under which the leading hypothesis works (25% advance, supplier credit, team capacity)
7. The failure modes (advance refused, payment delay, team overload)
8. The second-order effects (precedent, signal to competitors, opportunity cost)
9. The spiritual dimension (tawakkul is action + trust)
10. Confidence: MEDIUM (the structure is sound but conditions need verification)
11. Sources
12. Vulnerabilities considered
13. What I still don't know

Plan for 4 iterations (high-stakes).

### Stage 7: Build (First Draft)

[2000-word first draft written.]

### Stage 8: Review

Gaps: didn't address the spiritual dimension explicitly. Didn't address the precedent set. Didn't address the alternative uses of the capital.

Confusions: the term "working capital" wasn't defined.

Weak arguments: the 25% advance claim needs a source.

Missing perspectives: didn't invoke Liu Bei for the relationship dimension.

### Stage 9: Hunt

Logical vulnerability: assumes the 25% advance is the norm — what if client refuses?

Factual vulnerability: the 25% advance claim is from 2024 data; may be different in 2026.

Ethical vulnerability: didn't address whether the contract terms are fair to the client.

Strategic vulnerability: didn't consider what competitors will do if I take this project.

Operational vulnerability: didn't address whether the team has capacity for this project size.

Red Team: the case for NOT taking the contract is strong if (a) the client is in financial trouble, (b) the team is already at capacity, (c) the user has a better opportunity in 6 months.

Smart Critic: a senior contractor would say "you've analyzed the bid but not the chain of decisions."

Stress Test: the answer is wrong if (a) payment delays 60+ days (probability 30%), (b) better opportunity in 6 months (probability 20%), (c) team can't scale (probability 25%).

Inversion: what would guarantee getting this wrong? Acting on incomplete information, ignoring precedent, optimizing for short-term.

### Stage 10: Fix and Iterate

Address each gap, confusion, weak argument, missing perspective, and vulnerability.

Add: spiritual dimension (tawakkul = action + trust, the action is the bid, the trust is in Allah).
Add: precedent analysis (taking 10:1 sets a precedent).
Add: alternative uses of capital (what else could EGP 500K do).
Define working capital.
Cite the 25% advance claim (with 2024 source and 2026 caveat).
Invoke Liu Bei for the relationship dimension.
Address the client failure mode (add a clause for client financial trouble).
Address the competitor response (they will undercut or poach).
Address the team capacity (add a capacity check).

[Second draft: 3500 words.]

Iteration 2: Review, Hunt, Fix again.

[Third draft: 4800 words.]

Iteration 3: Review, Hunt, Fix again.

[Fourth draft: 5200 words.]

Iteration 4: Polish.

[Final draft: 5200 words, tightened.]

### Stage 11: Final Audit

Premise Check: all premises stated (yes — assuming user wants to maximize profit AND build reputation AND maintain halal practice).
Multiple-Hypothesis Check: yes (5 hypotheses, 2 retained).
Source Check: all claims sourced.
Counterfactual Check: stated (3 conditions that would make the answer wrong).
Bias Check: anchoring on the 25% advance norm flagged; overconfidence on the structure flagged.
Ethics Check: the recommendation is halal; the negotiation is fair.
Confidence Check: MEDIUM (the structure is sound, but conditions need verification).

### Stage 12: Delivery

Deliver the structured answer with all 11 elements (reframed question, diagnosis, reasoning, options, recommendation, second-order effects, confidence, sources, vulnerabilities, gaps, follow-up).

---

## The Discipline in One Sentence

**The Thinking Loop is the complete pipeline from a user's question to the best answer the system can produce: understand deeply, route intelligently, hypothesize multiple, retrieve knowledge, plan, build, review, hunt vulnerabilities, fix, audit, deliver.**

---

## When to Use the Full Loop

- High-stakes questions: full 12-stage loop with 4 iterations.
- Medium-stakes: full 12-stage loop with 2 iterations.
- Low-stakes: lighter version (Stages 0-7, 11, 12 only).
- Definitional or factual: single-pass answer, no loop.

The discipline: match the depth to the stakes. Don't use a 4-iteration loop on a definitional question. Don't use a single-pass on a high-stakes strategic decision.

---

## File History

- Created: 2026-09-10
- Version: 1.0
- Review: 2027-03-10
- Source: Integration of all 00_META protocols into a single pipeline
- Confidence: HIGH
