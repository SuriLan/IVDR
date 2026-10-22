#!/usr/bin/env python3
"""
EMDN code lookup helper for IVDR classification work.

Searches an EMDN export (xlsx) for terms and prints matching codes with their
full ancestor path, so the analyst can pick the correct terminal code.

Usage:
    search_emdn.py <emdn.xlsx> <keyword1> [keyword2 ...]
    search_emdn.py <emdn.xlsx> --path W01021314

Options:
    --path CODE   Print the full ancestor chain for the given code
    --sheet NAME  Sheet name to read (default: first sheet)

Examples:
    search_emdn.py EMDN_v2026_EN.xlsx "ST2" "cardiac"
    search_emdn.py EMDN_v2026_EN.xlsx --path W0105020102
"""

import sys
from pathlib import Path

import openpyxl


def load_rows(xlsx_path, sheet_name=None):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    ws = wb[sheet_name] if sheet_name else wb[wb.sheetnames[0]]
    rows = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        if row and row[2]:  # code column
            rows.append(row)
    return rows


def ancestor_path(rows, code):
    path = []
    for r in rows:
        if code.startswith(str(r[2])):
            path.append(r)
    return path


def fmt(row):
    return f"{row[2]} | {row[3]} | L{row[4]} | terminal={row[5]}"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1

    xlsx = args[0]
    sheet = None
    if "--sheet" in args:
        i = args.index("--sheet")
        sheet = args[i + 1]
        del args[i : i + 2]

    if not Path(xlsx).exists():
        print(f"ERROR: file not found: {xlsx}")
        return 1

    rows = load_rows(xlsx, sheet)

    if "--path" in args:
        i = args.index("--path")
        code = args[i + 1]
        print(f"=== Ancestor path for {code} ===")
        for r in ancestor_path(rows, code):
            print(fmt(r))
        return 0

    keywords = [k.upper() for k in args[1:]]
    print(f"=== Matching codes (keywords: {', '.join(args[1:])}) ===")
    for r in rows:
        term = str(r[3]).upper()
        if all(kw in term for kw in keywords):
            print(fmt(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
