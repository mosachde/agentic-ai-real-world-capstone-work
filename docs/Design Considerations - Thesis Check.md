# Thesis Check: Design Considerations

Mohit Sachdeva · CMU Agentic AI capstone · Started Oct 17, 2026

Open design points to revisit before they are finalized in a checkpoint or the final report. Each entry records the idea, why it matters, and the questions still open.

| # | Consideration | Source | Status |
|---|---|---|---|
| 1 | Verdict scoring rubric | Feedback | Open, to revisit |
| 2 | Unclear thesis: offer at most 2 peer theses, otherwise block the run | Own product decision | Provisional, to revisit |
| 3 | How the evidence agents read and write "data facts" memory | Review of Checkpoint 2.1 | Open, to revisit |
| 4 | Bull/Bear requests for more evidence: an unbounded loop | Review of Checkpoint 2.1 | Open, to revisit |
| 5 | Tree-of-Thought claim search: provisional thresholds, weights and budget | Checkpoint 4.1 | Provisional, to calibrate |

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
- **Define the labels in the checkpoint doc.** Checkpoint 2.1 uses Met/Broken for claims and Intact/Weakening for the thesis, and calls "Untestable as stated" a "fourth outcome", but never lists the three verdicts. Once the rubric is settled, state both label sets in one line so a reader can tell claim scores from thesis verdicts.

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

---

## 3. How the evidence agents read and write "data facts" memory

**Source:** review of Checkpoint 2.1 (Oct 21, 2026).

**The gap.** The memory table and Figure 1 give the Filing Researcher and the Financial Data Analyst semantic memory: where a company reports a figure, and how it labels its line items. But the tools table lists the thesis and run-history store only for the Supervisor, Thesis Analyst and Report Writer. The design does not say how the evidence agents read these facts, or who saves new ones.

**Why it matters.** This is the one place the system learns from its own runs. A wrong fact (e.g., a mislabeled line item) would be reused on every later check of that company without anyone noticing.

**Proposal.**
1. **Reads:** the Supervisor loads the relevant data facts into each evidence agent's scoped view at the start of the run. Neither agent needs a memory tool, which keeps least privilege intact.
2. **Writes:** a fact is saved only after the Fact-Checker has verified the evidence it came from, by code at the end of the run, never by an agent mid-loop.

**Open questions to resolve when revisiting:**
- **Staleness.** Should a saved fact expire, or be re-checked when a company changes its reporting (new segments, restated figures)?
- **Scope.** Are facts stored per company, or shared across companies that use the same XBRL tags?
- **Doc consistency.** Update the tools table or the memory table in the next checkpoint so both describe the same access.

---

## 4. Bull/Bear requests for more evidence: an unbounded loop

**Source:** review of Checkpoint 2.1 (Oct 21, 2026).

**The gap.** Section 2 says the advocates get one rebuttal round and "if more evidence is needed, they ask the Supervisor." This path is not in Figure 1 or in the list of bounded feedback loops, and it has no limit.

**Why it matters.** Without a cap, the debate can keep reopening research and spending the cost budget, which is the unbounded behavior the fixed Supervisor workflow is meant to prevent. An advocate could also keep asking until it finds support for its side.

**Proposal.** Count an evidence request against the same budget as fact-check rework: at most one request per claim, and at most two trips back to the evidence agents per claim in total. Once the budget is spent, the gap is recorded and lowers confidence, the same way unresolved disagreement does.

**Open questions to resolve when revisiting:**
- **Who approves a request.** The Supervisor by a fixed rule (e.g., the claim has fewer than N cited passages), or does every request go through?
- **What happens after new evidence arrives.** A fresh rebuttal round, or the debate closes with the existing arguments plus the new evidence?
- **Doc consistency.** Add the path to Figure 1 and to the bounded-loop list in the next checkpoint.

---

## 5. Tree-of-Thought claim search: provisional thresholds, weights and budget

**Source:** Checkpoint 4.1 (Oct 29, 2026).

**The gap.** Checkpoint 4.1 sets the numbers that control the claim search, but they are my estimates, not measured values:

| Setting | Provisional value | What it controls |
|---|---|---|
| Tie margin | 0.25 points (1–5 scale) | When the investor is shown two readings instead of one |
| Claim-set cutoff | Weighted score below 3.5 is pruned | How strict the search is before returning "Untestable as stated" |
| Faithfulness floor | Faithful below 3 is pruned at either depth | The only cut the critic can make on its own |
| Rubric weights | Faithful 30%, Covers the chain 25%, Could fail 25%, Distinct 10%, Clear 10% | Which claim set wins |
| Beam width | 2 readings kept at depth 1 | How many readings survive a critic misjudgment |
| Budget | 12 LLM calls (cap 14), 20 tool probes, ~30k tokens, under 20 seconds | Cost and wait before the confirmation screen |

**Why it matters.** Each value moves the system in a direction the product cares about. A wide tie margin shows the investor two readings too often and adds friction; a narrow one hides real ambiguity. A strict cutoff turns testable theses into "Untestable as stated"; a loose one lets weak claim sets through. Too much weight on "Could fail" could tilt the search toward claims built to break, a bear bias that mirrors the confirmation bias the product counters.

**Proposal.** Set the values on the golden set before ToT goes live, not by judgment:
1. Write about 20 test theses with my reference readings and claim sets, including a thesis with two valid readings and one whose key metric the company doesn't report.
2. Measure how often the reference reading survives depth 1 (target: at least 90%), how often runs end in a tie, and how often they end "Untestable as stated."
3. Adjust the beam width, cutoff and weights until the targets hold, then record the final values in Checkpoint 4.1 and the README.

**Open questions to resolve when revisiting:**
- **Tie-rate target.** What share of runs should show two readings before it feels like friction? Measure once the confirmation screen is built.
- **Bear tilt.** Check that a claim set's "Could fail" score doesn't predict its eventual verdict; if it does, the search is choosing claims built to break.
- **Clarifying-question limit.** The failure path asks one clarifying question that counts toward 2.1's limit of 2–3. If the limit is already spent, should the run go straight to "Untestable as stated"?
- **Probe cutoff.** The text testability probe should use the same similarity cutoff as `search_filings` (Checkpoint 3.1), so "testable at decomposition" means "findable at research". Confirm when the retrieval tool is built.
- **Linear baseline.** If ToT doesn't beat a single linear decomposition on evidence coverage, agreement with reference claim sets and investor edit rate, it is removed (Checkpoint 4.1, Section 8).
