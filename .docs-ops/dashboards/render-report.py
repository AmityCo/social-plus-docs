#!/usr/bin/env python3
"""
Docs-quality report renderer.

Reads the latest snapshot (and previous if available) from
.docs-ops/dashboards/snapshots/ and renders a human-readable markdown
report to .docs-ops/dashboards/latest-report.md.

Usage:
    python3 .docs-ops/dashboards/render-report.py

Run after snapshot.py. Commits latest-report.md alongside the snapshot.
"""
from __future__ import annotations
import json
import pathlib
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
SNAPSHOTS_DIR = SCRIPT_DIR / "snapshots"
REPORT_PATH = SCRIPT_DIR / "latest-report.md"

PLATFORMS = ["typescript", "ios", "android", "flutter"]
PLATFORM_LABELS = {
    "typescript": "TypeScript",
    "ios": "iOS",
    "android": "Android",
    "flutter": "Flutter",
}


def load_snapshots() -> tuple[dict, dict | None]:
    snaps = sorted(SNAPSHOTS_DIR.glob("*.json"))
    if not snaps:
        print("No snapshots found. Run snapshot.py first.", file=sys.stderr)
        sys.exit(1)
    latest = json.loads(snaps[-1].read_text(encoding="utf-8"))
    prev = json.loads(snaps[-2].read_text(encoding="utf-8")) if len(snaps) >= 2 else None
    return latest, prev


def pct(score: float | None) -> str:
    if score is None:
        return "n/a"
    return f"{score * 100:.0f}%"


def delta_str(curr: int | float | None, prev: int | float | None, is_pct: bool = False) -> str:
    if prev is None or curr is None:
        return "—"
    diff = (curr or 0) - (prev or 0)
    if diff == 0:
        return "—"
    sign = "+" if diff > 0 else ""
    if is_pct:
        return f"{sign}{diff * 100:.0f}pp"
    return f"{sign}{diff}"


def trend_table(snaps: list[dict], key_path: list) -> str:
    """Render a simple trend table from up to 8 snapshots."""
    rows = []
    for s in snaps:
        val = s
        try:
            for k in key_path:
                val = val[k]
        except (KeyError, TypeError):
            val = "?"
        rows.append((s["snapshot_date"], val))

    if not rows:
        return "_No trend data._\n"

    header = "| Date | Value |\n|---|---|\n"
    lines = "\n".join(f"| {date} | {v} |" for date, v in rows)
    return header + lines + "\n"


def sparkline(values: list[int | float]) -> str:
    """Render a mini ASCII sparkline from a list of numeric values."""
    blocks = " ▁▂▃▄▅▆▇█"
    if not values:
        return ""
    mn, mx = min(values), max(values)
    span = mx - mn or 1
    return "".join(blocks[min(8, int((v - mn) / span * 8))] for v in values)


def render(latest: dict, prev: dict | None, all_snaps: list[dict]) -> str:
    lines: list[str] = []

    prev_date = prev["snapshot_date"] if prev else None
    comparing = f" · comparing against {prev_date} snapshot" if prev_date else " · first snapshot"
    lines.append(f"# Docs Quality Dashboard\n")
    lines.append(f"_Snapshot: {latest['snapshot_date']}{comparing}_\n")

    # ── Headline ──────────────────────────────────────────────────────────────
    lines.append("## Headline\n")
    s = latest["summary"]
    ps = prev["summary"] if prev else None

    total_drift = s["total_drift_issues"]
    total_fail = s["total_doc_as_test_failures"]
    e_health = s["eastern_health_score"]
    w_health = s["western_health_score"]

    pd_drift = ps["total_drift_issues"] if ps else None
    pd_fail = ps["total_doc_as_test_failures"] if ps else None
    pe_health = ps["eastern_health_score"] if ps else None
    pw_health = ps["western_health_score"] if ps else None

    lines.append("| Metric | This week | Last week | Δ |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Total regex drift | {total_drift} | {pd_drift if pd_drift is not None else '—'} | {delta_str(total_drift, pd_drift)} |")
    lines.append(f"| Total doc-as-test failures | {total_fail} | {pd_fail if pd_fail is not None else '—'} | {delta_str(total_fail, pd_fail)} |")
    lines.append(f"| Eastern cohort health | {pct(e_health)} | {pct(pe_health)} | {delta_str(e_health, pe_health, is_pct=True)} |")
    lines.append(f"| Western cohort health | {pct(w_health)} | {pct(pw_health)} | {delta_str(w_health, pw_health, is_pct=True)} |")
    lines.append("")

    healthy_badge = "✅ All systems healthy" if s["healthy"] else "⚠️  Issues detected — see Alerts below"
    lines.append(f"**Status:** {healthy_badge}\n")

    # ── Per-platform regex drift ───────────────────────────────────────────────
    lines.append("## Per-platform (regex drift)\n")
    lines.append("| Platform | Total | Eastern | Western | Shared | Other |")
    lines.append("|---|---|---|---|---|---|")
    for p in PLATFORMS:
        dr = latest["regex_drift"].get(p, {})
        bc = dr.get("by_cohort", {})
        lines.append(
            f"| {PLATFORM_LABELS[p]} | {dr.get('total', 0)} "
            f"| {bc.get('eastern', 0)} | {bc.get('western', 0)} "
            f"| {bc.get('shared', 0)} | {bc.get('other', 0)} |"
        )
    lines.append("")

    # ── Per-platform doc-as-test ───────────────────────────────────────────────
    lines.append("## Per-platform (doc-as-test type-checking)\n")
    lines.append("| Platform | Pass | Skip | Fail | Warn | Eastern blocks | Western blocks | Shared blocks |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for p in PLATFORMS:
        dat = latest["doc_as_test"].get(p, {})
        bc = dat.get("by_cohort", {})
        e = bc.get("eastern", {})
        w = bc.get("western", {})
        sh = bc.get("shared", {})
        e_total = e.get("passed", 0) + e.get("failed", 0) + e.get("skipped", 0)
        w_total = w.get("passed", 0) + w.get("failed", 0) + w.get("skipped", 0)
        sh_total = sh.get("passed", 0) + sh.get("failed", 0) + sh.get("skipped", 0)
        lines.append(
            f"| {PLATFORM_LABELS[p]} "
            f"| {dat.get('passed', 0)} | {dat.get('skipped', 0)} "
            f"| {dat.get('failed', 0)} | {dat.get('warnings', 0)} "
            f"| {e_total} | {w_total} | {sh_total} |"
        )
    lines.append("")

    # ── Trend (last 8 snapshots) ───────────────────────────────────────────────
    lines.append("## Trend (last 8 snapshots)\n")
    recent = all_snaps[-8:]
    if len(recent) < 2:
        lines.append("_Not enough snapshots yet for trend analysis. Re-run weekly to build history._\n")
    else:
        drift_vals = [s["summary"]["total_drift_issues"] for s in recent]
        fail_vals = [s["summary"]["total_doc_as_test_failures"] for s in recent]
        e_vals = [s["summary"]["eastern_health_score"] or 1.0 for s in recent]
        w_vals = [s["summary"]["western_health_score"] or 1.0 for s in recent]

        lines.append("| Date | Drift | Failures | Eastern health | Western health |")
        lines.append("|---|---|---|---|---|")
        for s in recent:
            sm = s["summary"]
            lines.append(
                f"| {s['snapshot_date']} "
                f"| {sm['total_drift_issues']} "
                f"| {sm['total_doc_as_test_failures']} "
                f"| {pct(sm['eastern_health_score'])} "
                f"| {pct(sm['western_health_score'])} |"
            )
        lines.append("")
        lines.append(f"Drift trend:          `{sparkline(drift_vals)}` (left=oldest)")
        lines.append(f"Failure trend:        `{sparkline(fail_vals)}`")
        lines.append(f"Eastern health trend: `{sparkline(e_vals)}`")
        lines.append(f"Western health trend: `{sparkline(w_vals)}`")
    lines.append("")

    # ── Alerts ────────────────────────────────────────────────────────────────
    lines.append("## Alerts\n")
    alerts: list[str] = []

    if s["total_drift_issues"] > 0:
        alerts.append(f"⚠️  **{s['total_drift_issues']} regex drift issue(s)** detected across all platforms.")

    if s["total_doc_as_test_failures"] > 0:
        alerts.append(f"⚠️  **{s['total_doc_as_test_failures']} doc-as-test failure(s)** — code blocks do not compile.")

    # Regressions vs previous
    if prev:
        drift_delta = s["total_drift_issues"] - ps["total_drift_issues"]
        if drift_delta > 0:
            alerts.append(f"📈 Drift increased by **{drift_delta}** since last snapshot.")
        fail_delta = s["total_doc_as_test_failures"] - ps["total_doc_as_test_failures"]
        if fail_delta > 0:
            alerts.append(f"📈 Doc-as-test failures increased by **{fail_delta}** since last snapshot.")

    if not alerts:
        lines.append("_No alerts. All checks passing._\n")
    else:
        for alert in alerts:
            lines.append(f"- {alert}")
        lines.append("")

    # ── Footer ────────────────────────────────────────────────────────────────
    lines.append("---")
    lines.append(f"_Generated by `.docs-ops/dashboards/render-report.py` · snapshot: `{latest['snapshot_run_at']}`_")

    return "\n".join(lines) + "\n"


def main() -> int:
    latest, prev = load_snapshots()
    all_snaps = [json.loads(p.read_text()) for p in sorted(SNAPSHOTS_DIR.glob("*.json"))]

    report = render(latest, prev, all_snaps)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Report written → {REPORT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
