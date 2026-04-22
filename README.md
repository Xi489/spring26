# Job Match Agent

A small open-source project that uses an OpenClaw-friendly workflow to rank internship or job listings against a candidate profile.

## What it does

- Reads a CSV export of job listings.
- Scores each listing against a keyword profile.
- Writes a short Markdown report with the top matches and matched skills.
- Includes an OpenClaw skill so the workflow can be triggered from an agent session.

## Project structure

- `scripts/score_jobs.py`: CLI for scoring jobs and generating the report.
- `data/sample_jobs.csv`: Sample job data.
- `profiles/cdx_intern_keywords.txt`: Sample keyword profile.
- `skills/job_matcher/SKILL.md`: OpenClaw skill instructions.
- `reports/sample_report.md`: Example output generated from the sample data.

## Quick start

```bash
python3 scripts/score_jobs.py \
  --jobs data/sample_jobs.csv \
  --profile profiles/cdx_intern_keywords.txt \
  --output reports/generated/job_matches.md \
  --top 3
```

## Why this project

This is intentionally small and practical. It shows a complete loop: structured input, automated matching, and a result that is easy to review or share.
