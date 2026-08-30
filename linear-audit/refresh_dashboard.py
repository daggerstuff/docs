#!/usr/bin/env python3
"""
refresh_dashboard.py — Live dashboard generator for Enterprise Readiness Program.

Fetches all issues from the Linear project, computes completion stats per
workstream, and regenerates docs/linear-audit/dashboard.md with live data.

Usage:
    export LINEAR_API_KEY=lin_api_...
    python3 refresh_dashboard.py
"""

import argparse
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import requests

# ── Defaults & Constants ──────────────────────────────────────────────────────

DEFAULT_API_URL = "https://api.linear.app/graphql"
DEFAULT_PROJECT_ID = "29c133a2-9195-42d3-b53e-31154d47ea7d"
DEFAULT_CUSTOM_VIEW_URL = "https://linear.app/pixelated/view/cb20ccc27a23"
DEFAULT_DASHBOARD_PATH = Path(__file__).resolve().parent / "dashboard.md"
DEFAULT_EPIC_ID = "PIX-4131"
DEFAULT_AUDIT_TRACKER_ID = "PIX-4158"

# Workstream definitions keyed by parent issue identifier.
# Each entry: (short_name, priority, icon, priority_emoji)
DEFAULT_WORKSTREAMS = {
    "PIX-4126": ("Penetration Testing", 1, "\U0001f512", "\U0001f534"),  # Urgent
    "PIX-4125": ("Disaster Recovery", 2, "\U0001f504", "\U0001f7e1"),  # High
    "PIX-4127": ("SLA/SLO Definitions", 2, "\U0001f4ca", "\U0001f7e1"),  # High
    "PIX-4129": ("Vendor Risk Assessment", 2, "\U0001f4cb", "\U0001f7e1"),  # High
    "PIX-4130": ("SOC2/HIPAA Readiness", 2, "\u2705", "\U0001f7e1"),  # High
    "PIX-4128": ("Chaos Engineering", 3, "\U0001f9ea", "\U0001f7e2"),  # Medium
}

# Module-level aliases for backwards compatibility
API_URL = DEFAULT_API_URL
PROJECT_ID = DEFAULT_PROJECT_ID
CUSTOM_VIEW_URL = DEFAULT_CUSTOM_VIEW_URL
DASHBOARD_PATH = str(DEFAULT_DASHBOARD_PATH)
WORKSTREAMS = DEFAULT_WORKSTREAMS

PRIORITY_LABELS = {1: "Urgent", 2: "High", 3: "Medium"}

# State types considered "complete/done"
DONE_STATE_TYPES = {"completed"}

# State types considered "in progress"
IN_PROGRESS_STATE_TYPES = {"started", "review"}


# ── API helpers ───────────────────────────────────────────────────────────────


def gql(query: str, api_key: str | None = None, api_url: str = DEFAULT_API_URL) -> dict | None:
    """Execute a GraphQL query against the Linear API with retry."""
    if not api_url.startswith(("https://", "http://")):
        raise ValueError("Invalid URL scheme: only https/http supported")
    key = api_key or os.environ.get("LINEAR_API_KEY", "")
    for attempt in range(3):
        try:
            resp = requests.post(
                api_url,
                json={"query": query},
                headers={"Content-Type": "application/json", "Authorization": key},
                timeout=30,
            )
            result = resp.json()
            if "errors" in result:
                print(f"  API error: {result['errors']}", file=sys.stderr)
                return None
            return result
        except Exception as e:
            if attempt < 2:
                print(f"  Retry {attempt + 1} after: {e}", file=sys.stderr)
            else:
                print(f"  Failed after 3 retries: {e}", file=sys.stderr)
                return None


def fetch_project_issues(
    project_id: str = DEFAULT_PROJECT_ID,
    api_key: str | None = None,
    api_url: str = DEFAULT_API_URL,
    max_pages: int | None = 100,
) -> list[dict]:
    """Fetch all issues in the Linear project."""
    all_issues = []
    cursor = None
    page = 0

    while True:
        page += 1
        if max_pages is not None and page > max_pages:
            print(f"Reached maximum page limit ({max_pages}), stopping.", file=sys.stderr)
            break

        after = f', after: "{cursor}"' if cursor else ""
        query = f"""{{
            issues(first: 50{after}, filter: {{
                project: {{ id: {{ eq: "{project_id}" }} }}
            }}) {{
                nodes {{
                    id identifier title priority estimate
                    state {{ id name type }}
                    parent {{ id identifier title }}
                    completedAt
                }}
                pageInfo {{ hasNextPage endCursor }}
            }}
        }}"""
        result = gql(query, api_key=api_key, api_url=api_url)
        if not result or "data" not in result:
            print(f"  Error on page {page}", file=sys.stderr)
            break

        nodes = result["data"]["issues"]["nodes"]
        page_info = result["data"]["issues"]["pageInfo"]
        all_issues.extend(nodes)

        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    return all_issues


# ── Markdown generation ───────────────────────────────────────────────────────


def progress_bar(completed: int, total: int, width: int = 10) -> str:
    """Generate a Unicode progress bar like ████░░░░░░."""
    if total == 0:
        return "\u2591" * width + " 0%"
    filled = round(completed / total * width)
    pct = round(completed / total * 100)
    bar = "\u2588" * filled + "\u2591" * (width - filled)
    return f"{bar} {pct}%"


def render_workstream_table(ws_entries: list) -> str:
    """Render the overview progress table."""
    rows = []
    for ws in ws_entries:
        rows.append(
            f"| {ws['priority_emoji']} {ws['priority_label']} "
            f"| {ws['icon']} {ws['name']} "
            f"| {ws['progress_bar']} "
            f"| {ws['done_count']}/{ws['total']} "
            f"| {ws['done_effort']}/{ws['total_effort']} pts |"
        )
    return "\n".join(rows)


def render_detail_section(ws: dict, sub_issues: list) -> str:
    """Render the detailed sub-issue table for one workstream."""
    # Summary line
    in_prog = ws["in_progress_count"]
    triage = ws["triage_count"]
    other = ws["total"] - ws["done_count"] - in_prog - triage
    parts = [f"**Sub-issues:** {ws['total']}"]
    if ws["done_count"]:
        parts.append(f"**Done:** {ws['done_count']}")
    if in_prog:
        parts.append(f"**In Progress:** {in_prog}")
    if triage:
        parts.append(f"**Triage:** {triage}")
    if other:
        parts.append(f"**Other:** {other}")
    summary = " | ".join(parts)

    lines = [
        f"### {ws['icon']} {ws['name']}",
        "",
        f"{summary}  ",
        f"**Est. Effort:** {ws['done_effort']}/{ws['total_effort']} pts completed",
        "",
        "| Issue | Title | Status | Priority | Estimate |",
        "|-------|-------|--------|----------|----------|",
    ]

    for si in sorted(sub_issues, key=lambda x: x.get("identifier") or x.get("id") or ""):
        ident = si.get("identifier") or si.get("id") or ""
        title = si.get("title") or ""
        state = si.get("state")
        if isinstance(state, dict):
            state_type = state.get("type", "triage")
            state_name = state.get("name", "?")
        else:
            state_type = si.get("statusType", "triage")
            state_name = si.get("status", "?")

        priority_raw = si.get("priority")
        priority = priority_raw.get("value", 0) if isinstance(priority_raw, dict) else (priority_raw or 0)
        estimate_raw = si.get("estimate")
        estimate = estimate_raw.get("value", 0) if isinstance(estimate_raw, dict) else (estimate_raw or 0)

        # Status emoji
        if state_type in DONE_STATE_TYPES:
            status_emoji = "\u2705"
        elif state_type in IN_PROGRESS_STATE_TYPES:
            status_emoji = "\U0001f3c3"
        elif state_type == "canceled":
            status_emoji = "\u274c"
        else:
            status_emoji = "\u23f3"

        # Priority emoji
        pri_emoji = {1: "\U0001f534", 2: "\U0001f7e1", 3: "\U0001f7e2", 0: "\u26ab"}.get(priority, "\u26ab")

        # Truncate title to fit table
        title_display = title[:65]

        lines.append(f"| {ident} | {title_display} | {status_emoji} {state_name} | {pri_emoji} | {estimate} |")

    return "\n".join(lines)


def generate_dashboard_content(
    all_issues: list[dict],
    workstreams: dict | None = None,
    workstream_order: list[str] | None = None,
    project_name: str = "Enterprise Readiness Program",
    custom_view_url: str = DEFAULT_CUSTOM_VIEW_URL,
    epic_id: str = DEFAULT_EPIC_ID,
    audit_tracker_id: str = DEFAULT_AUDIT_TRACKER_ID,
    now_str: str | None = None,
) -> tuple[str, list[dict], dict]:
    """Pure helper to generate dashboard markdown and workstream stats from issue list."""
    ws_dict = workstreams or DEFAULT_WORKSTREAMS
    ws_order = workstream_order or list(ws_dict.keys())

    # Build parent → sub-issue map
    sub_issues_by_parent: dict[str, list[dict]] = {}
    parent_map: dict[str, dict] = {}

    for issue in all_issues:
        ident = issue.get("identifier") or issue.get("id")
        parent = issue.get("parent")
        pid = None
        if isinstance(parent, dict):
            pid = parent.get("identifier") or parent.get("id")
        elif isinstance(parent, str):
            pid = parent
        elif issue.get("parentId"):
            pid = issue.get("parentId")

        if pid:
            if pid not in sub_issues_by_parent:
                sub_issues_by_parent[pid] = []
            sub_issues_by_parent[pid].append(issue)
        elif ident:
            parent_map[ident] = issue
            if issue.get("id") and issue["id"] != ident:
                parent_map[issue["id"]] = issue

    ws_entries = []
    all_detail_sections = []

    total_done = 0
    total_sub_issues = 0
    total_done_effort = 0
    total_effort = 0

    def _get_state_type(k: dict) -> str:
        st = k.get("state")
        if isinstance(st, dict):
            return st.get("type", "triage")
        return k.get("statusType", "triage")

    def _get_estimate(k: dict) -> int | float:
        est = k.get("estimate")
        if isinstance(est, dict):
            return est.get("value", 0) or 0
        return est or 0

    for ws_ident in ws_order:
        if ws_ident not in ws_dict:
            continue

        name, priority, icon, pri_emoji = ws_dict[ws_ident]
        parent = parent_map.get(ws_ident)
        if not parent:
            continue

        p_key = parent.get("id") or ws_ident
        kids = sub_issues_by_parent.get(p_key, [])
        if not kids and ws_ident in sub_issues_by_parent:
            kids = sub_issues_by_parent[ws_ident]

        done_count = sum(1 for k in kids if _get_state_type(k) in DONE_STATE_TYPES)
        in_progress_count = sum(1 for k in kids if _get_state_type(k) in IN_PROGRESS_STATE_TYPES)
        triage_count = sum(1 for k in kids if _get_state_type(k) == "triage")
        total = len(kids)

        done_effort = sum(_get_estimate(k) for k in kids if _get_state_type(k) in DONE_STATE_TYPES)
        total_effort_ws = sum(_get_estimate(k) for k in kids)

        total_done += done_count
        total_sub_issues += total
        total_done_effort += done_effort
        total_effort += total_effort_ws

        ws_entry = {
            "ident": ws_ident,
            "name": name,
            "priority": priority,
            "priority_label": PRIORITY_LABELS.get(priority, "Unknown"),
            "priority_emoji": pri_emoji,
            "icon": icon,
            "total": total,
            "done_count": done_count,
            "in_progress_count": in_progress_count,
            "triage_count": triage_count,
            "done_effort": done_effort,
            "total_effort": total_effort_ws,
            "progress_bar": progress_bar(done_count, total),
        }
        ws_entries.append(ws_entry)

        detail = render_detail_section(ws_entry, kids)
        all_detail_sections.append(detail)

    epic = parent_map.get(epic_id)
    epic_status = (epic.get("state") or {}).get("name", "Triage") if epic else "?"

    audit_issue = [i for i in all_issues if i.get("identifier") == audit_tracker_id]
    audit_status = (audit_issue[0].get("state") or {}).get("name", "Triage") if audit_issue else "?"

    now = now_str or datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    if total_done == 0 and sum(ws["in_progress_count"] for ws in ws_entries) == 0:
        banner = (
            "> **\U0001f504 All sub-issues are in Triage \u2014 execution has not yet begun.**\n"
            "> The 0% completion across all workstreams is accurate for this starting state. "
            "Work begins with PIX-4126 (Penetration Testing \u2014 Urgent priority) as the first priority sprint.\n"
        )
    else:
        banner = ""

    overview_table = render_workstream_table(ws_entries)
    detail_sections = "\n\n".join(all_detail_sections)

    dashboard = f"""# {project_name} \u2014 Dashboard

**Generated:** {now}
**Project:** {project_name}
**Linear View:** [\U0001f517 Workstream Dashboard]({custom_view_url})

{banner}---

## Overview

| Metric | Value |
|--------|-------|
| Total Issues | {len(all_issues)} |
| Workstreams | {len(ws_entries)} |
| Completed Sub-Issues | {total_done}/{total_sub_issues} |
| Total Estimated Effort | {total_effort} pts (completed: {total_done_effort} pts) |

---

## Workstream Progress

| Priority | Workstream | Progress | Completed | Est. Effort |
|----------|------------|----------|-----------|-------------|
{overview_table}

---

## Workstream Details

{detail_sections}

---

## EPIC: Enterprise Readiness

**EPIC: Enterprise Readiness \u2014 Close All Enterprise Gaps** \u2014 Status: {epic_status}

Tracks the overall closure of all 6 enterprise gaps.

---

## Quarterly Audit Tracker

**Quarterly Workspace Audit \u2014 Linear Hygiene Check** \u2014 Status: {audit_status}

Next scheduled audit: **2026-10-29**

---

## Navigation

- **Linear Project:** {project_name} (`PIX` team)
- **Linear Custom View:** [\U0001f517 Workstream Dashboard]({custom_view_url})
- **Initiative:** [Enterprise Readiness](https://linear.app/pixelated/initiative/enterprise-readiness)
- **Initial Audit Report:** [./linear_audit.md](./linear_audit.md)
- **Final Snapshot:** [./linear_audit_final.md](./linear_audit_final.md)
- **Scripts:** `./fetch_issues.py`, `./run_audit.py`, `./remediate.py`, `./refresh_dashboard.py`

---

*Dashboard auto-generated by `refresh_dashboard.py`. Refresh by re-running:*
*`python3 docs/linear-audit/refresh_dashboard.py`*
"""

    summary_stats = {
        "total_issues": len(all_issues),
        "total_done": total_done,
        "total_sub_issues": total_sub_issues,
        "total_done_effort": total_done_effort,
        "total_effort": total_effort,
    }

    return dashboard, ws_entries, summary_stats


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Generate live dashboard for Linear project")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("LINEAR_API_KEY", ""),
        help="Linear API key (or set LINEAR_API_KEY)",
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("LINEAR_PROJECT_ID", DEFAULT_PROJECT_ID),
        help="Linear project ID (or set LINEAR_PROJECT_ID)",
    )
    parser.add_argument(
        "--api-url",
        default=os.environ.get("LINEAR_API_URL", DEFAULT_API_URL),
        help="Linear GraphQL API URL",
    )
    parser.add_argument(
        "--custom-view-url",
        default=os.environ.get("LINEAR_CUSTOM_VIEW_URL", DEFAULT_CUSTOM_VIEW_URL),
        help="Linear Custom View URL",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_DASHBOARD_PATH),
        help="Output dashboard markdown path",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Max pages to fetch from Linear (default: 100)",
    )
    args = parser.parse_args()

    if not args.api_key:
        print("ERROR: LINEAR_API_KEY environment variable or --api-key must be set.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60, file=sys.stderr)
    print("REFRESH DASHBOARD: Enterprise Readiness Program", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    # 1. Fetch data
    print(f"Fetching issues for project {args.project_id}...", file=sys.stderr)
    all_issues = fetch_project_issues(
        project_id=args.project_id,
        api_key=args.api_key,
        api_url=args.api_url,
        max_pages=args.max_pages,
    )
    print(f"  {len(all_issues)} issues found", file=sys.stderr)

    if not all_issues:
        print("ERROR: No issues found in project!", file=sys.stderr)
        sys.exit(1)

    # 2. Generate dashboard markdown
    dashboard, ws_entries, stats = generate_dashboard_content(
        all_issues=all_issues,
        workstreams=DEFAULT_WORKSTREAMS,
        custom_view_url=args.custom_view_url,
    )

    # 3. Write to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(dashboard)

    print(f"\n\U0001f4be Dashboard written to {output_path}", file=sys.stderr)
    completed_line = (
        f"   {stats['total_done']}/{stats['total_sub_issues']} sub-issues completed "
        f"({stats['total_done_effort']}/{stats['total_effort']} pts)"
    )
    print(completed_line, file=sys.stderr)

    # Summary
    print("\n=== WORKSTREAM SUMMARY ===", file=sys.stderr)
    for ws in ws_entries:
        bar = ws["progress_bar"]
        summary_line = (
            f"  {ws['icon']} {ws['name']:25s} {bar:15s}  "
            f"{ws['done_count']:2d}/{ws['total']:2d}  "
            f"({ws['done_effort']}/{ws['total_effort']} pts)"
        )
        print(summary_line, file=sys.stderr)


if __name__ == "__main__":
    main()
