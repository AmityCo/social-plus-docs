#!/usr/bin/env python3
"""
Reads the feature matrix from Google Sheets and generates a Mintlify-compatible MDX file.
Handles category grouping, notes, and splits SDK / UIKit into tabs.
"""

import csv
import io
import json
import os
import sys

import requests


# ---------------------------------------------------------------------------
# Column mapping (0-indexed) — matches the sheet structure
# ---------------------------------------------------------------------------
# Col 0:  Features
# Col 1:  SDK > Availability
# Col 2:  SDK > Platform Parity  (not used in output)
# Col 3:  SDK > Android
# Col 4:  SDK > iOS
# Col 5:  SDK > TS
# Col 6:  SDK > Flutter
# Col 7:  UIKit > Availability
# Col 8:  UIKit > Platform Parity  (not used in output)
# Col 9:  UIKit > Android
# Col 10: UIKit > iOS
# Col 11: UIKit > Web
# Col 12: UIKit > RN
# Col 13: UIKit > Flutter

SDK_COLS = {
    "Availability": 1,
    "Android": 3,
    "iOS": 4,
    "TS": 5,
    "Flutter": 6,
}

UIKIT_COLS = {
    "Availability": 7,
    "Android": 9,
    "iOS": 10,
    "Web": 11,
    "RN": 12,
    "Flutter": 13,
}

# Known category headers (these appear as section dividers in the sheet)
CATEGORIES = {
    "Discovery",
    "Activity Feeds",
    "Feed Management",
    "Posts",
    "Post Types",
    "Post Composition",
    "Posting Permissions (Community Posts Only)",
    "Stories",
    "Comments & Reactions",
    "Live Streaming",
    "Live Stream Creation",
    "Live Stream Capabilities",
    "Events",
    "Content Sharing & Management",
    "Notifications",
    "Users",
    "Communities",
    "Moderation",
    "Commerce",
    "Sponsored Content",
}

# Rows to skip (legend, headers, blank rows at the top)
LEGEND_KEYWORDS = {"Legend", "Full Parity", "Partial =", "Planned =", "Features", "SDK", "UIKit"}

# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_sheet_public(sheet_id: str, sheet_name: str) -> list[list[str]]:
    """Fetch raw rows via the public CSV export URL."""
    url = (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    reader = csv.reader(io.StringIO(resp.text))
    return [row for row in reader]


def fetch_sheet_service_account(sheet_id: str, sheet_name: str) -> list[list[str]]:
    """Fetch raw rows via Google Sheets API with a service account."""
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_SA_KEY"]),
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    service = build("sheets", "v4", credentials=creds)
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=sheet_name)
        .execute()
    )
    return result.get("values", [])


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def is_skip_row(row: list[str]) -> bool:
    """Return True if this row is part of the legend/header block."""
    if not row or not row[0].strip():
        return True
    first = row[0].strip()
    return any(kw in first for kw in LEGEND_KEYWORDS)


def is_category_row(row: list[str]) -> bool:
    """Return True if this row is a category header."""
    first = row[0].strip()
    if first in CATEGORIES:
        return True
    # Fallback: if only the first column has content and no data columns are filled,
    # it's likely a category header
    data_cells = [c.strip() for c in row[1:] if c.strip()]
    if first and not data_cells:
        return True
    return False


def safe_get(row: list[str], idx: int) -> str:
    """Safely get a cell value by index."""
    if idx < len(row):
        return row[idx].strip()
    return ""


def parse_rows(raw_rows: list[list[str]]) -> list[dict]:
    """
    Parse raw sheet rows into structured data.
    Returns a list of dicts, each either a category or a feature.
    """
    parsed = []
    for row in raw_rows:
        if is_skip_row(row):
            continue

        if is_category_row(row):
            parsed.append({
                "type": "category",
                "name": row[0].strip(),
            })
        else:
            feature_text = row[0].strip()
            # Separate feature name from notes (notes often start with "Note:")
            name = feature_text
            note = ""
            if "\n" in feature_text:
                parts = feature_text.split("\n", 1)
                name = parts[0].strip()
                note = parts[1].strip()
            elif "Note:" in feature_text:
                idx = feature_text.index("Note:")
                name = feature_text[:idx].strip()
                note = feature_text[idx:].strip()

            parsed.append({
                "type": "feature",
                "name": name,
                "note": note,
                "sdk": {k: safe_get(row, i) for k, i in SDK_COLS.items()},
                "uikit": {k: safe_get(row, i) for k, i in UIKIT_COLS.items()},
            })

    return parsed


# ---------------------------------------------------------------------------
# MDX generation
# ---------------------------------------------------------------------------

def format_availability(value: str) -> str:
    """Convert availability status values to readable text with emoji."""
    v = value.strip().lower()
    if not v:
        return ""
    if v == "available":
        return "Available"
    if v in ("not av", "not av...", "not available"):
        return "Not Available"
    if v == "planned":
        return "Planned"
    return value


def format_platform(value: str) -> str:
    """
    Convert platform cell values for display.
    Blank = available on that platform -> checkmark
    'No' = not available on that platform -> cross
    """
    v = value.strip().lower()
    if not v:
        # Blank means available for that platform
        return "✅"
    if v == "no":
        return "—"
    return value


def generate_table(features: list[dict], product: str) -> str:
    """Generate a markdown table for a list of features under one product (sdk or uikit)."""
    if product == "sdk":
        platform_headers = ["Android", "iOS", "TS", "Flutter"]
    else:
        platform_headers = ["Android", "iOS", "Web", "RN", "Flutter"]

    header_row = "| Feature | Availability | " + " | ".join(platform_headers) + " |"
    separator = "| :--- | :---: | " + " | ".join([":---:"] * len(platform_headers)) + " |"

    lines = [header_row, separator]

    for f in features:
        data = f[product]
        name = f["name"]
        if f.get("note"):
            # Use italic text for notes — no HTML tags (Mintlify doesn't support <small>)
            name += f" *({f['note']})*"

        availability = format_availability(data.get("Availability", ""))
        platforms = [format_platform(data.get(p, "")) for p in platform_headers]

        cells = [name, availability] + platforms
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def to_mdx(parsed: list[dict]) -> str:
    """Convert parsed data into a full Mintlify MDX page."""
    lines = [
        "---",
        'title: "Feature Matrix"',
        'sidebarTitle: "Feature Matrix"',
        'description: "Feature availability and platform support across SDK and UIKit."',
        "---",
        "",
        "# Feature Matrix",
        "",
        "A comprehensive overview of feature availability and platform support across **SDK** and **UIKit**.",
        "Use the tabs within each section to compare coverage between the two.",
        "",
        "<Note>",
        "",
        "**Availability** indicates whether a feature is available, planned, or not yet available.",
        "For individual platforms, ✅ means supported and **—** means not yet supported.",
        "",
        "</Note>",
        "",
    ]

    # Group features by category
    categories = []
    current_category = None
    current_features = []

    for item in parsed:
        if item["type"] == "category":
            if current_category is not None:
                categories.append((current_category, current_features))
            current_category = item["name"]
            current_features = []
        elif item["type"] == "feature":
            current_features.append(item)

    # Don't forget the last category
    if current_category is not None:
        categories.append((current_category, current_features))

    # Generate tabbed content for each category
    for cat_name, features in categories:
        if not features:
            continue

        lines.append(f"## {cat_name}")
        lines.append("")
        lines.append("<Tabs>")
        lines.append('  <Tab title="SDK">')
        lines.append("")
        lines.append(generate_table(features, "sdk"))
        lines.append("")
        lines.append("  </Tab>")
        lines.append('  <Tab title="UIKit">')
        lines.append("")
        lines.append(generate_table(features, "uikit"))
        lines.append("")
        lines.append("  </Tab>")
        lines.append("</Tabs>")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    sheet_id = os.environ["SHEET_ID"]
    sheet_name = os.environ.get("SHEET_NAME", "Sheet1")
    output_path = os.environ.get("OUTPUT_PATH", "feature-matrix.mdx")

    # Use service account if key is available, otherwise public CSV
    if os.environ.get("GOOGLE_SA_KEY"):
        raw_rows = fetch_sheet_service_account(sheet_id, sheet_name)
    else:
        raw_rows = fetch_sheet_public(sheet_id, sheet_name)

    if not raw_rows:
        print("ERROR: No data returned from sheet", file=sys.stderr)
        sys.exit(1)

    parsed = parse_rows(raw_rows)
    feature_count = sum(1 for p in parsed if p["type"] == "feature")
    category_count = sum(1 for p in parsed if p["type"] == "category")

    if feature_count == 0:
        print("ERROR: No features found after parsing", file=sys.stderr)
        sys.exit(1)

    mdx_content = to_mdx(parsed)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(mdx_content)

    print(f"Written {feature_count} features across {category_count} categories to {output_path}")


if __name__ == "__main__":
    main()
