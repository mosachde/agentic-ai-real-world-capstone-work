from __future__ import annotations

import os
from typing import List

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore[assignment]

from .models import SourceDocument


class LLMWriter:
    """
    Optional LLM-powered report writer.

    This class should only call an LLM when OPENAI_API_KEY is available.
    If no API key is configured, the research agent should still work using
    extractive summarization.
    """

    def __init__(self) -> None:
        """
        TODO:
        Read API configuration from environment variables.

        Recommended environment variables:
        - OPENAI_API_KEY
        - OPENAI_MODEL
        - OPENAI_BASE_URL

        Do not hardcode API keys in this file.
        """
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self._client = None

        # TODO:
        # Initialize the OpenAI client only if:
        # 1. OPENAI_API_KEY is available
        # 2. The openai package is installed
        if self.api_key and OpenAI is not None:
            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @property
    def enabled(self) -> bool:
        """
        Return True when LLM-enhanced mode is available.
        """
        return self._client is not None

    def build_context(self, sources: List[SourceDocument]) -> str:
        """
        TODO:
        Convert source documents into a compact context string for the LLM.

        Suggested format:
        [1] Source title
        URL: source url
        Snippet: source snippet
        Summary: source summary or source content

        Keep each source short enough to avoid sending too much text.
        """
        context_chunks = []

        for idx, src in enumerate(sources, start=1):
            content = src.summary or src.content

            # TODO:
            # Adjust this limit based on the model/context window you use.
            content = content[:1800]

            context_chunks.append(
                f"[{idx}] {src.title}\n"
                f"URL: {src.url}\n"
                f"Snippet: {src.snippet}\n"
                f"Summary: {content}"
            )

        return "\n\n".join(context_chunks)

    def build_prompt(self, topic: str, context: str) -> str:
        """
        TODO:
        Create a strong instruction prompt for the LLM.

        The prompt should:
        - Define the role of the model.
        - Specify the report structure.
        - Tell the model to use only provided sources.
        - Require numbered citations.
        - Include the topic and source context.
        """
        return (
            "You are a research analyst. Create a markdown research report.\n"
            "\n"
            "Required sections:\n"
            "1) Executive Summary\n"
            "2) Background and Context\n"
            "3) Current Landscape\n"
            "4) Key Challenges and Risks\n"
            "5) Opportunities and Future Outlook\n"
            "6) Actionable Recommendations\n"
            "7) References\n"
            "\n"
            "Use only the provided sources. Do not invent facts.\n"
            "Use numbered citations like [1], [2], [3].\n"
            f"\nTopic: {topic}\n\n"
            f"Sources:\n{context}"
        )

    def write_report(self, topic: str, sources: List[SourceDocument]) -> str:
        """
        TODO:
        Use the LLM to write a markdown report.

        Requirements:
        - If no client is configured, return an empty string.
        - Build source context.
        - Build a prompt.
        - Call the model.
        - Return the generated markdown text.
        """
        if not self._client:
            return ""

        context = self.build_context(sources)
        prompt = self.build_prompt(topic, context)

        # TODO:
        # Try changing temperature, model, or prompt structure.
        response = self._client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.2,
        )

        return (response.output_text or "").strip()