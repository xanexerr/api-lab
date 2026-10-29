# API Lab: QuickPizza

## Setup

Requirements: Python 3.10 or newer, Git, and `curl.exe` on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the complete suite from this directory:

```powershell
pytest -v
```

Create a self-contained HTML report:
```powershell
pytest -v --html=report.html --self-contained-html
```

<a href="https://github.com/xanexerr/api-lab/blob/main/report.html" target="_blank">Open My Report Here!</a>


| Characteristic | Blocks and test values | Test coverage |
| --- | --- | --- |
| C1: stars value | Below range: `0`; valid base: `3`; above range: `6` | `test_stars_out_of_range`, `test_base_choice_is_saved` |
| C2: stars type | Integer base: `3`; decimal: `3.5`; text: `"3"`; missing | `test_base_choice_is_saved`, `test_stars_type_blocks` |
| C3: pizza existence | Existing fixture pizza; nonexistent ID `999999999` | `test_base_choice_is_saved`, `test_nonexistent_pizza_is_refused` |
| C4: token | Own logged-in token; no header; made-up short token | `test_base_choice_is_saved`, `test_missing_token_is_refused`, `test_made_up_token_cannot_read_ratings` |

The lab prohibits creating or changing ratings with tokens that were not obtained by logging in. The made-up token is therefore checked with a read-only GET. QuickPizza currently returns the shared ratings list for that token; the expected rejection is recorded as an expected failure.

## Findings

`RESULTS.md` records the observed defect details and reflection answers. The all-tools-excluded pizza request currently returns HTTP 500 with an empty body. A made-up token also receives HTTP 200 and the shared ratings list. These expected failures remain visible in the test report.
