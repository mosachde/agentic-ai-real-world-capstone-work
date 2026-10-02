# Thesis Check: STP and Positioning

Mohit Sachdeva · CMU Agentic AI capstone · Oct 1, 2026

## Working title

**Thesis Check: A Multi-Agent AI That Helps Investors Decide on Evidence, Not Emotion**

Alternatives:
- Thesis Check: Countering Investor Bias with Multi-Agent Research on SEC Evidence
- Thesis Check: An AI Investment Committee That Holds You to Your Own Thesis

## Problem and user (capstone Section 2)

**The problem: investors are predictably biased, and nothing in their workflow pushes back.**
Investors hold losing stocks too long hoping to break even, sell winners too early to lock in gains, and seek out information that confirms what they already believe. Behavioral finance has documented this for decades. Shefrin and Statman named it the *disposition effect* in 1985. Odean (1998) studied thousands of brokerage accounts and found that the winners investors sold went on to outperform the losers they kept. Barber and Odean (2000) found that the most active individual traders trailed the market by several percentage points a year. These aren't rare mistakes by novices. They are systematic, and they compound over time.

**Why it happens.**
A key contributor is that the original reason for buying ("margins will expand because of the cloud shift") is rarely written down or re-tested. New evidence keeps arriving: 10-Q and 10-K filings (often 100+ pages), earnings releases, guidance changes and insider trades. Reading it all against a personal thesis takes hours most people don't have. So when the stock moves, the decision is driven by the price and the emotion it triggers, not by whether the reason still holds. Professional investors guard against this with investment committees, written theses and a designated devil's advocate. Individual investors have none of that.

**Who is affected.**
Retail participation is at record levels. Schwab alone reports about 38.5 million active brokerage accounts, and individual investors make up roughly a fifth of US equity trading volume. The primary users of this system are **self-directed "conviction" stock-pickers**: people like Priya, a 34-year-old product manager with $120k across 12 stocks. She bought a semiconductor stock because "AI demand will keep margins above 60%," hasn't read a filing since, and is now holding a 20% loss "until it gets back to even." A secondary group is **professionals with concentrated employer stock** (RSUs, ESPP). Their largest financial decision, how much of their employer to keep, often has no thesis behind it at all.

**Why existing tools don't solve it.**
Today's AI investing tools (broker assistants, research platforms) summarize news and generate new ideas. They answer "what's happening with this stock?", not "is *my* reason for owning it still true?" Many are built into brokerages that earn more when customers trade more, so they have little incentive to say "your thesis is intact, do nothing." Human advisors play this role, but they typically charge around 1% of assets, which is uneconomic below a few hundred thousand dollars.

**Why this is an interesting problem for agentic AI.**
The fix mirrors how a professional investment committee works, and that structure maps naturally onto multiple agents:

1. **Turn** a vague belief into testable claims.
2. **Gather** evidence from long primary-source documents.
3. **Argue** both sides deliberately. A bull agent and a bear agent counter the user's confirmation bias by design.
4. **Verify** every number before anyone sees it, because a single hallucinated figure could trigger a costly decision.

A single prompt can't reliably do all four. Separate roles, structured debate, a validator and a human approval step can. Success means the investor makes a hold/sell decision based on evidence they can see and check, not on the last price move.

*Sources: the Schwab and trading-volume figures come from mrd.md (idea-inv-drift). The academic findings are cited from memory; verify them before submission.*

## Mission and vision

- **Mission:** Help self-directed investors make hold/sell decisions based on evidence, not emotion.
- **Vision:** Every investor gets the discipline of an investment committee: an honest second opinion that tests why they own what they own.

## 1. Segmentation

Segment by **behavior**, not demographics. What predicts fit is how someone makes investment decisions: do they hold individual stocks, do they have a reason for owning them, and how do they react to news?

| Segment | Who they are | Decision behavior | Main bias | Has a thesis? |
|---|---|---|---|---|
| A. Conviction Stock-Pickers | Long-term DIY investors with 5–25 individual stocks, roughly $25k–$500k, often in tech, finance or engineering jobs | Research before buying, then rarely revisit | Confirmation bias, holding losers | Yes, at least loosely |
| B. Concentrated-Position Professionals | Tech or corporate employees with a large chunk of wealth in employer stock (RSUs, ESPP) | Never chose to buy, so never decide to sell | Familiarity bias, inertia | No ("I work there" isn't a thesis) |
| C. Anxious New Investors | Started investing after 2020, smaller portfolios, follow social media and tips | Buy on hype, panic-sell in drops | Herding, loss aversion | Rarely |
| D. Active Traders | Frequent traders, options, momentum, short horizons | Act on price and technicals | Overconfidence | Technical, not fundamental |
| E. DIY Income Investors | 50+, dividend stocks, preserving retirement income | Hold for years; worry about dividend cuts | Status quo bias | Yes ("the dividend is safe") |
| F. Pro-sumers | Newsletter writers, finfluencers, investment clubs | Publish theses publicly | Commitment bias (defending a public call) | Yes, written down |
| G. Financial Advisors (later, B2B2C) | RIAs serving mass-affluent clients | Manage clients' emotions in drawdowns | Clients' biases, not their own | Plan-level thesis |

## 2. Targeting

| Segment | Size | Pain intensity | Can state a thesis? | Willingness to pay | Fit with v1 (SEC filings, US stocks) | Verdict |
|---|---|---|---|---|---|---|
| A. Conviction Stock-Pickers | Medium | Medium–High | High | Medium | High | **Primary target** |
| B. Concentrated-Position Pros | Medium | Very high (big stakes) | Low, but the system can help build one | High | High | **Secondary target** |
| E. DIY Income Investors | Medium | Medium | High | Medium | High (dividend data is in filings) | Later expansion |
| F. Pro-sumers | Small | Medium | Very high | Medium | High | Channel and early adopters |
| C. Anxious New Investors | Large | High | Low | Low | Low | Avoid in v1 |
| D. Active Traders | Large | Low (for this job) | Low | Medium | Low (wrong time horizon) | Avoid; Robinhood's turf |
| G. Advisors | Medium | High | Plan-level | High | Medium (needs integrations) | Commercial phase |

Size ratings are relative and directional, not measured.

- **Why A is primary:** they already have a thesis, so the product works as designed. They also take the riskiest assumption (A3: "can investors state a thesis?") off the table for v1.
- **Why B is the secondary target:** a large RSU position in one stock is the highest-stakes, least-examined decision many professionals face. The job changes from "test my thesis" to "help me build one, then hold me to it." This could be the commercial wedge later.
- **Who to avoid:** C needs coaching more than research and pays little. D wants speed and signals, the opposite of what Thesis Check offers.

## 3. Positioning

### Positioning statement

For self-directed investors who pick their own stocks but have no one to challenge their decisions, Thesis Check is an AI research partner that tests why you own a stock against the latest SEC evidence. Unlike AI research tools that summarize news or suggest new trades, Thesis Check starts from your own reason for buying, has AI agents argue both the bull and bear case, and verifies every number against official filings, so you hold or sell on evidence, not emotion.

**One-liner:** "An AI investment committee that tests your thesis before your emotions do."

| Element | Content |
|---|---|
| Target (whom we serve) | Self-directed investors who pick their own stocks but have no advisor or committee to challenge their decisions |
| Frame of reference (what we compete with) | AI investment research tools: Robinhood Cortex, Public Alpha, Seeking Alpha, Fiscal.ai |
| Points of parity (table stakes) | AI summaries of filings and earnings; plain-language explanations; cited sources; any US-listed stock; results in minutes |
| Points of difference (why us) | Starts from your thesis, not the stock. Bull and bear agents argue both sides, countering confirmation bias. Every number is verified against official SEC data. It remembers why you bought and re-checks when new filings arrive. No trading agenda: it will tell you to do nothing. |
| Reason to believe | A multi-agent design with an adversarial debate and an independent fact-checker; primary-source SEC data instead of web articles; a full audit trail of evidence for every verdict |

Note: "no trading agenda" only holds if the product never earns from trades. That's fine for the capstone; it matters if commercialized.

### Messaging by target

| Target | Message | Key proof point |
|---|---|---|
| A. Conviction Stock-Pickers | "An investment committee that tests your thesis before your emotions do." | Bull/bear debate, cited SEC evidence |
| B. Concentrated-Position Pros | "You never decided to own this much of your employer. Decide now, on evidence." | Turns "I work there" into explicit sell rules ("sell 25% if revenue growth drops below 10%") |
| E. Income Investors | "Know if your dividend is safe before the cut is announced." | Payout ratio, cash flow and debt trends from filings |
| F. Pro-sumers | "Keep your public calls honest, with receipts." | A shareable thesis scorecard |

## Primary persona

**Priya, 34, product manager in Seattle.** She has $120k across 12 stocks and believes she's a long-term investor. She bought a semiconductor stock 18 months ago because "AI demand will keep margins above 60%," and hasn't opened a 10-Q since. It's down 20% and she's holding until it "gets back to even." She doesn't want stock tips. She wants someone to tell her honestly whether her original reason still holds.

## Implications for the build

- Write the golden test set from Segment A theses: clear, fundamental and testable.
- Add a stretch test case from Segment B (an RSU holder with no thesis), so the Thesis Analyst agent also has to help *build* a thesis, not just parse one.
- Keep the scope to US-listed stocks and SEC data, which fits Segments A, B and E.
