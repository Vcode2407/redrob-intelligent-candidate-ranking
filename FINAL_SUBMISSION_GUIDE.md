# Final Submission Guide

## Placeholder Metadata Table

| Field | Required Value | Status |
|---|---|---|
| `team_name` | Final registered team name | Missing human input |
| `primary_contact.name` | Primary contact full name | Missing human input |
| `primary_contact.email` | Primary contact email | Missing human input |
| `primary_contact.phone` | Primary contact phone number | Missing human input |
| `team_members[0].name` | Team member full name | Missing human input |
| `team_members[0].email` | Team member email | Missing human input |
| `github_repo` | Public or organizer-accessible GitHub repository URL | Missing human input |
| `sandbox_link` | Working hosted sandbox or demo URL | Missing human input |
| `compute.platform` | Final machine/platform used for submitted run | Review and confirm |
| `compute.cpu_cores` | Final CPU core count | Review and confirm |
| `compute.ram_gb` | Final RAM in GB | Review and confirm |
| `compute.python_version` | Exact Python version from final environment | Review and confirm |
| `compute.os` | Exact OS from final environment | Review and confirm |

## GitHub Repository Checklist

| Check | Status |
|---|---|
| README completeness | Complete: setup, reproduction command, approach, layout, tests |
| Architecture docs | Complete: `docs/architecture.md` |
| Scoring docs | Complete: `docs/scoring_methodology.md` |
| Analysis docs | Complete: `docs/analysis_report.md` |
| PPT/PDF content | Complete: `FINAL_PDF_SUBMISSION_CONTENT.md` and `docs/ppt_content.md` |
| Requirements file | Complete: `requirements.txt` |
| Reproducibility instructions | Complete: `README.md` and `run.py` |
| Submission metadata template | Present but placeholders remain |
| Tests | Complete: `tests/test_core.py` |
| Generated CSV | Complete: `submission.csv` and `outputs/submission.csv` |
| Debug audit artifact | Reproducible locally with `--debug-json`; not committed |

## Deliverable Verification

| Deliverable | Expected File / Link | Status |
|---|---|---|
| `submission.csv` | `submission.csv` | Exists |
| GitHub repository | Final remote URL in `submission_metadata.yaml` | Missing human action |
| PDF/PPT | Export from `FINAL_PDF_SUBMISSION_CONTENT.md` into official template | Content ready; export missing |
| Metadata | `submission_metadata.yaml` | Exists; placeholders remain |
| Sandbox link | Final hosted demo URL | Missing human action |

## Step 1: Create GitHub Repository

1. Create a GitHub repository for `redrob_ranker`.
2. Use a clear name such as `redrob-candidate-ranker`.
3. Keep it public if possible, or ensure organizer access can be granted.

## Step 2: Upload Code

1. Commit the full `redrob_ranker/` directory.
2. Include source, docs, tests, `submission.csv`, and metadata.
3. Do not commit the full `candidates.jsonl` file.
4. Confirm `requirements.txt` and `README.md` are in the repository root.

## Step 3: Verify Files

Run:

```bash
python run.py --candidates ./data/candidates.jsonl --out ./submission.csv
python -m unittest discover -s tests
python validate_submission.py submission.csv
```

Expected:

- The ranking command completes under 5 minutes.
- Tests pass.
- Validator reports `Submission is valid.`

## Step 4: Export PDF

1. Open the official Redrob idea submission template.
2. Fill it using `FINAL_PDF_SUBMISSION_CONTENT.md`.
3. Export the completed deck/template as PDF.
4. Check that all slide titles, bullets, diagrams, and presenter notes are represented clearly.

## Step 5: Fill Metadata

1. Replace placeholders in `submission_metadata.yaml`.
2. Add final GitHub repository URL.
3. Add final sandbox/demo link.
4. Confirm compute environment details match the machine used for the final run.
5. Keep AI usage declaration honest and consistent with the code.

## Step 6: Submit On Portal

1. Upload `submission.csv`.
2. Enter portal metadata exactly as in `submission_metadata.yaml`.
3. Upload or link the final PDF/PPT assets if required by the portal.
4. Provide GitHub repository URL.
5. Provide sandbox/demo URL.
6. Submit only after all missing human-input items below are resolved.

## Missing Items

- Final team name.
- Primary contact name, email, and phone.
- Final team member names and emails.
- Final GitHub repository URL.
- Final sandbox/demo link.
- Final exact compute environment values if different from the current placeholders.
- Exported PDF/PPT file from the provided slide content.

## Technical Status

TECHNICAL SUBMISSION COMPLETE

The code, CSV, docs, tests, validator-compatible output, audit report, and slide content are complete. Remaining work is manual submission packaging: identity metadata, GitHub remote, sandbox link, and PDF/PPT export.
