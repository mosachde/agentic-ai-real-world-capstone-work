# Thesis Check

**A multi-agent AI that helps investors decide on evidence, not emotion.**

CMU Executive Education, *Agentic AI and Applications*, capstone project by Mohit Sachdeva.

> **Status: v1.0, project definition (Module 1).** The problem, users, positioning and a draft architecture are defined. The code folder still contains the course's single-agent starter template, unmodified; the multi-agent system is built in later versions.

## The problem

Investors are predictably biased: they hold losing stocks too long hoping to break even, sell winners too early to lock in gains (the disposition effect), and seek out information that confirms what they already believe. A key contributor is that the original reason for buying ("margins will expand because of the cloud shift") is rarely written down or re-tested as new evidence arrives in 10-Q and 10-K filings, earnings releases and insider trades. Without an advisor or investment committee to push back, decisions default to emotion.

## Who it's for

Self-directed investors who pick their own stocks but have no one to challenge their decisions. Primary persona: *Priya, 34, a product manager with $120k across 12 stocks, holding a 20% loss "until it gets back to even."* Secondary: professionals with concentrated employer stock (RSUs, ESPP).

## What it will do

Given a ticker and a plain-language thesis, Thesis Check will:

1. Turn the thesis into 3–5 testable claims with KPIs and thresholds.
2. Gather evidence from SEC filings (RAG) and structured XBRL financial data (tools).
3. Run a bounded bull-vs-bear debate between agents to counter confirmation bias.
4. Verify every number and citation with a fact-checker agent.
5. Return a verdict (Intact / Weakening / Broken) with cited evidence for the user to approve.

### Draft agent roster (to be refined in the next checkpoint)

| Agent | Role |
|---|---|
| Supervisor | Plans the run, routes work, enforces round and budget limits |
| Thesis Analyst | Converts the thesis into testable claims |
| Filing Researcher | Retrieves relevant 10-K / 10-Q / 8-K passages |
| Financial Data Analyst | Pulls XBRL facts and computes ratios with deterministic tools |
| Bull Advocate / Bear Advocate | Argue for and against each claim using only gathered evidence |
| Fact-Checker | Validates every number and citation before anything is shown |
| Report Writer | Produces the verdict report |

A human approves the extracted claims before research starts and approves or overrides the final verdict.

**Planned stack:** Python, LangGraph, an LLM API (Claude or OpenAI), SEC EDGAR APIs, Chroma, SQLite, Pydantic, pytest.

## Repository structure

```text
.
├── README.md
├── docs/
│   ├── Self-study Capstone Checkpoint Activity 7.1_...docx   # capstone report plan
│   └── STP and Positioning - Thesis Check.md                 # segmentation, targeting, positioning, persona
└── code/                                                      # CMU Research Agent starter template (baseline)
    ├── research_agent/
    ├── tests/
    └── requirements.txt
```

## Running the baseline (starter template)

```bash
cd code
python -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python -m research_agent.cli "Impact of AI on healthcare" --max-sources 8 --output report.md
python -m pytest tests -q
```

The single-agent starter is kept as the **baseline** the multi-agent system will be evaluated against.

## Roadmap

- **v1.0**: problem definition, users, positioning, draft architecture *(this version)*
- **v2**: SEC EDGAR data client and financial tools; single tool-using agent
- **v3**: RAG over filings; multi-agent supervisor graph
- **v4**: bull/bear debate, fact-checker, human-in-the-loop
- **v5**: memory across runs, evaluation harness (golden set, numeric accuracy, baseline comparison), guardrails

## Disclaimer

Thesis Check is an educational project and decision-support tool. It does not provide financial advice or buy/sell recommendations.

## Credits

The `code/` baseline is the CMU *Agentic AI and Applications* Research Agent starter template.
