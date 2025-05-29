import json
import csv
from click.testing import CliRunner
from datetime import datetime
import pytest

import src.log_tool as log_tool

SAMPLE_LOG = """\
2025-05-01T10:00:00 INFO Starting process
2025-05-01T10:05:00 DEBUG Debugging details
2025-05-02T12:00:00 WARNING A warning occurred
2025-05-03T15:30:00 ERROR An error occurred
Unformatted line without timestamp
"""

@pytest.fixture
def log_file(tmp_path):
    path = tmp_path / "app.log"
    path.write_text(SAMPLE_LOG)
    return str(path)

def run_cli(args):
    runner = CliRunner()
    result = runner.invoke(log_tool.main, args)
    return result.exit_code, result.output

def test_text_output_no_filters(log_file):
    code, out = run_cli(["-i", log_file])
    assert code == 0
    for line in SAMPLE_LOG.splitlines():
        assert line in out

def test_filter_by_pattern(log_file):
    code, out = run_cli(["-i", log_file, "-p", "ERROR"])
    assert code == 0
    lines = out.splitlines()
    assert any("ERROR An error occurred" in l for l in lines)
    assert not any("WARNING" in l for l in lines)

def test_filter_by_date_range(log_file):
    code, out = run_cli([
        "-i", log_file,
        "--start-date", "2025-05-02",
        "--end-date", "2025-05-02"
    ])
    assert code == 0
    lines = out.splitlines()
    assert any("2025-05-02T12:00:00 WARNING" in l for l in lines)
    assert all("INFO" not in l and "ERROR" not in l for l in lines)

@pytest.mark.parametrize("fmt", ["json", "csv"])
def test_output_formats(log_file, fmt, tmp_path):
    out_file = tmp_path / f"out.{fmt}"
    code, _ = run_cli(["-i", log_file, "-o", str(out_file), "-f", fmt])
    assert code == 0

    raw = out_file.read_text()
    if fmt == "json":
        data = json.loads(raw)
        assert isinstance(data, list)
        assert all(k in data[0] for k in ("timestamp", "level", "line"))
    else:
        reader = csv.DictReader(raw.splitlines())
        rows = list(reader)
        assert reader.fieldnames == ["timestamp", "level", "line"]
        assert any(r["timestamp"].startswith("2025-05-01T10:00:00") for r in rows)

def test_log_level_extraction(log_file, tmp_path):
    out_file = tmp_path / "levels.json"
    code, _ = run_cli(["-i", log_file, "-o", str(out_file), "-f", "json"])
    assert code == 0
    data = json.loads(out_file.read_text())
    levels = [entry["level"] for entry in data if entry["level"]]
    assert set(["INFO", "DEBUG", "WARNING", "ERROR"]).issubset(set(levels))

def test_date_filter_excludes_all(log_file):
    code, out = run_cli([
        "-i", log_file,
        "--start-date", "2026-01-01",
        "--end-date", "2026-01-31"
    ])
    assert code == 0
    assert out.strip() == ""

def test_includes_unstructured_lines(log_file):
    code, out = run_cli(["-i", log_file])
    assert code == 0
    assert "Unformatted line without timestamp" in out
