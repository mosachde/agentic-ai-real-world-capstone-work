# Research Agent Starter Template

## Overview

This repository is a starter template for the CMU Agentic AI Capstone.

The goal is to build an autonomous research agent that can:

* Generate research queries from a topic
* Search the web for relevant information
* Retrieve and process source content
* Summarize findings from multiple sources
* Generate a structured research report
* Optionally use an LLM to enhance report quality

The provided code includes a working project structure and scaffolding to help you get started. Several components contain TODOs and opportunities for enhancement as part of your capstone implementation.

## What You Will Build

As part of this capstone, you are encouraged to:

* Improve research query generation
* Enhance web search and retrieval strategies
* Improve source summarization
* Generate richer research reports
* Integrate LLM-powered report generation
* Experiment with agentic workflows and decision-making

## Project Structure

```text
research_agent/
├── agent.py              # Research workflow orchestration
├── cli.py                # Command-line interface
├── llm_writer.py         # Optional LLM report generation
├── models.py            # Data models
├── summarizer.py        # Summarization logic
└── web_research.py      # Web search and retrieval

tests/
```

## Files with TODOs

The starter template includes scaffolding and TODOs in:

* `agent.py`
* `web_research.py`
* `summarizer.py`
* `llm_writer.py`

You are encouraged to customize and improve these components as part of your capstone project.

## Setup

Create and activate a virtual environment.

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m research_agent.cli "Impact of AI on healthcare" --max-sources 8 --output ai_healthcare_report.md
```

## Environment Variables

The project works without an API key using extractive summarization.

To enable LLM-enhanced report generation, create a `.env` file using the provided `.env.example`.

Example:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

Do not commit API keys to source control.

## Output Format

The generated report may include:

* Executive Summary
* Detailed Findings
* Sources / References

Depending on your implementation, you may choose to extend the report with additional sections, citations, recommendations, or analysis.

## Tests

```powershell
python -m pytest tests -q
```

## Suggested Enhancements

Possible extensions include:

* Better search query generation
* Improved source ranking and filtering
* Smarter summarization techniques
* Citation-aware report generation
* Multi-agent workflows
* Additional report formats (PDF, HTML, DOCX)
* Custom user interfaces

## Notes

* This repository is intended as a starting point, not a completed capstone solution.
* Multiple implementation approaches are valid.
* You are encouraged to adapt the architecture to fit your project goals.
* Review all TODOs before beginning development.



