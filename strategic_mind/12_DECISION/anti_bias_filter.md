# The Anti-Bias Filter — Explicit Bias Mitigation

> **Layer**: 12_DECISION/
> **File**: anti_bias_filter
> **Subject**: The anti-bias filter — the explicit bias mitigation discipline, covering the 20 most relevant biases for the Egyptian contractor, with trigger/symptom/discipline for each, the pre-decision bias check, the post-decision bias review, and the Islamic dimension (muhasaba as anti-bias discipline)
> **Domain**: Decision — the bias mitigation layer, complementary to the blind spot checker
> **User**: Egyptian Muslim electrical contractor whose decisions are systematically distorted by cognitive biases he is unaware of, and who needs an explicit, operational filter to mitigate them
> **Why this file exists**: The blind spot checker (sister file) catches errors in the reasoning chain. This file catches the systematic distortions in the reasoning itself. The bias catalog (`04_PSYCHOLOGY/cognitive_biases.md`) defines the 20 biases; this file operationalizes them as a discipline: for each bias, when it activates, how to recognize it, and how to mitigate. The discipline is not to be unbiased (impossible) but to know which biases are operative and to design around them.
> **Tier**: Synthesized from the bias catalog (`04_PSYCHOLOGY/cognitive_biases.md`), the self-audit protocol, and classical Islamic muhasabah tradition
> **Provenance**: Synthesized on 2026-09-09 from Tversky & Kahneman's heuristics-and-biases program, the bias catalog's 20 entries, and the classical Islamic tradition of muhasabah (al-Muhasibi, al-Ghazzali, Ibn al-Mubarak). Audit per `00_META/self_audit_protocol.md`. Confidence: MEDIUM-HIGH.

---

## The Premise

Cognitive biases are not failures of intelligence. They are properties of the cognitive architecture that produce fast, approximately-correct answers in familiar environments and systematic errors in unfamiliar or high-stakes environments. The strategic mind does not try to eliminate biases (impossible) but to (a) recognize which biases are operative in which decisions, (b) apply specific debiasing techniques for each, (c) build decision processes that constrain the most dangerous biases through external review, written records, and pre-committed thresholds.

The discipline is not to be unbiased; the discipline is to know which biases you are subject to and to design around them. This file is the design.

For each bias: **Trigger** (when the bias activates in the contractor's decisions), **Symptom** (how to recognize it), **Discipline** (how to mitigate).

---

## The 20 Biases — Trigger, Symptom, Discipline

### 1. Anchoring

**Trigger**: The first number mentioned in a negotiation (the client's first price, the subcontractor's first quote, the supplier's first offer).
**Symptom**: The contractor's counter is closer to the first number than to the contractor's own pre-derived number; the contractor cannot articulate why the first number is wrong, only that it "feels high" or "feels low."
**Discipline**: Before any negotiation, write down your own number, derived from costs and reasonable margin. Negotiate from your number, not from theirs. When hearing an extreme anchor, explicitly consider the opposite ("what if the right number is 50% of theirs?").

### 2. Availability

**Trigger**: A vivid recent event (a project fire, a client's late payment, a competitor's collapse) that dominates memory.
**Symptom**: The contractor over-estimates the probability of the vivid event recurring; over-specifies protection against it; demands aggressive terms from all subsequent counterparties.
**Discipline**: Use base rates, not vividness. Before estimating probability, ask: in a comparable sample, what is the actual frequency? The Federation of Contractors' data or the contractor's own project history is more reliable than the recent memory.

### 3. Confirmation Bias

**Trigger**: A belief has been formed about a counterparty (a subcontractor is unreliable, a client is difficult, a supplier is honest).
**Symptom**: The contractor notices confirming evidence and explains away disconfirming evidence; the belief, once formed, becomes self-protecting; the contractor cannot articulate what would change his mind.
**Discipline**: For every significant belief, ask "what evidence would I have to see to change my mind?" If the answer is "nothing," the belief is identity, not hypothesis. Appoint a "red team" (a peer who argues against) for every significant decision.

### 4. Sunk Cost Fallacy

**Trigger**: A project or relationship has consumed significant past investment (EGP 5M in a losing project, 3 years in a difficult client relationship).
**Symptom**: The contractor continues investing despite negative future returns, because abandoning feels like admitting the past investment was wasted; the past investment dominates the decision instead of the future returns.
**Discipline**: Ask "if I were not already invested, would I start investing today?" If no, abandon — the past is gone regardless. Pre-commit to a "kill threshold" before any major project: "if losses exceed EGP X or delay exceeds Y months, I exit regardless of past investment."

### 5. Overconfidence

**Trigger**: A domain where the contractor has had several successes (3 successful hospital projects → believes the 4th will be easy).
**Symptom**: The contractor's estimates lack adequate contingencies; the bid is aggressive; the planning assumes best-case execution; the contractor says "we've done this before, no problem."
**Discipline**: Track calibration. For every significant estimate, write it down and later compare to actual. After 20-30 estimates, calculate your calibration curve. Most contractors are 30-40% overconfident; adjust downward by that amount.

### 6. Hindsight Bias

**Trigger**: An outcome is known (a project has failed; a project has succeeded).
**Symptom**: The contractor believes the outcome was predictable ("I knew it all along"); assigns blame or credit accordingly; learns the wrong lessons (how to predict what already happened, not how to predict what will happen).
**Discipline**: Document predictions in writing at the time you make them. Review against outcomes not to assign blame but to calibrate. Admit that most outcomes were not predictable; learn from the decision process, not the retroactive narrative.

### 7. Survivorship Bias

**Trigger**: The contractor studies successful contractors, attends conferences, reads success stories.
**Symptom**: The contractor copies the practices of the successful, without seeing that the same practices also produced failures invisible to him; the contractor attributes success to practices that may not have caused it.
**Discipline**: Actively seek the failed cases. For every successful contractor studied, find a failed contractor who did the same things. Ask "what do successful and failed contractors both do, and what actually differentiates them?" Most differentiators are luck and timing.

### 8. Halo Effect

**Trigger**: A single strong positive attribute of a counterparty (well-dressed client, prestigious supplier, one impressive project).
**Symptom**: The contractor judges the counterparty's unrelated attributes positively based on the single strong one; the contractor is surprised when the well-dressed client is financially unreliable or the prestigious supplier is technically inferior.
**Discipline**: Evaluate attributes independently. For each significant counterparty, write separate assessments of each relevant attribute (technical competence, financial reliability, character, schedule discipline). Do not allow one strong attribute to influence the others.

### 9. Framing

**Trigger**: A decision is presented in either a gain frame ("we will deliver on time") or a loss frame ("we will avoid the failures that plagued competitors").
**Symptom**: The contractor's preference shifts with the frame even when the content is identical; the contractor's counterparty's preference also shifts, and the contractor does not notice the frame is doing the work.
**Discipline**: Restate the same problem in both frames and check whether your preference changes. If it does, you are driven by the frame, not the content. For counterparty communications, deliberately choose the frame (loss for cautious, gain for expansive) and do not allow the counterparty to set the frame unopposed.

### 10. Endowment Effect

**Trigger**: The contractor owns something (inventory, an approved design, a long-held contract).
**Symptom**: The contractor values what he owns more than he would value the same thing if he did not own it; he resists selling, scope reductions, or contract changes that are in his financial interest because they are felt as losses.
**Discipline**: Ask "if I did not already own this, would I buy it today at this price?" If no, sell. For counterparty resistance, reframe the change as a non-loss ("the scope is being refined, not reduced").

### 11. Loss Aversion

**Trigger**: A decision involves a potential loss (losing a client, losing a project, losing a margin).
**Symptom**: The contractor weighs the potential loss approximately 2-2.5 times more heavily than the equivalent gain; he passes on positive-expected-value opportunities because the loss looms larger than the gain.
**Discipline**: Audit your resistance to changes for loss aversion: "am I resisting because the change is bad, or because I feel the current state as a loss?" For counterparty persuasion, frame proposals in the loss frame for cautious counterparties and in the gain frame for expansive ones.

### 12. Dunning-Kruger Effect

**Trigger**: The contractor selects subcontractors, suppliers, or hires based on confidence.
**Symptom**: The least competent are the most confident; the most competent under-bid and are self-critical; the contractor selects over-confident incompetent counterparties and under-confident competent ones.
**Discipline**: Do not select on confidence. Select on track record, test projects, reference checks. Calibrate confidence against demonstrated competence — confidence without competence is a warning sign.

### 13. Fundamental Attribution Error

**Trigger**: A counterparty's behavior is negative (a subcontractor delivers late; a client is difficult).
**Symptom**: The contractor attributes the behavior to disposition (the subcontractor is irresponsible; the client is a difficult person) instead of situation (the subcontractor's supply chain failed; the client's company has cash flow trouble). The misattribution produces wrong responses (firing the subcontractor, dropping the client).
**Discipline**: Before judging disposition, ask "what situational pressure would produce this behavior in a normal, well-intentioned person?" If a plausible situational explanation exists, investigate before responding.

### 14. Self-Serving Bias

**Trigger**: A project outcome is known (success or failure).
**Symptom**: The contractor attributes successes to skill ("I delivered well") and failures to external factors ("the client changed scope"). The asymmetry prevents learning — neither successes nor failures produce lessons.
**Discipline**: For every significant outcome, run a counterfactual: "if I had made different choices, would the outcome have been different?" If yes, your choices mattered — examine them. If no, the outcome was largely external — recognize it as such, without taking credit or blame.

### 15. Planning Fallacy

**Trigger**: The contractor estimates time or cost for a future project.
**Symptom**: The estimate is more optimistic than the actual outcome of similar past projects; the contractor says "this time will be different"; contingencies are minimal.
**Discipline**: Use the "outside view" — base the estimate on the actual outcomes of similar past projects, not on the specific optimistic estimate for this project. Multiply initial estimates by your historical overconfidence factor (typically 1.3-1.5x for time, 1.2-1.3x for cost).

### 16. Recency Bias

**Trigger**: A recent event dominates memory (a recent project failure, a recent client's late payment).
**Symptom**: The contractor over-weights the recent event relative to the longer trend; recent data dominates the decision.
**Discipline**: Force explicit weighing of older data. For any decision based on recent events, also list the comparable events from 6, 12, and 24 months ago. The longer trend is usually more reliable than the recent spike.

### 17. Status Quo Bias

**Trigger**: A decision involves changing the current state (switching suppliers, changing pricing structure, replacing a foreman).
**Symptom**: The contractor resists the change even when the change has positive expected value; the current state feels safer than it is; the cost of change is overweighted.
**Discipline**: Ask "if I were starting today, would I choose the current state?" If no, the current state is preserved only by bias — change it. Use a default rotation: periodically review whether current arrangements (suppliers, prices, processes) would be chosen if starting fresh.

### 18. Bandwagon Effect

**Trigger**: Many contractors in the market are doing the same thing (bidding low to win work, taking exclusive contracts, entering a particular market).
**Symptom**: The contractor joins the bandwagon because "everyone is doing it"; the contractor cannot articulate why the bandwagon move is right for his specific situation.
**Discipline**: Before joining any bandwagon, ask "what would have to be true for this to be right for me specifically?" If you cannot articulate the specific reasoning, the bandwagon is doing your thinking for you. Stand aside; let the bandwagon pass; assess the survivors and the casualties.

### 19. Reciprocity Bias

**Trigger**: A counterparty has done the contractor a favor (a client who extended payment terms, a supplier who gave a discount, a subcontractor who worked late).
**Symptom**: The contractor reciprocates beyond what the favor warrants (gives the client a larger discount later, accepts the supplier's later price increase, awards the subcontractor extra work at higher rates). The reciprocity produces misallocation.
**Discipline**: For each favor, calculate its market value (what would the equivalent cost on the open market?). Reciprocate at market value, not at felt value. The felt value is inflated by reciprocity bias.

### 20. Authority Bias

**Trigger**: An authority figure (a senior contractor, a government official, a religious scholar, a wealthy client) voices an opinion.
**Symptom**: The contractor defers to the authority beyond what the authority's expertise justifies; the authority's opinion dominates even outside his domain.
**Discipline**: For each authority opinion, ask "what is this person's actual domain of expertise, and is this question within it?" A senior contractor's opinion on contracting is authoritative; his opinion on aqeedah is not. A scholar's opinion on fiqh is authoritative; his opinion on business strategy is not. Restrict authority to domain.

---

## The Pre-Decision Bias Check

Before any consequential decision (per the classification in `situation_diagnosis.md` — strategic, tactical with high stakes), run the pre-decision bias check:

1. **Identify the top 3-5 biases most likely to be active in this decision.** Use the triggers above. For a bid decision: anchoring (the client's first number), overconfidence (the contractor's estimate), planning fallacy (time/cost estimate), confirmation (the contractor's preferred subcontractor). For a hire decision: halo effect (one strong impression), Dunning-Kruger (the candidate's confidence), fundamental attribution (the candidate's past behavior interpreted as disposition).

2. **For each identified bias, articulate the specific symptom you would see if it were active.** "If I am anchored, my counter would be closer to X than to my pre-derived number. If I am overconfident, my estimate would lack the 30% contingency my calibration suggests."

3. **Apply the specific discipline for each identified bias.** Write down your pre-derived number; check your calibration curve; use the outside view for estimates; appoint a red team.

4. **Document the bias check in writing.** A bias check not written is a bias check not done. The discipline is the written record, which becomes evidence for the post-decision review.

The pre-decision bias check takes 15-30 minutes for a consequential decision. The cost is small; the cost of not checking is potentially EGP millions.

---

## The Post-Decision Bias Review

After the outcome of a consequential decision is known, run the post-decision bias review:

1. **Compare the actual outcome to the pre-decision estimate.** Did the project come in on time, on budget? Was the client reliable? Was the subcontractor's quality as expected?

2. **Identify the biases that were operative in the pre-decision.** Which of the 20 biases actually distorted the decision? (Compare the pre-decision bias check's identification with what actually happened.)

3. **For each identified bias, assess the discipline's effectiveness.** Did the discipline mitigate the bias? If yes, the discipline worked; reinforce it. If no, the discipline was insufficient; strengthen it.

4. **Update the calibration record.** Add the actual outcome to the calibration database. After 20-30 entries, the calibration curve becomes reliable. The contractor learns his own bias profile.

5. **Identify new biases not previously checked.** The 20-bias list is not exhaustive; specific situations may surface biases not on the list. Document them.

The post-decision bias review is the discipline that compounds. Each review improves the next decision. After 5 years of disciplined reviews, the contractor's bias profile is well-mapped and his decision quality has improved substantially. Without the review, the same biases recur for 5 years with no improvement.

---

## The Islamic Dimension — Muhasabah as Anti-Bias Discipline

The Islamic concept of **muhasabah** (self-accounting) is the spiritual form of the anti-bias discipline. The Prophet ﷺ said: "The intelligent person is the one who takes account of himself and works for what comes after death" (Tirmidhi, narrated from Ibn Umar). Umar ibn al-Khattab said: "Take account of yourselves before you are taken to account; weigh your deeds before they are weighed for you" (narrated by al-Tirmidhi).

Muhasabah is the daily, weekly, and annual review of one's own actions, intentions, and states. It includes:
- **Daily muhasabah** (before sleep): what did I do today? What was my intention? What did I do wrong? What should I do tomorrow?
- **Weekly muhasabah** (Friday): what did I do this week? What were my patterns? What should I change?
- **Annual muhasabah** (Ramadan): what did I do this year? Where am I relative to where I should be? What is my plan for the next year?

The structural parallel to the anti-bias discipline:
- **Daily muhasabah** ↔ the post-decision bias review (small, frequent, corrective)
- **Weekly muhasabah** ↔ the multi-decision review (patterns, not just events)
- **Annual muhasabah** ↔ the calibration update (long-term, structural)

The Islamic discipline adds what the secular bias literature does not: **the intention behind the action**. The bias literature examines the cognitive distortion; the Islamic discipline examines the nafs (lower self) that drives the distortion. The contractor who debiases his decisions but does not examine the greed that drove the overconfidence, or the fear that drove the loss aversion, or the laziness that drove the status quo bias, has treated the symptom but not the disease.

The integrated discipline: for each bias identified, also identify the spiritual root. Overconfidence is rooted in kibr (pride). Loss aversion is rooted in hirs (greed) and fear of poverty (the opposite of tawakkul). Sunk cost is rooted in attachment to the world. Confirmation bias is rooted in narcissism (the belief that one's existing view is correct). The debiasing discipline is most effective when paired with the spiritual discipline of removing the root.

**The contractor's daily muhasabah for decisions**: before sleep, the contractor reviews the day's decisions. For each significant decision, he asks:
1. What bias might have been active?
2. What was the spiritual root?
3. Did I apply the discipline?
4. What will I do differently tomorrow?

This is the integration: the cognitive discipline (the 20-bias filter) and the spiritual discipline (muhasabah), working together. The contractor who does both for 5 years becomes both a better decision-maker and a better Muslim.

---

## The Discipline in One Page

1. **Anchoring**: write your own number first.
2. **Availability**: use base rates, not vividness.
3. **Confirmation**: ask "what would change my mind?"
4. **Sunk cost**: ask "would I start investing today?"
5. **Overconfidence**: track calibration; adjust by your historical overconfidence factor.
6. **Hindsight**: document predictions; learn from process, not narrative.
7. **Survivorship**: seek the failed cases, not just the successful.
8. **Halo**: evaluate attributes independently.
9. **Framing**: restate in both frames; check whether your preference changes.
10. **Endowment**: ask "would I buy this today?"
11. **Loss aversion**: audit resistance for the loss frame.
12. **Dunning-Kruger**: do not select on confidence.
13. **Fundamental attribution**: ask "what situational pressure would produce this in a normal person?"
14. **Self-serving**: run counterfactuals on both successes and failures.
15. **Planning fallacy**: use the outside view; multiply by historical overconfidence.
16. **Recency**: force explicit weighing of older data.
17. **Status quo**: ask "would I choose the current state if starting fresh?"
18. **Bandwagon**: ask "would this be right for me specifically?"
19. **Reciprocity**: reciprocate at market value, not felt value.
20. **Authority**: restrict authority to domain.

Pre-decision: identify the top 3-5 active biases; articulate symptoms; apply disciplines; document.
Post-decision: compare outcome to estimate; identify operative biases; assess discipline effectiveness; update calibration; identify new biases.
Islamic dimension: muhasabah daily, weekly, annually — paired with the spiritual root of each bias (kibr for overconfidence, hirs for loss aversion, attachment for sunk cost, narcissism for confirmation).

---

## Common Pitfalls

**Pitfall 1: Bias check as theater.** Listing the biases without engaging with the specific symptoms and disciplines. If you cannot articulate the specific symptom you would see if the bias were active, you have not checked for it.

**Pitfall 2: Bias check on only high-stakes decisions.** The biases operate in every decision. The high-stakes decisions are where the cost is highest, but the small decisions compound. Run a light bias check on tactical decisions, not just strategic ones.

**Pitfall 3: Forgetting the post-decision review.** The pre-decision check catches biases prospectively; the post-decision review catches them retrospectively and updates calibration. Without the review, the pre-decision check becomes rote. The review is what makes the pre-decision check better next time.

**Pitfall 4: Treating biases as separate from spiritual state.** The cognitive discipline and the spiritual discipline are one. The contractor who debiases his decisions but does not treat his kibr, his hirs, his attachment, has treated the symptom. The integration is the discipline.

**Pitfall 5: Believing one can become unbiased.** The biases are properties of the cognitive architecture; they cannot be eliminated. The discipline is to know which are operative and to design around them — not to aspire to a state one cannot reach.

---

## File History

- Created: 2026-09-09
- Version: 1.0
- Source: `04_PSYCHOLOGY/cognitive_biases.md` (the bias catalog), `00_META/self_audit_protocol.md`, `00_META/confidence_scoring.md`, classical Islamic muhasabah tradition (al-Muhasibi's "Kitab al-Ri'ayah"; al-Ghazzali's "Ihya Ulum al-Din"; Ibn al-Mubarak's "Kitab al-Zuhd"), Tversky & Kahneman's heuristics-and-biases program. Cross-referenced with `situation_diagnosis.md`, `domain_routing.md`, `mind_routing.md`, `multi_mind_synthesis.md`, `blind_spot_checker.md`.
- Review: 2027-03-09
