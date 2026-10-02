from __future__ import annotations

from urllib.parse import quote_plus, urlparse

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None  # type: ignore[assignment]

from .models import SearchResult, SourceDocument


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}


class WebResearchClient:
    """
    Web research client used to:
    1. Search the web.
    2. Retrieve source content.
    3. Convert pages into SourceDocument objects.

    TODO:
    Improve the search and retrieval strategy.
    """

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout

    def search(self, query: str, limit: int = 8) -> list[SearchResult]:
        """
        Search the web for a topic.

        TODO:
        Implement one or more search strategies.

        Ideas:
        - Bing
        - DuckDuckGo
        - Tavily
        - SerpAPI
        - News APIs
        - Custom search providers
        """

        if BeautifulSoup is None:
            raise RuntimeError(
                "beautifulsoup4 is required for web search parsing."
            )

        # Starter implementation:
        return self._search_bing(query, limit=limit)

    def _search_bing(self, query: str, limit: int = 8) -> list[SearchResult]:
        """
        Basic Bing search implementation.

        TODO:
        Improve result quality and metadata extraction.
        """

        url = (
            f"https://www.bing.com/search?q={quote_plus(query)}"
            f"&count={max(limit, 10)}"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=self.timeout,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        results: list[SearchResult] = []

        for node in soup.select("li.b_algo"):
            link = node.select_one("h2 a")

            if not link:
                continue

            title = link.get_text(strip=True)
            href = link.get("href", "")

            results.append(
                SearchResult(
                    title=title,
                    url=href,
                    snippet="",
                    query=query,
                )
            )

            if len(results) >= limit:
                break

        return results

    def fetch_source(
        self,
        result: SearchResult,
        max_chars: int = 12000,
    ) -> SourceDocument:
        """
        Retrieve page content from a URL.

        TODO:
        Improve content extraction.

        Ideas:
        - Remove navigation content
        - Preserve article structure
        - Extract publication dates
        - Capture authors
        - Use readability libraries
        """

        text = ""

        try:
            if BeautifulSoup is None:
                raise RuntimeError(
                    "beautifulsoup4 is required."
                )

            response = requests.get(
                result.url,
                headers=HEADERS,
                timeout=self.timeout,
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser",
            )

            paragraphs = []

            for node in soup.find_all("p"):
                content = node.get_text(
                    " ",
                    strip=True,
                )

                if content:
                    paragraphs.append(content)

            text = "\n".join(paragraphs)

            if len(text) > max_chars:
                text = text[:max_chars]

        except Exception as exc:
            text = (
                f"Could not retrieve source content. "
                f"Error: {exc}"
            )

        return SourceDocument(
            title=result.title,
            url=result.url,
            snippet=result.snippet,
            query=result.query,
            content=text,
        )


def deduplicate_results(
    results: list[SearchResult],
    keep: int,
) -> list[SearchResult]:
    """
    Remove duplicate search results.

    TODO:
    Improve the deduplication strategy.

    Ideas:
    - URL normalization
    - Domain diversity
    - Similarity scoring
    - Source ranking
    """

    seen_urls = set()
    deduped: list[SearchResult] = []

    for result in results:
        if result.url in seen_urls:
            continue

        seen_urls.add(result.url)
        deduped.append(result)

        if len(deduped) >= keep:
            break

    return deduped