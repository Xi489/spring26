#!/usr/bin/env python3

import argparse
import csv
import pathlib
import re
from typing import Dict, List, Sequence, Tuple


TITLE_WEIGHT = 3
DESC_WEIGHT = 2
LOCATION_WEIGHT = 1


def normalize(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"\s+", " ", lowered).strip()


def load_keywords(path: pathlib.Path) -> List[str]:
    keywords: List[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        keywords.append(normalize(line))
    return keywords


def read_jobs(path: pathlib.Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def match_keywords(text: str, keywords: Sequence[str]) -> List[str]:
    normalized = normalize(text)
    return [keyword for keyword in keywords if keyword in normalized]


def score_job(job: Dict[str, str], keywords: Sequence[str]) -> Tuple[int, List[str]]:
    title_matches = match_keywords(job.get("title", ""), keywords)
    desc_matches = match_keywords(job.get("description", ""), keywords)
    location_matches = match_keywords(job.get("location", ""), keywords)

    unique_matches: List[str] = []
    for keyword in title_matches + desc_matches + location_matches:
        if keyword not in unique_matches:
            unique_matches.append(keyword)

    score = (
        len(title_matches) * TITLE_WEIGHT
        + len(desc_matches) * DESC_WEIGHT
        + len(location_matches) * LOCATION_WEIGHT
    )
    return score, unique_matches


def build_report(scored_jobs: Sequence[Tuple[int, Dict[str, str], List[str]]], top_n: int) -> str:
    lines = [
        "# Job Match Report",
        "",
        f"Top {min(top_n, len(scored_jobs))} matches generated from the current job list.",
        "",
    ]

    for index, (score, job, matches) in enumerate(scored_jobs[:top_n], start=1):
        lines.extend(
            [
                f"## {index}. {job.get('title', 'Untitled Role')} - {job.get('company', 'Unknown Company')}",
                f"- Score: {score}",
                f"- Location: {job.get('location', 'N/A')}",
                f"- Matched skills: {', '.join(matches) if matches else 'None'}",
                f"- Link: {job.get('url', 'N/A')}",
                f"- Summary: {job.get('description', '').strip()}",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank job listings against a keyword profile.")
    parser.add_argument("--jobs", required=True, help="Path to the job CSV file.")
    parser.add_argument("--profile", required=True, help="Path to the keyword profile text file.")
    parser.add_argument("--output", required=True, help="Path to the generated markdown report.")
    parser.add_argument("--top", type=int, default=5, help="Number of top matches to include.")
    args = parser.parse_args()

    jobs_path = pathlib.Path(args.jobs)
    profile_path = pathlib.Path(args.profile)
    output_path = pathlib.Path(args.output)

    keywords = load_keywords(profile_path)
    jobs = read_jobs(jobs_path)

    scored_jobs: List[Tuple[int, Dict[str, str], List[str]]] = []
    for job in jobs:
        score, matches = score_job(job, keywords)
        scored_jobs.append((score, job, matches))

    scored_jobs.sort(
        key=lambda item: (
            item[0],
            len(item[2]),
            normalize(item[1].get("title", "")),
        ),
        reverse=True,
    )

    report = build_report(scored_jobs, args.top)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote report to {output_path}")


if __name__ == "__main__":
    main()
