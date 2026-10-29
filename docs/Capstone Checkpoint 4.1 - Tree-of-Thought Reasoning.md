# Capstone Checkpoint 4.1: Tree-of-Thought Reasoning

**Thesis Check: Choosing the Right Claims Before Testing Them**

Mohit Sachdeva | Agentic AI Program | October 2026

## 1. Is Tree-of-Thought appropriate?

Yes, in one place. Tree-of-Thought (ToT) improves the step where the Thesis Analyst turns a thesis into claims, and it would hurt everywhere else in Thesis Check.

Checkpoint 2.1 added a reasoning loop only where the next step depends on what was just observed. ToT gets a matching rule: explore alternatives only where (1) an early wrong choice is expensive, (2) no later step can catch it, and (3) candidates can be scored cheaply before committing to one. Claim decomposition is the only step that meets all three.

| Step | Reasoning today (2.1) | ToT? | Why |
|---|---|---|---|
| Thesis Analyst: claim decomposition | One structured step, plus clarifying questions | **Yes** | Every later step inherits the claims, no loop sends them back, and testability can be checked cheaply before research starts |
| Filing Researcher | ReAct loop | No | Each search result shows what to try next. A miss stays local to one claim and ends as "insufficient evidence." Branching would multiply retrieval calls without adding evidence |
| Financial Data Analyst | Short ReAct loop | No | Few alternatives (e.g., gross profit = revenue − cost of revenue), and tools do the arithmetic |
| Bull and Bear Advocates | One-round structured debate | No | They argue only from gathered evidence. Searching for the most persuasive argument rewards rhetoric, not truth |
| Fact-Checker | Rule-based checks | No | A number matches its source or it doesn't. There is one right answer |
| Supervisor and verdict rubric | Fixed workflow and rules | No, by design | The same filing must give the same verdict, and cost must stay bounded. A search over verdicts breaks both |

## 2. Where ToT is used

ToT runs inside the Thesis Analyst, after the investor enters a thesis and before they confirm the claims. Its job is to pick the best set of 3–5 testable claims. It runs once per thesis: quarterly re-checks reload the confirmed claims from long-term memory, so they never pay for the search again and stay comparable over time.

Take Priya's thesis, "AI demand will keep gross margins above 60%." A linear chain of thought fails here in three ways.

- **Premature commitment.** A linear chain decides in its first sentence what "AI demand" and "keep" mean, and everything after builds on that. If it reads "keep" as "last quarter's margin," it never adds a claim on management's outlook, and the claim set can pass even when next quarter's guidance has just dropped below 60%. Nothing downstream catches the gap. The Fact-Checker checks evidence against its sources, and rework goes back to the evidence agents, not to the Thesis Analyst. The run produces a fully verified answer to the wrong question. The investor's confirmation is a weak backstop: the person reviewing the claims is the person whose confirmation bias the product exists to counter, and an easy-to-pass claim set looks good to them.
- **High branching.** "AI demand" can be measured as data-center revenue, total revenue growth, backlog or management commentary. "Margins" can mean gross or operating margin. "Keep" can mean last quarter, the last four quarters or next quarter's outlook. That's roughly 30 plausible combinations before any threshold is set.
- **Constraint complexity.** A valid claim set must meet six rules at once: 3–5 claims; each testable from *this company's* SEC data; no price-based claims; the investor's numbers kept exactly (60% stays 60%); no two claims measuring the same thing; and at least one claim that could actually fail. Testability is company-specific: many companies don't report AI or segment figures as separate XBRL facts, so a claim that works for one ticker is untestable for another. A linear chain checks these rules at the end, if at all. Violations surface downstream as "insufficient evidence," after the research budget is spent.

### Where ToT sits in the workflow

Figure 1 updates the Checkpoint 2.1 system design. ToT is added inside the Thesis Analyst, between the clarifying questions and the investor's claim confirmation. Every other agent, loop and checkpoint is unchanged.

![Thesis Check system design, updated for Checkpoint 4.1: ToT claim search inside the Thesis Analyst](images/thesis-check-system-design-v4.1.png)

*Figure 1. Thesis Check system design, updated for Checkpoint 4.1.*

The run order, with the ToT step expanded:

```text
Investor: ticker + thesis         (new ticker → filings ingested, so the probes can run)
  │
  ▼
Supervisor: fixed workflow, step and cost limits
  │
  ▼
Thesis Analyst
  ├─ clarifying questions if the thesis is vague (up to 2–3)
  └─ ToT claim search  ◀── new in 4.1; skipped on re-checks (confirmed claims reloaded)
       Thought Generator → gates (code + MCP probes) → Claim Critic → prune (beam 2)
       depth 1: 3 readings → keep 2      depth 2: 3 claim sets each → select 1 (2 if tied)
       nothing survives → 1 clarifying question → rerun once → "Untestable as stated"
  │
  ▼
HUMAN CHECKPOINT: investor confirms, edits (edits re-gated) or picks one of two readings
  │
  ▼
Filing Researcher (ReAct)  ‖  Financial Data Analyst (ReAct)    same MCP tools as the probes
  │                                     ▲
  ▼                                     │ rework, at most 2 (never back to the claim search)
Bull ↔ Bear debate  →  Fact-Checker ────┘
  │
  ▼
Verdict rubric (code) → Report Writer
  │
  ▼
HUMAN CHECKPOINT: approve or override → long-term memory (claims, verdict, decision)
```

The workflow makes two points visible. The Fact-Checker's rework loop returns to the evidence agents, never to the claim search, so claim errors have to be caught before confirmation. And quarterly re-checks start from the confirmed claims, so they skip ToT entirely.

## 3. ToT structure

| Element | In Thesis Check |
|---|---|
| Thought | One decision about how to make the thesis testable: how to read it, or how to measure it |
| Node (reasoning state) | Everything decided so far: the root plus the thoughts on the path to it. A depth-1 state holds the thesis and one reading; a depth-2 state adds one claim set. States are stored as immutable records (Section 6) |
| Root (depth 0) | The thesis as written, the ticker, any clarifying answers, and the thresholds the investor stated (extracted by code) |
| Depth 1 node | A **reading**: the thesis as a short cause-and-effect chain with vague words pinned down, e.g., "AI demand → data-center sales grow faster → richer product mix → gross margin ≥ 60% each quarter" |
| Depth 2 node (leaf) | A **claim set**: 3–5 claims that measure one reading, each with a metric, comparison, threshold, period and evidence source (XBRL concept or filing section) |
| Branch | An alternative thought from the same parent: another reading, or another claim set for the same reading |
| Branching behavior | The generator proposes 3 children per node: 3 readings at depth 1, then 3 claim sets for each reading kept. Effective branching is lower: the beam keeps 2 readings, and gates remove claims or whole sets |
| Depth limit | 2. A leaf is a complete claim set, so nothing is left to decide |
| Tree size | With a beam width of 2, at most 3 + 6 = 9 nodes are generated and scored |

```text
Thesis: "AI demand will keep gross margins above 60%"
├── R1 Pricing power: demand lets the company hold prices → GM ≥ 60%      kept (4.4)
│   └── S1a, S1b, S1c                                                     best: S1a (4.2)
├── R2 Mix shift: data-center sales grow faster → richer mix → GM ≥ 60%   kept (4.6)
│   ├── S2a                                                               SELECTED (4.55)
│   ├── S2b  AI chip revenue not reported → claim dropped, driver lost    pruned (3.25)
│   └── S2c  stock-price claim dropped by gate                            kept, ranked lower (4.0)
└── R3 Guidance only: management guides GM ≥ 60%                          pruned: ranked 3rd (3.0)
```

**Termination and selection.** The search ends when the depth-2 claim sets are scored. The highest-scoring surviving set is selected and shown at the existing claim-confirmation step. If only one reading survives depth 1, the search continues with that one. It also stops early when the budget runs out or nothing survives (Section 4).

**Why two levels instead of "generate several claim sets and pick the best."** The reading is the high-impact choice. Pruning a wrong reading before writing claims for it saves calls. And when the two finalists come from different readings, the system learns the thesis itself is ambiguous, which is a question for the investor rather than for the scorer.

## 4. Search and evaluation

### Search strategy: beam search, width 2

| Strategy | Compute | Latency | System complexity | Fit |
|---|---|---|---|---|
| **Beam search, width 2 (chosen)** | Fixed: 9 nodes, 12 LLM calls | 4 rounds; calls within a level run in parallel | Low: score, sort and keep the top 2 at each level | Compares readings side by side and drops weak ones before spending calls on them. Width 2 keeps a second reading alive in case the critic misjudges the first |
| BFS | 12 nodes, 16 LLM calls, and no cap: 4 readings would mean 20 nodes | 4 rounds | Lowest: no ranking until the end | Would work at this size, but it spends calls expanding readings already known to be weak |
| DFS | Unpredictable: as few as 6 calls if the first reading works, up to the BFS count if it backtracks | 4 to 8 rounds: readings are tried one after another | Medium: needs a backtracking stack and a "good enough to stop" rule | Commits to the first reading before seeing the others: the premature commitment ToT is meant to fix. The result also depends on generation order |
| Monte Carlo sampling | Dozens of rollouts to beat beam on a two-level tree, so it needs its own cap | Many sequential select-expand-score rounds | High: selection policy, rollouts, score backup and visit counts, all hard to explain in an audit log | Built for deep trees with uncertain payoffs. Here it adds cost and run-to-run variation without improving accuracy |

The generator proposes all three siblings in one call and is asked to make them differ. It runs at temperature 0, so the variety comes from the prompt, not random sampling, and the same thesis produces nearly the same tree.

ToT's complexity stays contained. It is one subgraph inside the Thesis Analyst, with four steps (generate, gate, score, prune) and a linear fallback. Removing it would mean replacing that subgraph with a single call; no other agent would change.

### How branches are assessed

Code and tools decide facts. A critic LLM judges meaning.

**Layer 1: pass/fail gates (code and tool calls), applied to every claim before any scoring.**

| Gate | Check | Done by |
|---|---|---|
| Well-formed | Metric, comparison, threshold, period and source are all present | Pydantic schema |
| No price claims | No stock price, valuation multiple or price target. Also applied to each reading's outcome | Rule check |
| Investor's numbers kept | Every threshold in the thesis appears unchanged in the claims | Code |
| Testable | Numeric claim: the XBRL concept has values for the needed periods. Text claim: `search_filings` returns at least one passage above the similarity cutoff for the claim's period | Tool probes |

The probes answer "can this be tested?", never "would it pass?" They return found or not found, never the figure or the passage. If the critic saw outcomes, the search would drift toward claims with a known result: choosing the test after seeing the answers.

**Layer 2: critic scores (LLM, 1–5 per criterion).**

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| Faithful | 30% | Tests the belief as stated, with the investor's metric and time frame | Tests a different, easier belief |
| Covers the chain | 25% | Every link from driver to outcome has a claim | Only the outcome is tested |
| Could fail | 25% | At least one claim could plausibly fail on the next filing | Every claim passes whatever the results, e.g., "management discusses AI" |
| Distinct | 10% | Each claim measures something different | Two claims measure the same thing, e.g., gross margin and gross-profit growth |
| Clear | 10% | The investor can confirm it in one read | Needs a finance background to follow |

Readings at depth 1 have no claims yet, so they're scored on Faithful (60%) and Covers the chain (40%) only. "Could fail" is the bias check. A linear chain and the investor both drift toward claims that are easy to pass, and this criterion pushes back. It rewards claims that *could* fail, not ones likely to: the critic never sees the data, so it can't tilt toward either result.

**Who evaluates.** The evaluator has two parts, both inside the Thesis Analyst step and neither one a new agent: the gates, which are plain code plus tool calls, and the **Claim Critic**, a separate LLM role with its own prompt, at temperature 0. The decision maker then applies the thresholds below to their results. The critic sees only the thesis and one candidate, never the generator's reasoning or the other candidates, so neither order nor anchoring can sway a score. It also never sees the investor's past claim edits. Those can guide how the generator drafts claims, but they can't lower the bar for "Could fail." This follows Checkpoint 2.1's rule that overrides are preferences, not evidence.

**Pruning thresholds and failure conditions.**

- A claim that fails a gate is dropped from its set.
- Depth 1: a reading is pruned if its outcome is price-based or it scores Faithful < 3. The top 2 survivors move on.
- Depth 2: a claim set is pruned if fewer than 3 claims survive the gates, its outcome claim is dropped, it scores Faithful < 3, or its weighted score is below 3.5.
- Nothing survives: the Thesis Analyst asks one clarifying question built from the failure reason ("This company doesn't report AI chip sales separately. Would data-center revenue work?") and reruns once. This question counts toward 2.1's limit of 2–3 clarifying questions. If nothing survives again, the result is "Untestable as stated," with the failed gates shown so the investor can rephrase.
- Budget exhausted: the best surviving claim set is shown, flagged as a partial search.
- Critic output fails schema validation twice: the system falls back to one linear decomposition through the same gates, and logs it.
- A pruned node is marked with its reason and never expanded. It stays in the run log.

**Ties.** Two claim sets tie when their scores are within 0.25 points.

- **Different readings:** the thesis is genuinely ambiguous, and only the investor knows what they meant. The confirmation screen shows both ("We read your thesis two ways; pick one"). That's at most 2 options, matching the peer-thesis rule in Design Considerations.
- **Same reading:** a fixed order decides: more claims backed by exact XBRL figures, then a higher "Could fail" score, then fewer claims, then the earlier node. The same tree always yields the same pick.

**Compute, latency and cost (estimates, to be measured).**

| Limit | Value |
|---|---|
| LLM calls | 12 planned (3 generator calls and 9 critic calls); hard cap of 14 to allow retries |
| Tool probes | At most 20, deduplicated by metric and period. Numeric probes are local lookups in the company's cached XBRL data |
| Tokens | Short prompts (a thesis and one candidate, no filing text); cap of about 30k tokens per search |
| Latency | Calls run in parallel within each level, so there are 4 sequential rounds; target under 20 seconds before the confirmation screen |
| Frequency | Once per new or edited thesis, never on quarterly re-checks |

## 5. ToT in action

Thesis: "AI demand will keep gross margins above 60%." The tree is in Section 3. *(Illustrative; scores and data availability are hypothetical.)*

1. The generator proposes three readings. The critic scores mix shift (R2) 4.6 and pricing power (R1) 4.4. Guidance only (R3) scores 3.0: it tests the forecast but not the demand behind it, so it ranks third and the beam drops it. The outlook doesn't disappear; it comes back as a claim under R2.
2. For each kept reading, the generator proposes three claim sets. Under R2:
   - **S2a:** data-center revenue grows year over year in each of the last two quarters (10-Q segment note); gross margin ≥ 60.0% in the latest quarter (XBRL: gross profit ÷ revenue); next-quarter gross margin outlook ≥ 60% (8-K earnings release); inventory charges not rising as a share of revenue (10-Q MD&A).
   - **S2b** swaps the first claim for "AI accelerator revenue grows." The probe finds no such figure, so the claim is dropped. Three claims remain, but the driver link is gone, and the set scores 3.25. Pruned.
   - **S2c** adds "the stock outperforms the semiconductor index." The price gate drops that claim, and the rest scores 4.0.
3. S2a scores 4.55, ahead of S2c (4.0) and R1's best set (4.2). The gap is wider than the 0.25 tie margin, so S2a is shown alone, with each claim's source.
4. The investor confirms. The tree, with every score and pruning reason, goes to the run log.

A linear chain of thought might produce "gross margin above 60% last quarter, revenue growing, management positive on AI demand." It misses guidance, and its third claim can't fail. If last quarter's margin, though lower, is still above 60% while guidance has fallen to 58% (Checkpoint 3.1's example), that set says Intact. S2a includes the outlook claim, which comes back Broken.

## 6. Mapping ToT roles to tools

**Role definitions.** The two LLM roles are defined the way CrewAI defines agents: a role, a goal, what each one sees and what it must never see. That keeps the design independent of any framework. The gates, the decision maker and the state manager are code, not LLMs.

| Role | Goal | Sees | Never sees | Produces |
|---|---|---|---|---|
| Thought Generator | Propose 3 distinct readings, then 3 claim sets for each reading kept | Thesis, ticker, clarifying answers, the investor's past claim edits | Scores, data values | Readings and claim sets in a fixed Pydantic schema |
| Claim Critic | Score one candidate against the rubric | Thesis, one candidate, its gate results (found / not found) | Other candidates, the generator's reasoning, the investor's edits, data values | A 1–5 score per criterion, each with a one-line reason |
| Decision maker | Apply the gate results and score thresholds, prune, run the beam, tie and budget rules, and stop | The whole tree and the budget counters | n/a (deterministic code) | The selected claim set, or two when tied |
| State manager | Keep the tree consistent and resumable, and save the result | Every node | n/a (storage) | A checkpoint per level, the run log, and confirmed claims in long-term memory |

**How each tool supports each role.**

| ToT role | LangChain / LangGraph | MCP | CrewAI (evaluated) |
|---|---|---|---|
| Thought Generator | **Used.** An LCEL chain (prompt → model → Pydantic output), called from a LangGraph node. `batch()` runs both kept readings in parallel | **Used** for context: reads the investor's confirmed claims and past edits from the thesis store | Could define it as an `Agent` with its own role and goal. Not needed: a LangGraph node with its own prompt gives the same separation |
| Critic / evaluator (gates + Claim Critic) | **Used.** The Claim Critic is a separate LCEL chain that returns typed scores; the gates are Python functions in a LangGraph node | **Used** for testability probes: the XBRL lookup and `search_filings` run on the same MCP server the evidence agents use, so "testable at decomposition" means "findable at research" | Could define it as a second `Agent`. Not needed, for the same reason. CrewAI's built-in crew memory is shared between agents, which would undo the critic's isolation |
| Decision maker | **Used.** A LangGraph subgraph runs generate → gate → score → prune, with a conditional edge that loops to depth 2 or stops. Beam, tie and budget rules are code, and the confirmation step is a LangGraph interrupt | Not used | Not suitable: CrewAI's hierarchical process lets a manager LLM choose the next step, which the fixed Supervisor design rules out |
| State manager | **Used.** LangGraph state holds the tree as immutable nodes (id, parent, depth, thought, gate results, scores, status, reason), so branches can't overwrite each other. A SQLite checkpointer saves each level, so an interrupted run resumes without re-scoring | **Used** for state across runs: the thesis store, served over MCP, saves the confirmed claim set and returns it on re-checks | Not used: its own memory and task outputs would be a second copy of the state |

The tree itself stays in LangGraph, because the decision maker reads and writes it at every step. MCP carries what is shared beyond this step: the SEC tools and the thesis store. Only the chosen claim set passes to the downstream agents; the full tree goes to the run log.

**Why LangChain is enough, and CrewAI isn't used.** I evaluated CrewAI for each role. Its main strengths are agents that delegate to each other and a manager LLM that routes work, and Thesis Check deliberately rules out both: the Supervisor is a fixed workflow, and the critic must not share context with the generator. The one thing CrewAI would add, separate role definitions, comes from the role table above plus LangGraph nodes with their own prompts and scoped state. Adding CrewAI would bring a second framework, with its own prompt text, execution loop and logs, for no change in behavior. Every extra line of prompt text is also one more thing to hold fixed for temperature-0 scoring. If defining all eight agents in the multi-agent stage proves clumsy in LangGraph, the role definitions above can be ported to CrewAI agents while LangGraph keeps the control flow.

## 7. Risk and mitigation

**Risk: weak evaluation signals cause premature pruning of the best branch.** Beam pruning is final: once a reading is cut at depth 1, nothing brings it back. The critic decides from one sentence what the investor meant. LLM judges tend to prefer the most common reading and the most fluent claim set, and to undervalue company-specific ones; an inventory-charge claim can look odd yet be the one most likely to break. If the investor's real reading is cut, they will probably confirm whatever they're shown.

**Mitigation: the critic ranks but doesn't cut alone, and it is calibrated before it's trusted.**

- Outright cuts come from objective checks: the gates, and clear misreadings (Faithful < 3). Otherwise the critic's score only orders branches. The beam keeps two readings, so one misjudgment doesn't decide the outcome, and near-ties go to the investor.
- The golden set gains about 20 theses with my reference readings and claim sets. Before ToT goes live, I'll measure how often the reference reading survives depth 1 (target: at least 90%). If it falls short, I'll adjust the rubric anchors, the 3.5 threshold or the beam width.
- Every pruned branch is logged with its score and reason, so a wrong cut shows up in the run log instead of passing silently.

The design also handles the other common ToT risks: the fixed beam and call caps prevent branch explosion, and immutable nodes keep branch state consistent.

## 8. What changes from Checkpoints 2.1 and 3.1

- **Thesis Analyst:** its reasoning changes from "light (clarifying questions)" to "ToT claim search (beam width 2, depth 2) plus clarifying questions." The Thought Generator and Claim Critic are separate roles inside this step, not new agents.
- **System design:** Figure 1 replaces the 2.1 diagram for this version. The SEC tools and the thesis store are served over MCP, so the probes, the evidence agents and the claim search share one implementation.
- **Claim confirmation:** the investor sees one claim set, or two when the thesis reads two ways. Their edits go through the same gates before research starts.
- **"Untestable as stated"** now has a precise meaning: no claim set passes the gates, even after one clarifying question.
- **Ingest timing:** filings are ingested as soon as a new ticker is entered, so the index is ready for the testability probes.
- **Run log and golden set:** the log records the full tree. The golden set adds decomposition cases, including a thesis with two valid readings and one whose key metric the company doesn't report.
- **Evaluation:** ToT will be compared with a single linear decomposition on three measures: the share of claims that end with evidence rather than "insufficient evidence," agreement with my reference claim sets, and how often investors edit the claims. If ToT doesn't beat the linear version, it's removed.
- **Provisional values:** the 0.25 tie margin, the 3.5 threshold and the rubric weights stay provisional until calibration, and are tracked in Design Considerations.

## 9. Project repository

Repository: [https://github.com/mosachde/agentic-ai-real-world-capstone-work](https://github.com/mosachde/agentic-ai-real-world-capstone-work)

This checkpoint: [https://github.com/mosachde/agentic-ai-real-world-capstone-work/tree/checkpoint-4.1/docs](https://github.com/mosachde/agentic-ai-real-world-capstone-work/tree/checkpoint-4.1/docs)
