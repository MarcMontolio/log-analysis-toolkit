# Log Toolkit — Usage Guide

This short guide shows how to use the CLI for `log-analysis-toolkit`. Nothing fancy, just what you need.

---

## Requirements

* Python 3.7 or newer
* Access to the log files you want to read
* Virtual environment optional, but smart

---

## Setup

```bash
git clone https://github.com/MarcMontolio/log-analysis-toolkit.git
cd log-analysis-toolkit
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\Activate.ps1     # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Basic Usage

Run the script like this:

```bash
python src/log_tool.py \
  --input examples/sample.log \
  --pattern "ERROR" \
  --format text \
  --output examples/errors.log
```

### Options

* `-i, --input`: Path to your log file
* `-p, --pattern`: Regex to filter lines
* `--start-date`: From this date onward (format: YYYY-MM-DD)
* `--end-date`: Up to and including this date
* `-f, --format`: Output format: `text`, `json`, or `csv`
* `-o, --output`: File to save results; prints to terminal if left out

---

## Examples

### Just the errors

```bash
python src/log_tool.py -i examples/sample.log -p ERROR
```

### Logs from a specific date range, as JSON

```bash
python src/log_tool.py \
  -i examples/sample.log \
  --start-date 2025-05-02 \
  --end-date 2025-05-03 \
  -f json \
  -o examples/range.json
```

### Save warnings and up as CSV

```bash
python src/log_tool.py \
  -i examples/sample.log \
  -p "WARNING|ERROR|CRITICAL" \
  -f csv \
  -o examples/warnings.csv
```

---

## Custom Stuff

* **Timestamps not matching?**
  Edit the `TIMESTAMP_REGEX` in `src/log_tool.py` to match your format.

* **Running in CI?**
  Here's how you can fail a job if something bad pops up:

  ```bash
  python src/log_tool.py -i logs/app.log -p ERROR -o /dev/null
  if [ $? -ne 0 ]; then exit 1; fi
  ```

---

## Project Structure

```
log-analysis-toolkit/
├── .github/
│   └── workflows/ci.yml
├── docs/
│   └── usage.md
├── examples/
│   ├── sample.log
│   ├── errors.log
│   └── warnings.csv
├── src/
│   └── log_tool.py
├── tests/
│   └── test_log_tool.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Contributing

* Fork it
* Make your changes on a new branch
* Run tests with `pytest`
* Open a pull request

---

## License

MIT © 2025 Marc Montolio
