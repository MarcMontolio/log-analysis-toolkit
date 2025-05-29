<p align="center">
  <img src="https://img.shields.io/github/workflow/status/MarcMontolio/log-analysis-toolkit/CI?label=CI&logo=github" alt="CI">
  <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/github/license/MarcMontolio/log-analysis-toolkit" alt="License">
</p>

# 🪵 Log Analysis Toolkit

> **CLI tool for parsing logs, filtering by pattern or date, and exporting the results**

* 🔍 Regex-based filtering
* 📅 Date range support (ISO 8601)
* 📄 Output as text, JSON, or CSV
* 🧪 Tests included (pytest)
* ⚙️ GitHub Actions for lint and test CI

---

## 📋 Table of Contents

* [📋 Prerequisites](#-prerequisites)
* [🔧 Installation](#-installation)
* [▶️ Usage](#-usage)
* [🔍 Examples](#-examples)
* [⚙️ Advanced Options](#-advanced-options)
* [🧪 Tests](#-tests)
* [🤝 Contributing](#-contributing)
* [📜 License](#-license)

---

## 📋 Prerequisites

* Python 3.7+
* Access to log files you want to parse

---

## 🔧 Installation

```bash
git clone https://github.com/MarcMontolio/log-analysis-toolkit.git
cd log-analysis-toolkit
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\Activate.ps1     # Windows PowerShell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Usage

Basic example:

```bash
python src/log_tool.py \
  --input examples/sample.log \
  --pattern "ERROR" \
  --format text \
  --output examples/errors.log
```

CLI options:

* `-i, --input`: Path to log file
* `-p, --pattern`: Filter logs using regex
* `--start-date`: Start filtering from this date (YYYY-MM-DD)
* `--end-date`: Stop filtering after this date (inclusive)
* `-f, --format`: Output type: `text`, `json`, or `csv`
* `-o, --output`: Write output to file (prints to terminal if omitted)

---

## 🔍 Examples

More usage examples are in [`docs/usage.md`](docs/usage.md).

---

## ⚙️ Advanced Options

Want to customize?

* Edit regex or timestamp logic in `src/log_tool.py` to match your log structure.

---

## 🧪 Tests

Run tests with:

```bash
pytest -q
```

---

## 🤝 Contributing

* Fork the repository
* Branch out
* Test your changes
* Open a PR

---

## 📜 License

MIT © 2025 Marc Montolio
