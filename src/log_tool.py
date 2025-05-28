#!/usr/bin/env python3
"""
log-analysis-toolkit

A simple CLI to parse log files, filter by patterns or date ranges,
and output results in CSV or JSON.
"""

import re
import click
from datetime import datetime

TIMESTAMP_REGEX = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')
LOGLEVEL_REGEX = re.compile(r'\b(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\b', re.IGNORECASE)

@click.command()
@click.option('-i', '--input', 'infile', required=True, help='Path to log file.')
@click.option('-p', '--pattern', default=None, help='Regex pattern to filter lines.')
@click.option('--start-date', default=None, help='Filter logs starting from this ISO date (YYYY-MM-DD).')
@click.option('--end-date', default=None, help='Filter logs up to this ISO date (YYYY-MM-DD).')
@click.option('-o', '--output', 'outfile', default=None, help='Path to write filtered output (optional).')
@click.option('-f', '--format', 'outfmt', type=click.Choice(['text', 'json', 'csv']), default='text', show_default=True, help='Output format.')
def main(infile, pattern, start_date, end_date, outfile, outfmt):
    """
    Reads a log file, applies an optional regex filter and date range filter, and outputs matching lines.
    Automatically extracts timestamps and log levels when available.
    """
    regex = re.compile(pattern) if pattern else None
    start_dt = datetime.fromisoformat(start_date) if start_date else None
    end_dt = datetime.fromisoformat(end_date) if end_date else None
    results = []

    with open(infile, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            # Extract timestamp
            timestamp_match = TIMESTAMP_REGEX.search(line)
            timestamp_str = timestamp_match.group('timestamp') if timestamp_match else ''
            timestamp = None
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                    if (start_dt and timestamp < start_dt) or (end_dt and timestamp > end_dt):
                        continue
                except ValueError:
                    pass

            # Regex filter
            if regex and not regex.search(line):
                continue

            # Extract log level
            level_match = LOGLEVEL_REGEX.search(line)
            level = level_match.group('level').upper() if level_match else ''

            results.append({
                'timestamp': timestamp_str,
                'level': level,
                'line': line
            })

    # Output
    if outfmt == 'text':
        output_data = '\n'.join([item['line'] for item in results])
    elif outfmt == 'json':
        import json
        output_data = json.dumps(results, indent=2)
    else:  # csv
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
