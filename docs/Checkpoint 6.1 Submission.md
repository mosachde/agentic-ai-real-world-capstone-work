# Capstone Checkpoint 6.1: Guardrails, Evaluation and Human Oversight

**Thesis Check: Making an Investment-Thesis Agent Safe and Dependable**

Mohit Sachdeva | Agentic AI Program | November 2026

## 1. Purpose and risks

Thesis Check takes a ticker and the investor's reason for owning it, turns that reason into 3–5 testable claims, gathers evidence from SEC filings, runs a Bull/Bear debate, fact-checks every number and returns a verdict (Intact, Weakening or Broken) for the investor to approve. Its tools are read-only, so it cannot trade. Its risks are about trust:

- **False reassurance:** a wrong number, or a passage from the wrong period, lets a failing claim pass.
- **The wrong question:** poorly chosen claims give a verified answer to the wrong question.
- **Agreeing with the user:** the bias the product exists to counter.
- **Untrusted text:** the thesis or a retrieved passage could carry hidden instructions.
- **Memory poisoning:** a wrong saved fact is reused on every later check.
- **Reading as advice:** the report could look like a buy/sell recommendation.

## 2. Guardrails

Guardrails sit at the four gates of the agent loop and are enforced in code, not prompts. *(new)* marks additions in this checkpoint.

| Gate | Guardrails |
|---|---|
| Input | Thesis text scanned and wrapped as untrusted *(new)*; vague theses get clarifying questions or "Untestable as stated" |
| Plan | Fixed workflow, not LLM routing; claims must pass code gates (no price claims, testable from SEC data); the investor confirms the claims |
| Tools | Read-only tools per agent (none for Bull and Bear); no trading tool; searches filtered to the claim's period; at most two rework loops; step and cost limits |
| Output | Every number and quote matched to its source and period; verdict from fixed rules; buy/sell language blocked *(new)* |

Every step, tool call and guardrail decision is logged under one trace ID *(new)*, and facts enter memory only after the Fact-Checker verifies them.

## 3. Evaluation metrics

Five core metrics on a golden set of test theses, compared with the course starter agent and a prompt-only baseline:

| Metric | Measured by |
|---|---|
| Numeric accuracy | Figures match XBRL for the right period (code) |
| Groundedness | Statements supported by their cited passages (LLM judge, checked against my labels) *(new)* |
| Verdict agreement | Matches my reference verdict; two runs agree (code) |
| Claim quality | Reference reading survives the claim search at least 90% of the time; investor edit rate |
| Safety | Older-filing trap never cited; no verdict without a confirmed thesis; injection cases fail *(new)* |

I also track cost, latency, override rate and the "insufficient evidence" rate *(new)*. The suite runs on every change, and a change ships only if no score drops *(new)*.

## 4. When a human must step in

The investor always confirms the claims and approves or overrides the verdict. The system also hands control to a person when:

- **The thesis is ambiguous:** it asks clarifying questions; if two readings tie, the investor picks one.
- **Evidence is missing or contested:** unverified claims are marked "insufficient evidence", and unresolved Bull/Bear disagreement or a spent rework budget lowers confidence. Nothing is guessed.
- **A guardrail fires:** injected instructions or a budget overrun stop the run for my review *(new)*.

## 5. How the parts work together

Guardrails block the failures I can predict, evaluation shows they hold before release, and people judge what code cannot. Every failure found in logs or by an investor becomes a golden-set test, and overrides are logged as preferences, never learned as evidence.

## 6. Trade-offs

| Choice | Gain | Cost |
|---|---|---|
| Supervised autonomy (Level 2): the investor approves claims and verdict | Investor stays in control | Friction, so only two touchpoints |
| Fixed workflow; verdict in code | Predictable, reproducible, auditable | Less flexible for unusual theses |
| Fact-check loops, capped at two | No unverified number reaches the investor | More time and cost |
| Code checks in every run; the groundedness judge runs offline | Runs stay fast and cheap | Some unsupported statements caught later |

## 7. Safer real-world deployment

Because Thesis Check cannot trade, its worst outcome is a misleading report, which is what this plan targets: verified numbers, reproducible verdicts, runs that can be replayed from their logs, and releases gated by evaluation. It is decision support, not financial advice.

## Project repository

Repository: [https://github.com/mosachde/agentic-ai-real-world-capstone-work](https://github.com/mosachde/agentic-ai-real-world-capstone-work)

This checkpoint: [https://github.com/mosachde/agentic-ai-real-world-capstone-work/tree/checkpoint-6.1/docs](https://github.com/mosachde/agentic-ai-real-world-capstone-work/tree/checkpoint-6.1/docs)
