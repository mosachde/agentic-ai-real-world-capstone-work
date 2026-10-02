from __future__ import annotations

import re
from collections import Counter
from typing import List


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "in", "is", "it", "its", "of", "on", "or", "that", "the", "to", "was",
    "were", "will", "with", "this", "these", "those", "their", "there",
    "which", "about", "into", "than", "also", "can", "may", "more", "most",
}


def _sentence_split(text: str) -> List[str]:
    """
    Split raw text into candidate sentences.

    TODO:
    Improve sentence splitting if your sources contain messy web text,
    bullet lists, tables, or short fragments.
    """

    chunks = re.split(r"(?<=[.!?])\s+", text.strip())
    cleaned = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 25]

    if cleaned:
        return cleaned

    line_chunks = [line.strip() for line in text.splitlines()]
    return [line for line in line_chunks if len(line) > 25]


def _tokenize(text: str) -> List[str]:
    """
    Convert text into lowercase keyword tokens.

    TODO:
    Improve tokenization for your capstone use case.

    Possible enhancements:
    - Add domain-specific stopwords
    - Keep important acronyms
    - Handle numbers, dates, and named entities
    - Use an NLP library for better preprocessing
    """

    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]+", text.lower())

    return [
        word
        for word in words
        if word not in STOPWORDS and len(word) > 2
    ]


def summarize_text(
    text: str,
    topic: str,
    max_sentences: int = 5,
) -> str:
    """
    Create an extractive summary for one source document.

    Current starter approach:
    - Split text into sentences.
    - Score sentences based on keyword frequency.
    - Boost sentences that contain topic words.
    - Return the highest-scoring sentences in original order.

    TODO:
    Improve the summarization strategy.

    Ideas:
    - Use LLM-based summarization
    - Use embeddings to rank sentences by relevance
    - Add citation-aware summaries
    - Remove duplicate or low-quality sentences
    - Prefer recent statistics, examples, and named entities
    """

    sentences = _sentence_split(text)

    if not sentences:
        return ""

    topic_tokens = set(_tokenize(topic))
    all_tokens = _tokenize(text)
    token_freq = Counter(all_tokens)

    def sentence_score(sentence: str) -> float:
        tokens = _tokenize(sentence)

        if not tokens:
            return 0.0

        base_score = sum(token_freq[token] for token in tokens) / max(len(tokens), 1)

        topic_boost = sum(
            2.0
            for token in tokens
            if token in topic_tokens
        )

        length_penalty = 0.0 if 12 <= len(tokens) <= 45 else 0.3

        return base_score + topic_boost - length_penalty

    ranked = sorted(
        sentences,
        key=sentence_score,
        reverse=True,
    )

    selected = ranked[:max_sentences]
    selected_set = set(selected)

    selected_in_order = [
        sentence
        for sentence in sentences
        if sentence in selected_set
    ]

    return " ".join(selected_in_order)


def summarize_documents(
    doc_summaries: List[str],
    topic: str,
    limit: int = 8,
) -> List[str]:
    """
    Combine multiple document summaries into report bullets.

    TODO:
    Improve how summaries are merged.

    Ideas:
    - Group findings by theme
    - Rank findings by relevance to the topic
    - Remove near-duplicates
    - Generate stronger executive-summary bullets
    - Use an LLM to synthesize across sources
    """

    bullets: List[str] = []
    seen = set()

    for summary in doc_summaries:
        for sentence in _sentence_split(summary):
            normalized = re.sub(r"\W+", "", sentence.lower())

            if normalized and normalized not in seen:
                bullets.append(sentence)
                seen.add(normalized)

            if len(bullets) >= limit:
                return bullets

    return bullets