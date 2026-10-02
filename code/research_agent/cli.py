from __future__ import annotations

import argparse
from pathlib import Path

from research_agent.agent import ResearchAgent, render_report


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Example:

    python -m research_agent.cli \
        "Impact of AI on healthcare" \
        --max-sources 8 \
        --output report.md
    """

    parser = argparse.ArgumentParser(
        description="Research a topic and generate a markdown report."
    )

    parser.add_argument(
        "topic",
        help="Topic to research"
    )

    parser.add_argument(
        "--max-sources",
        type=int,
        default=8,
        help="Maximum number of sources to include"
    )

    parser.add_argument(
        "--output",
        default="research_report.md",
        help="Output markdown file path"
    )

    return parser.parse_args()


def main() -> None:
    """
    Main application workflow.

    TODO:
    Review and customize this workflow as part of your capstone project.

    Suggested enhancements:
    - Add additional configuration options.
    - Allow users to choose different research modes.
    - Add support for custom report templates.
    - Add logging and error handling.
    """

    args = parse_args()

    # Create the research agent.
    agent = ResearchAgent()

    # Configure the maximum number of sources.
    agent.config.max_sources = max(3, args.max_sources)

    # TODO:
    # Execute the research workflow.
    report = agent.research(args.topic)

    # TODO:
    # Convert the report into markdown output.
    markdown = render_report(report)

    # Save the report.
    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Research completed for: {args.topic}")
    print(f"Saved report to: {output_path.resolve()}")
    print(f"Sources used: {len(report.references)}")

    # Optional enhancement ideas:
    #
    # TODO:
    # Display a short executive summary in the console.
    #
    # TODO:
    # Export reports in additional formats (PDF, DOCX, HTML).
    #
    # TODO:
    # Add progress indicators while research is running.


if __name__ == "__main__":
    main()