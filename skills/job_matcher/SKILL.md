---
name: "job_matcher"
description: "Rank internship or job listings against a keyword profile and generate a short markdown shortlist."
---

# Job Matcher

Use this skill when the user wants to compare a CSV of job listings against a candidate profile.

## Inputs

- A CSV file with at least `title`, `company`, `location`, `url`, and `description` columns.
- A text file with one keyword or phrase per line.

## Workflow

1. Confirm the CSV path and keyword profile path.
2. Run:

```bash
python3 scripts/score_jobs.py \
  --jobs <jobs.csv> \
  --profile <keywords.txt> \
  --output reports/generated/job_matches.md \
  --top 5
```

3. Return the top matches with score, matched skills, and a short explanation.

## Output

- A Markdown report that is easy to review, share, or commit.
