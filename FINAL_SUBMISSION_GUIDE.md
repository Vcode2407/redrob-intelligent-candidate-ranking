# Final Submission Guide

This guide covers the manual portal steps after the GitHub repository and `submission.csv` have been prepared.

## Metadata Check

| Field | Current Value | Status |
|---|---|---|
| `team_name` | `Vkodes` | Filled |
| `primary_contact.name` | `Vinay Kumar` | Filled |
| `primary_contact.email` | `vkslog69@gmail.com` | Filled |
| `primary_contact.phone` | `8309976969` | Filled |
| `team_members[0].name` | `Vinay Kumar` | Filled |
| `team_members[0].email` | `vkslog69@gmail.com` | Filled |
| `github_repo` | `https://github.com/Vcode2407/redrob-intelligent-candidate-ranking` | Filled |
| `sandbox_link` | Blank | Fill only if the portal requires a live demo link |
| `compute.platform` | Local Intel i7 CPU | Filled |
| `compute.cpu_cores` | `8` logical cores | Filled |
| `compute.ram_gb` | `15` | Filled |
| `compute.python_version` | `3.12.10` | Filled |
| `compute.os` | `Microsoft Windows 11 Pro` | Filled |

## Repository Checklist

| Check | Status |
|---|---|
| README | Includes overview, setup, reproduction, validation, runtime, and scoring summary |
| Architecture docs | `docs/architecture.md` |
| Scoring docs | `docs/scoring_methodology.md` |
| JD/signal analysis | `docs/analysis_report.md` |
| Slide/PDF content | `FINAL_PDF_SUBMISSION_CONTENT.md` and `docs/ppt_content.md` |
| Requirements file | `requirements.txt` |
| Tests | `tests/test_core.py` |
| Final CSV | `submission.csv` |
| Raw candidate dataset | Not committed |
| Output/debug artifacts | Not committed; can be regenerated locally |

## Reproduction Commands

Run from the repository root:

```bash
python run.py --candidates ./data/candidates.jsonl --out ./submission.csv
python -m unittest discover -s tests
python validate_submission.py submission.csv
```

Expected local results:

- ranking completes under the 5-minute CPU limit.
- unit tests pass.
- official validator prints `Submission is valid.`

## Portal Steps

1. Confirm the final `submission.csv` is the root-level file from this repository.
2. Use the generated `Vkodes_Redrob_Submission.pdf` and `Vkodes_Redrob_Submission.pptx`, or re-export from `FINAL_PDF_SUBMISSION_CONTENT.md` if the portal requires another format.
3. Enter the team and contact fields from `submission_metadata.yaml`.
4. Add the GitHub URL: `https://github.com/Vcode2407/redrob-intelligent-candidate-ranking`.
5. Add a sandbox/demo URL only if one has been created.
6. Upload the CSV and PDF/PPT on the Redrob portal.
7. Submit after checking that the portal preview shows the right files and links.

## Remaining Manual Item

- Replace `sandbox_link` only if the Redrob portal requires a live demo URL.
