#!/usr/bin/env python3
"""
log-analysis-toolkit

CLI tool to scan log files, filter entries by pattern or date, and export results.
Supports JSON, CSV, or plain text output.
"""

import re
import click
from datetime import datetime, timedelta

TIMESTAMP_REGEX = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')
LOGLEVEL_REGEX = re.compile(r'\b(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\b', re.IGNORECASE)

@click.command()
@click.option('-i', '--input', 'infile', required=True, help='Log file to parse.')
@click.option('-p', '--pattern', default=None, help='Regex to filter log lines.')
@click.option('--start-date', default=None, help='Start date (YYYY-MM-DD). Lines before this are skipped.')
@click.option('--end-date', default=None, help='End date (YYYY-MM-DD). Lines on/after this are skipped.')
@click.option('-o', '--output', 'outfile', default=None, help='Optional file to write results.')
@click.option('-f', '--format', 'outfmt',
              type=click.Choice(['text', 'json', 'csv']), default='text', show_default=True,
              help='Output format.')
def main(infile, pattern, start_date, end_date, outfile, outfmt):
    regex = re.compile(pattern) if pattern else None
    start_dt = datetime.fromisoformat(start_date) if start_date else None
    end_dt = datetime.fromisoformat(end_date) + timedelta(days=1) if end_date else None

    results = []

    with open(infile, 'r') as f:
        for line in f:
            line = line.rstrip('\n')

            ts_match = TIMESTAMP_REGEX.search(line)
            timestamp_str = ts_match.group('timestamp') if ts_match else ''
            timestamp = None
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except ValueError:
                    timestamp = None

            if (start_dt or end_dt) and not timestamp:
                continue

            if timestamp:
                if start_dt and timestamp < start_dt:
                    continue
                if end_dt and timestamp >= end_dt:
                    continue

            if regex and not regex.search(line):
                continue

            lvl_match = LOGLEVEL_REGEX.search(line)
            level = lvl_match.group('level').upper() if lvl_match else ''

            results.append({
                'timestamp': timestamp_str,
                'level': level,
                'line': line
            })

    if outfmt == 'text':
        output_data = '\n'.join(item['line'] for item in results)
    elif outfmt == 'json':
        import json
        output_data = json.dumps(results, indent=2)
    else:
        import csv
        from io import StringIO
        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=['timestamp', 'level', 'line'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
        output_data = buf.getvalue()

    if outfile:
        with open(outfile, 'w') as f:
            f.write(output_data)
    else:
        click.echo(output_data)

if __name__ == '__main__':
    main()
