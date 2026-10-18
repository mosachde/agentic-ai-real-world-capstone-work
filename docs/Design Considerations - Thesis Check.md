# Thesis Check: Design Considerations

Mohit Sachdeva · CMU Agentic AI capstone · Started Oct 17, 2026

Open design points to revisit before they are finalized in a checkpoint or the final report. Each entry records the idea, why it matters, and the questions still open.

| # | Consideration | Source | Status |
|---|---|---|---|
| 1 | Verdict scoring rubric | Feedback | Open, to revisit |
| 2 | Unclear thesis: offer at most 2 peer theses, otherwise block the run | Own product decision | Provisional, to revisit |

---

## 1. Verdict scoring rubric

**Source:** feedback on Checkpoint 1.1.

**The gap.** The design lists three verdicts (Intact, Weakening, Broken), but the step from claim-level evidence to the overall verdict is not written down. Without a rule, the LLM decides the verdict, and two runs on the same filing could disagree.

**Proposal.** A small, explicit scoring rubric:

1. Score each of the 3–5 claims as **Met**, **Weakening** or **Broken**.
2. Combine the claim scores with fixed rules:

| Condition | Verdict |
|---|---|
| 0 Broken **and** at least 80% of claims Met | **Intact** |
| 2 or more Broken | **Broken** |
| Anything else | **Weakening** |

**Benefit.** The verdict becomes reproducible: the same filing gives the same answer. Because the rule is plain code rather than an LLM judgment, it can be unit-tested with pytest and checked in evaluation (run twice, compare).

**Open questions to resolve when revisiting:**
- **The 80% threshold in practice.** With 3 or 4 claims, 80% Met means *all* claims Met (2/3 = 67%, 3/4 = 75%). Only with 5 claims does it allow one non-Met claim (4/5). Is that intended, or should the rule be stated as counts?
- **Exactly 1 Broken** always gives Weakening. Should one critical claim (e.g., the core margin claim) be able to break the thesis on its own? This would mean claim weights or a "core claim" flag.
- **How claims with insufficient evidence count.** Excluded from the denominator? Counted as Weakening? Do they lower confidence instead of changing the verdict?
- **How "Untestable as stated"** (from the vague-thesis handling) fits in. It is probably a separate path that runs before the rubric and never reaches it.
- **Claim-level scoring rules.** What makes a single claim Met vs Weakening vs Broken? For example: Met = threshold satisfied in the latest period; Weakening = satisfied, but trending toward the threshold or within a margin of it; Broken = threshold missed. The trend window and margin need defining.
- **Confidence vs verdict.** Bull/bear disagreement and fact-check results should probably set a separate *confidence* level (High / Medium / Low) rather than change the verdict itself.
- **Where the rubric lives.** Procedural memory (a versioned rules file in Git), applied by deterministic code, not by an LLM prompt.

---

## 2. Unclear thesis: offer at most 2 peer theses, otherwise block the run

**Source:** own product decision (provisional; to be refined).

**Context.** Some users have no real thesis at all. The stock was a gift, a random purchase, or bought on a tip. The vague-thesis handling (clarification loop, "Untestable as stated" verdict, price-based claims excluded) covers users who have *some* belief that can be made specific. This point covers users who have none.

**Decision (provisional):**
1. The Thesis Analyst looks at the theses of **other users who hold the same ticker**.
2. It presents **at most 2** candidate theses.
3. The user picks one, and the test runs on it.
4. If the user doesn't like either option, the run is **not allowed**. No verdict and no limited mode for this case.

**Rationale.** It forces the user to commit to a real, testable thesis instead of running checks on nothing, which fits the product's purpose of deciding on evidence, not emotion.

**Open questions to resolve when revisiting:**
- **Few users per ticker.** Early on, a ticker may have no peer theses. Fall back to seeded template theses per sector or company?
- **Privacy.** Peer theses must be anonymized and aggregated; never show another user's holdings or identity.
- **Herding risk.** Adopting someone else's thesis is close to the herding bias the product counters. Should the user be asked to restate the chosen thesis in their own words, or confirm the thresholds?
- **Choosing the 2 theses.** Most common? Most testable? One bullish-leaning and one more cautious?
- **Is blocking too strict?** Measure how many users drop off at this step once it is built.
- **Evaluation.** Add a "no thesis / gift stock" case to the golden test set. Expected behavior: offers at most 2 theses and never issues a verdict without a confirmed thesis.
