from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .llm_writer import LLMWriter
from .models import ResearchReport, SearchResult, SourceDocument
from .summarizer import summarize_documents, summarize_text
from .web_research import WebResearchClient, deduplicate_results


@dataclass
class ResearchConfig:
    max_queries: int = 4
    max_results_per_query: int = 5
    max_sources: int = 8


class ResearchAgent:
    def __init__(self, config: ResearchConfig | None = None) -> None:
        self.config = config or ResearchConfig()
        self.web = WebResearchClient()
        self.llm_writer = LLMWriter()

    def build_queries(self, topic: str) -> List[str]:
        """
        TODO:
        Create multiple useful search queries from the learner's topic.

        Example:
        Topic: "Impact of AI on healthcare"

        Possible queries:
        - "Impact of AI on healthcare"
        - "Impact of AI on healthcare latest developments"
        - "Impact of AI on healthcare statistics and trends"
        - "Impact of AI on healthcare challenges and opportunities"
        """
        base = topic.strip()

        # TODO: Replace this simple starter logic with your own query strategy.
        candidates = [
            base,
            f"{base} latest developments",
            f"{base} key challenges",
            f"{base} future outlook",
        ]

        return candidates[: self.config.max_queries]

    def collect_sources(self, topic: str) -> List[SourceDocument]:
        """
        TODO:
        Use the web research client to:
        1. Build search queries.
        2. Search the web for each query.
        3. Deduplicate the search results.
        4. Fetch source documents.
        """
        all_results: List[SearchResult] = []

        # TODO: Loop through the queries created by build_queries().
        for query in self.build_queries(topic):
            # TODO: Search the web using self.web.search().
            results = self.web.search(query, limit=self.config.max_results_per_query)
            all_results.extend(results)

        # TODO: Deduplicate results and limit to max_sources.
        selected = deduplicate_results(all_results, keep=self.config.max_sources)

        # TODO: Fetch the source documents for the selected search results.
        docs = [self.web.fetch_source(result) for result in selected]

        return docs

    def research(self, topic: str) -> ResearchReport:
        """
        TODO:
        Orchestrate the full research workflow.

        Suggested workflow:
        1. Collect sources.
        2. Summarize each source.
        3. Create an executive summary.
        4. Create detailed findings.
        5. Build and return a ResearchReport.
        6. Optional: use LLMWriter if OPENAI_API_KEY is available.
        """
        sources = self.collect_sources(topic)

        # TODO: Summarize each source.
        for source in sources:
            combined_text = "\n".join([source.snippet, source.content])
            source.summary = summarize_text(combined_text, topic, max_sentences=5)

        # TODO: Improve these summaries as part of your capstone implementation.
        executive = summarize_documents([s.summary for s in sources], topic, limit=7)
        detailed = summarize_documents([s.content for s in sources], topic, limit=14)

        report = ResearchReport(
            topic=topic,
            executive_summary=executive,
            detailed_findings=detailed,
            references=sources,
        )

        # Optional LLM-enhanced mode.
        # TODO: Decide how and when to use the LLM writer.
        llm_markdown = self.llm_writer.write_report(topic, sources)

        if llm_markdown:
            report.detailed_findings = ["LLM-enhanced report generated."]
            report.executive_summary = ["See full markdown report below."]
            report._llm_markdown = llm_markdown  # type: ignore[attr-defined]

        return report


def render_report(report: ResearchReport) -> str:
    """
    Render a ResearchReport as markdown.

    Learners may customize this output format.
    """
    llm_markdown = getattr(report, "_llm_markdown", "")

    if llm_markdown:
        header = [
            f"# Research Report: {report.topic}",
            "",
            f"Generated on: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
        ]
        return "\n".join(header) + llm_markdown

    return report.to_markdown()