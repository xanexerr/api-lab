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

My Report:
<a href="https://xanexerr.github.io/api-lab/report.html?sort=result" target="_blank">Open My Report Here!</a>


## Findings

`RESULTS.md` records the observed defect details and reflection answers. The all-tools-excluded pizza request currently returns HTTP 500 with an empty body. A made-up token also receives HTTP 200 and the shared ratings list. These expected failures remain visible in the test report.
