# Capstone Checkpoint 3.1: Retrieval Design

**Thesis Check: Grounding Claims in SEC Filings**

Mohit Sachdeva | Agentic AI Program | October 2026

## 1. Is retrieval required?

Yes, for text. Thesis Check needs two kinds of evidence. Reported numbers, such as revenue and cost of revenue, come from the SEC's structured XBRL data, so the agent looks them up exactly. I don't use semantic search for numbers, since it can return the right figure from the wrong quarter.

Everything else is text: why a margin fell, what management expects next quarter, which new risks have appeared. That text needs retrieval. It was filed after the model's training cutoff, and it has no fixed location or wording: a margin explanation might sit in the 10-Q or the earnings release, and talk about "inventory provisions" rather than "gross margin." Forward-looking claims can only be tested this way, because guidance never appears in XBRL. Pasting whole filings into the prompt isn't practical either: a 10-K runs past 100 pages, and the Fact-Checker needs a specific passage to verify.

## 2. How retrieval fits in

Retrieval replaces the starter template's web search. An ingest step (plain code, not an agent) downloads two years of 10-K, 10-Q and 8-K earnings releases for each ticker from SEC EDGAR. It splits them into chunks, embeds them (for example with OpenAI's `text-embedding-3-small`) and stores them in Chroma with their form, period, section and accession number. New filings are added as they appear, which also triggers the quarterly re-check.

Only the Filing Researcher searches the index, through a `search_filings` tool that filters by ticker, form and period, then ranks by similarity. Every passage comes back with its citation. If the results don't answer the claim, the Researcher's ReAct loop rephrases the query or tries another filing.

## 3. Retrieval in action

Take the thesis "AI demand will keep gross margins above 60%," and one confirmed claim: management's outlook keeps gross margin at or above 60%.

A prompt-only chatbot answers from training data that management "remains confident in strong margins." There's no source, and the investor feels reassured. Without the retrieval tool, Thesis Check has nothing to cite and marks the claim "insufficient evidence" rather than guessing. With retrieval on, the Researcher searches recent filings for "gross margin outlook next quarter." The top result, from the latest earnings release, says gross margin "is expected to be 58.0%, plus or minus 50 basis points." A 10-Q passage blames the recent drop on an inventory charge tied to export restrictions. The claim is marked Broken, with both passages cited. *(Illustrative; figures are hypothetical.)*

The retrieved passages also drive the debate. The Bear argues from the outlook, and the Bull can call the charge a one-time event only because that passage was found. The Fact-Checker then matches both quotes to the filing. All of this shows up in the run log, which records each query, its filters and the top results with their scores.

## 4. Key design choices

- **Source:** SEC filings only. They're primary, dated and citable. News and social posts are full of opinion and feed the bias the product is meant to counter.
- **Chunking:** filings are split by section first (Risk Factors, MD&A, the earnings-release outlook), then into chunks of about 500 tokens with a 50-token overlap, cut at paragraph breaks. A cause and its effect usually fit in a paragraph or two, and small chunks are easy to cite.
- **Chunk headers:** each chunk is labeled with company, form, period and section before embedding. This improves matching and keeps the period visible.
- **Results:** each search returns the top 5 passages and drops weak matches. The Researcher runs at most 3 searches per claim and keeps at most 5 passages. If the results miss, it asks a better question instead of pulling more.

## 5. Failure mode: a passage from the wrong period

Filings repeat a lot of wording from quarter to quarter. Last year's 10-K might say "we expect gross margins in the mid-60s," a near-perfect match for an outlook query, but out of date. If retrieved, it would pass the claim above and give the investor exactly the false reassurance the product exists to prevent.

The design handles this in four ways. Searches are filtered to the claim's period before ranking, so older filings can't outrank newer ones. Every citation shows its period and filing date. The Fact-Checker rejects a passage from the wrong period and sends the claim back for rework. And if nothing recent answers the claim, it's marked "insufficient evidence"; the search never quietly falls back to older filings. A golden-set test will check this: index an older filing with near-identical wording and confirm the citation always comes from the latest one.

## 6. Project repository

Repository: [https://github.com/mosachde/agentic-ai-real-world-capstone-work](https://github.com/mosachde/agentic-ai-real-world-capstone-work)

This checkpoint: [https://github.com/mosachde/agentic-ai-real-world-capstone-work/tree/module-3/docs](https://github.com/mosachde/agentic-ai-real-world-capstone-work/tree/module-3/docs)

Next build step: the EDGAR ingest pipeline and the `search_filings` tool.
