# Blind Spot Checker — The Pre-Output Audit

> **Layer**: 12_DECISION/
> **File**: blind_spot_checker
> **Subject**: The blind spot checker — the structured pre-output audit that catches errors before they reach the user; the 7-question blind spot check, the bias check, the counterfactual check, the source check, the ethics check, and the confidence calibration
> **Domain**: Decision — the final audit layer before any answer is delivered
> **User**: Egyptian Muslim electrical contractor whose decisions must be audited before action, because the cost of a wrong decision exceeds the cost of an audit
> **Why this file exists**: Even after diagnosis, routing, mind synthesis, and bias filtering, the answer can be wrong. The wrongness hides in the blind spots — the things the reasoning did not consider, the assumptions it did not state, the sources it did not verify, the counterfactuals it did not test. This file is the structured pre-output audit that catches what the prior steps missed. It is the last firewall before delivery.
> **Tier**: Synthesized from the self-audit protocol (`00_META/self_audit_protocol.md`), the bias catalog (`04_PSYCHOLOGY/cognitive_biases.md`), the ethics layer (`14_ETHICS/`), and the confidence scoring system (`00_META/confidence_scoring.md`)
> **Provenance**: Synthesized on 2026-09-09 from the self-audit protocol, the multi-hypothesis engine, the bias catalog, classical Islamic muhasabah (self-accounting) tradition, and the scientific falsification tradition (Popper). Audit per `00_META/self_audit_protocol.md`. Confidence: MEDIUM-HIGH.

---

## The Premise

The blind spot is the thing that would change the answer if it were seen. Most wrong answers are not wrong because the reasoning is flawed — they are wrong because the reasoning is incomplete. The blind spot checker is the structured interrogation that asks: what did I not see? What did I not check? What did I assume?

This file is the discipline: seven checks, run before any answer is delivered. The checks are not optional. The check that feels most unnecessary (because the answer "feels right") is the check most needed — that feeling is the symptom of overconfidence, which is the most common blind spot.

The blind spot checker is the operational form of the self-audit protocol (`00_META/self_audit_protocol.md`). The audit protocol defines the discipline; this file operationalizes it as the pre-output check.

---

## The 7-Question Blind Spot Check

### Check 1: The Premise Check

What premise is the answer resting on? Is it stated or implicit? If implicit, state it. If the user disagrees with the premise, the answer changes.

The premises to interrogate:
- "I'm assuming the user's goal is X." (Could be Y instead.)
- "I'm assuming the time horizon is Z." (Could be different.)
- "I'm assuming the risk tolerance is W." (Could be higher or lower.)
- "I'm assuming the other party's interest is V." (Could be different.)
- "I'm assuming the market conditions are A." (Could change.)

**The application**: The contractor asks "should I bid this project at EGP 5M?" The premise is "the user wants to maximize profit on this project." But the user might want to maximize relationship value with the developer (in which case a lower margin with better terms is better). Or the user might want to test pricing power (in which case a higher bid that loses is informative). The premise must be stated. If it's wrong, the answer changes.

**Failure mode**: the premise is wrong but the user can't see it because the premise was never stated. The answer is delivered; the user acts on it; the user discovers the premise was wrong; the answer was wrong.

### Check 2: The Multiple-Hypothesis Check

Did the answer consider multiple hypotheses, or did it anchor on the first plausible one?

For any strategic question, there should be 3-5 distinct hypotheses considered, with the leading one selected and the runner-up noted. (See `00_META/multi_hypothesis_engine.md` for the full protocol.)

**The application**: The contractor asks "should I take this exclusive contract?" The first answer that came to mind was "yes, it locks in revenue." The hypothesis engine produces 5 hypotheses (per the worked example in the multi_hypothesis_engine file). The leading hypothesis is "accept with minimum-volume clause." The runner-up is "negotiate right of first refusal." The rejected are listed with reasons. The blind spot check verifies: were these hypotheses generated, or did the answer jump to the first?

**Failure mode**: the answer is the first plausible one, with no alternatives considered. The first plausible is rarely the best.

### Check 3: The Bias Check

Which cognitive biases might be active? (See `04_PSYCHOLOGY/cognitive_biases.md` for the full catalog and `anti_bias_filter.md` for the explicit bias filter.)

The biases to check:
- Anchoring: did I overweight the first piece of information (the first price, the first supplier quote, the first impression of the client)?
- Availability: did I overweight recent or vivid examples (the last project that failed, the last client who paid late)?
- Confirmation: did I favor evidence that confirms my initial hypothesis?
- Sunk cost: did I overweight prior investment in the analysis (time spent, prior decisions made in the same direction)?
- Overconfidence: did I express more certainty than the evidence supports?
- Hindsight: did I judge a past decision by its outcome rather than its reasoning?
- Survivorship: did I overweight success stories and ignore failures?
- Halo effect: did I overweight one positive trait to assume others (the developer has a good brand, so I assume they pay on time)?
- Loss aversion: did I overweight the potential loss relative to the equivalent gain (fear of losing EGP 1M vs opportunity to gain EGP 1M)?
- Recency: did I overweight the most recent event (the most recent project) over the longer trend?

**The application**: The contractor is considering declining a project because the last similar project failed. Check: availability bias — the failure is recent and vivid, but the failure rate of similar projects may be 10%, not 80%. Counter-evidence: the failed project had a specific problem (the client's cash crunch) that doesn't apply here. Revised answer: investigate the current client's cash position before deciding.

**Failure mode**: the answer is biased and the bias is invisible to the answerer. The bias check forces it into the open.

### Check 4: The Counterfactual Check

What would have to be true for the answer to be wrong?

If the answerer cannot articulate this, the answer has not been thought hard enough about.

**The application**: The recommendation is "accept the contract with the minimum-volume clause." What would make this wrong?
- The client's financial situation is worse than it appears (the minimum-volume clause is unenforceable if they're bankrupt).
- The minimum-volume calculation is wrong (the contractor commits capacity for revenue that doesn't cover the cost).
- The exclusivity blocks other opportunities that would have been more profitable.
- The 5-year commitment extends beyond the contractor's ability to execute at the required scale (the team cannot grow fast enough).
- The market shifts such that the developer's projects become unprofitable, and the minimum volume is honored but the project margins are negative.

If any of these are true, the answer is wrong. The counterfactual check identifies what to verify before accepting the answer.

**Failure mode**: the answer is delivered without the counterfactuals articulated, and the user cannot evaluate the conditions under which the answer fails. The user acts with false confidence.

### Check 5: The Source Check

Every claim in the answer must be traceable to a source. The sources:
- A specific file in the STRATEGIC_MIND system (which itself cites its sources)
- A direct source the answerer can name (a book, a scholar, a regulation, a market report)

If a claim has no source, it is a guess. Mark it as such.

**The application**: The answer includes the claim "Egyptian subcontractor rates are typically 20-30% of contract value." The source check asks: where did this come from? If from `09_BUSINESS/contracting/subcontractor_management.md` (Tier 3, practitioner-based), cite it. If from a market report (Tier 4), cite it. If from the answerer's general sense without verification, flag: "based on general contracting principles, not a specific Egyptian source; verify with a recent market check."

**Failure mode**: the answer presents guesses as facts, and the user cannot distinguish the verified from the unverified.

### Check 6: The Ethics Check

Does the answer cross any ethical red line?

Consult `14_ETHICS/`:
- `red_lines.md`: does this cross a non-negotiable line (riba, deception of innocents, harm to non-consenting third parties)?
- `honesty_in_deception.md`: does this involve deception, and if so, of whom, and is it permissible?
- `harm_minimization.md`: does this harm non-consenting third parties?
- `long_term_reputation.md`: does this trade long-term reputation for short-term gain?
- `manipulation_vs_strategy.md`: does this use manipulation where straightforward strategy would work?

If the answer fails any check, either refuse the question, modify the answer, or offer an ethical alternative.

**The application**: The answer recommends accepting a contract whose terms the contractor plans to interpret loosely (use cheaper materials than the client expects). The ethics check catches: this is deception by ambiguity. The answer must be modified — either disclose the materials explicitly or use the specified materials. No third option is both ethical and reputationally sound.

**Failure mode**: the answer is ethical in appearance but unethical in substance (the deception is in the unstated assumption, not in the stated term). The ethics check must examine the substance, not just the surface.

### Check 7: The Confidence Calibration

Given all the above, what confidence level is honest?

- **High**: multiple Tier 1-2 sources agree, no contradictions, premises explicit and verified, no ethics issues, no significant bias risks.
- **Medium**: sources agree with caveats, OR premises need user verification, OR minor bias risks identified.
- **Low**: single-source, OR significant expert disagreement, OR premises are guesses, OR ethical gray zone.

State the confidence explicitly. Do not bury it.

**The application**: After running checks 1-6 on the recommendation "accept with minimum-volume clause," the confidence calibration:
- Premises: stated, but require user verification (the client's financial position is assumed, not verified) → reduces confidence.
- Hypotheses: 5 generated, leading and runner-up noted → supports confidence.
- Biases: anchoring on the rate reduction, loss aversion on losing the deal — both flagged → reduces confidence.
- Counterfactuals: 5 articulated, all require verification → reduces confidence.
- Sources: the cash flow analysis is from `09_BUSINESS/contracting/cash_flow_zero_capital.md` (Tier 3); the halal finance check is from `09_BUSINESS/halal_business/riba_free_finance.md` (Tier 1) → mixed tier → medium confidence.
- Ethics: clean, no red lines → supports confidence.

Overall: MEDIUM confidence. The structure is sound, but the client's financial position must be verified before the answer is acted upon.

**Failure mode**: the answer is delivered with implied high confidence when the evidence supports only medium. The user acts with more confidence than the evidence warrants.

---

## The Blind Spot Check in Practice — A Worked Example

**The answer to be audited**: "Counter the developer's offer at 5% rate reduction (not 20%), with a 7-year commitment, airtight minimum-volume and guaranteed-payment clauses, conditional on verified financial stability and 10-year plan compatibility."

### Check 1: Premise

Stated premises:
- The user's goal is to maximize long-term capacity utilization while preserving pricing power.
- The time horizon is 10 years (the contractor's strategic plan).
- The user's risk tolerance is moderate (willing to commit 5 years but not 10).
- The developer's interest is cost certainty and reliable delivery.
- The market is stable (no major macro shifts expected in the next 12 months).

Each is stated. If the user disagrees with any, the answer changes.

### Check 2: Multiple hypotheses

5 hypotheses generated:
1. Accept at 20% reduction (rejected: precedent compounds, signals weakness)
2. Decline outright (rejected: premature without verification)
3. Counter at 5% reduction with longer commitment (selected)
4. Negotiate right of first refusal (runner-up)
5. Accept at standard rate (rejected: developer will not accept)

The leading and runner-up are noted. ✓

### Check 3: Biases

- Anchoring: the 20% reduction was the first number; the 5% counter could be anchored to it. Counter-evidence: the 5% is based on the contractor's actual cost structure, not on the developer's number. Mitigation: re-derive the 5% from costs, not from the 20%.
- Loss aversion: fear of losing the deal could push toward accepting the 20%. Mitigation: explicit consideration of the cost of accepting (5 years of compounded rate erosion) vs the cost of declining (one lost deal).
- Halo effect: the developer's good brand could bias toward trusting their stability. Mitigation: the Dong Zhuo precondition (verify financial stability) is explicit.

### Check 4: Counterfactuals

What would make this wrong?
- The developer is in worse financial shape than appears (mitigation: the Dong Zhuo precondition verifies this)
- The minimum-volume calculation is wrong (mitigation: re-derive from the contractor's cost structure, not from the developer's number)
- The exclusivity blocks more profitable opportunities (mitigation: the Cao Cao precondition checks 10-year plan compatibility)
- The contractor cannot execute at the required scale (mitigation: verify team capacity before signing)
- The market shifts such that the developer's projects become unprofitable (mitigation: a force-majeure clause that allows renegotiation if macro conditions shift)

Each counterfactual has a mitigation. The answer is robust to the counterfactuals, conditional on the mitigations.

### Check 5: Sources

- Cash flow analysis: `09_BUSINESS/contracting/cash_flow_zero_capital.md` (Tier 3)
- Halal finance check: `09_BUSINESS/halal_business/riba_free_finance.md` (Tier 1)
- Islamic commercial fiqh: `09_BUSINESS/halal_business/islamic_commercial_fiqh.md` (Tier 1)
- Egyptian market norms: `09_BUSINESS/contracting/egypt_electrical_market.md` (Tier 4)
- Sima Yi's patience: `07_MINDS/sima_yi/when_to_activate.md` (Tier 2, derived from manga + classical)
- Cao Cao's integration: `07_MINDS/cao_cao/when_to_activate.md` (Tier 2)
- The "20% reduction compounds" claim: derived from the precedent analysis, not from a specific source → flag as judgment-based.

The flagged claim (the precedent compounding) is judgment-based. The confidence calibration reflects this.

### Check 6: Ethics

- Red lines: no riba (the contract is fee-for-service, not interest-bearing); no deception of innocents (the counter-offer is transparent); no harm to non-consenting third parties (the contract affects only the contractor and the developer) → clean.
- Long-term reputation: the counter-offer builds reputation (principled negotiation); the acceptance at 20% reduction would erode reputation (signals weakness) → the counter is reputation-positive.
- Manipulation vs strategy: the counter is straightforward strategy, not manipulation → clean.

Ethics: clean. ✓

### Check 7: Confidence

- Premises: stated, but the user must verify the developer's financial position → reduces confidence.
- Hypotheses: 5 generated, leading and runner-up noted → supports confidence.
- Biases: anchoring and loss aversion flagged, mitigations specified → reduces confidence slightly.
- Counterfactuals: 5 articulated, all mitigated → supports confidence.
- Sources: mixed tier; the precedent compounding claim is judgment-based → reduces confidence.
- Ethics: clean → supports confidence.

**Overall: MEDIUM confidence.** The structure is sound; the mitigations are specified; the user must verify the developer's financial position before acting.

---

## The Discipline in One Page

1. **Premise check**: state all premises. If any is wrong, the answer changes.
2. **Hypothesis check**: 3-5 distinct hypotheses generated, leading and runner-up noted.
3. **Bias check**: each of the major biases considered; if active, articulated and mitigated.
4. **Counterfactual check**: what would make this wrong? Articulate, and mitigate where possible.
5. **Source check**: every claim traceable to a source; guesses flagged.
6. **Ethics check**: no red lines, no harm to innocents, no reputation erosion, no manipulation where strategy works.
7. **Confidence calibration**: high, medium, or low — stated explicitly.

An answer that passes all 7 is audited. An answer that fails any is revised before delivery.

---

## Common Pitfalls

**Pitfall 1: Audit theater.** Going through the 7 checks without engaging. If you can't articulate the specific bias you're checking for, you didn't audit.

**Pitfall 2: Audit fatigue.** Skipping checks because the answer "feels right." Feel is not audit. The check that feels most unnecessary is the one most needed.

**Pitfall 3: Audit rationalization.** The audit reveals a problem, but the answerer rationalizes it away ("but I'm probably right anyway"). If the audit reveals a problem, fix it.

**Pitfall 4: Audit only on confident answers.** Overconfidence is exactly when audit is most needed. Audit high-confidence answers HARDER, not less.

**Pitfall 5: Audit as a one-time check.** The audit is not a single gate; it is a discipline that runs through the entire decision pipeline. The premise check happens at the diagnosis; the hypothesis check happens at routing; the bias check happens at synthesis; the counterfactual and ethics checks happen at synthesis and audit; the source and confidence checks happen at delivery. The 7 questions are not a sequence; they are a checklist that runs throughout.

**Pitfall 6: Forgetting the spiritual dimension.** The Islamic concept of muhasabah (self-accounting) is the spiritual form of the blind spot check. The contractor who audits his strategic answers but not his spiritual state has done half the audit. The full audit includes the question: "What is the state of my heart in this answer? Am I seeking Allah's pleasure or my own advantage?"

---

## File History

- Created: 2026-09-09
- Version: 1.0
- Source: `00_META/self_audit_protocol.md` (the audit protocol), `00_META/multi_hypothesis_engine.md` (the hypothesis engine), `04_PSYCHOLOGY/cognitive_biases.md` (the bias catalog), `14_ETHICS/` (the ethics layer), `00_META/confidence_scoring.md` (the confidence scoring), classical Islamic muhasabah tradition (al-Muhasibi, al-Ghazzali, Ibn al-Mubarak), Karl Popper's falsification principle. Cross-referenced with `situation_diagnosis.md`, `domain_routing.md`, `mind_routing.md`, `multi_mind_synthesis.md`, `anti_bias_filter.md`.
- Review: 2027-03-09
