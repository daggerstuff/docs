"""Unit tests for the pure functions in the linear-audit scripts."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINEAR_AUDIT = ROOT / "linear-audit"


def _load_module(name: str):
    path = LINEAR_AUDIT / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_audit = _load_module("run_audit")
fetch_issues = _load_module("fetch_issues")


def _issue(**overrides) -> dict:
    base = {
        "id": "PIX-1000",
        "title": "Example issue",
        "description": "Example description",
        "status": "Triage",
        "statusType": "triage",
        "assignee": "Chad",
        "assigneeId": "uuid-1",
        "archivedAt": None,
        "estimate": {"value": 2, "name": "2"},
        "project": "Some Project",
        "projectId": "proj-1",
        "completedAt": None,
        "url": "https://linear.app/pixelated/issue/PIX-1000",
    }
    base.update(overrides)
    return base


# ── normalize_title / title_similarity ────────────────────────────────────────


def test_normalize_title_lowercases_and_strips():
    assert run_audit.normalize_title("  Hello WORLD  ") == "hello world"


def test_title_similarity_identical_is_one():
    assert run_audit.title_similarity("Fix bug", "fix bug") == 1.0


def test_title_similarity_different_is_low():
    assert run_audit.title_similarity("Fix bug", "write docs") < 0.5


# ── detect_duplicates ─────────────────────────────────────────────────────────


def test_detect_duplicates_matches_similar_completed_titles():
    issues = [
        _issue(
            id="PIX-1",
            title="Generate Q4 2025 Corpus Batch (Oct - Dec)",
            statusType="completed",
        ),
        _issue(
            id="PIX-2",
            title="Generate Q3 2025 Corpus Batch (Jul - Sep)",
            statusType="completed",
        ),
    ]
    dupes = run_audit.detect_duplicates(issues)
    assert len(dupes) == 1
    assert dupes[0]["issue_a"]["id"] == "PIX-1"
    assert dupes[0]["issue_b"]["id"] == "PIX-2"
    assert dupes[0]["title_similarity"] >= run_audit.SIMILARITY_THRESHOLD


def test_detect_duplicates_ignores_non_completed():
    issues = [
        _issue(id="PIX-1", title="Generate Q4 Corpus", statusType="completed"),
        _issue(id="PIX-2", title="Generate Q4 Corpus", statusType="triage"),
    ]
    assert run_audit.detect_duplicates(issues) == []


def test_detect_duplicates_ignores_dissimilar_titles():
    issues = [
        _issue(id="PIX-1", title="Fix the login button", statusType="completed"),
        _issue(id="PIX-2", title="Rewrite the billing service", statusType="completed"),
    ]
    assert run_audit.detect_duplicates(issues) == []


# ── find_unassigned ───────────────────────────────────────────────────────────


def test_find_unassigned_flags_missing_assignee():
    issues = [_issue(id="PIX-1", assignee=None, assigneeId=None)]
    result = run_audit.find_unassigned(issues)
    assert len(result) == 1
    assert result[0]["id"] == "PIX-1"


def test_find_unassigned_skips_archived():
    issues = [_issue(id="PIX-1", assignee=None, assigneeId=None, archivedAt="2026-01-01")]
    assert run_audit.find_unassigned(issues) == []


def test_find_unassigned_skips_assigned():
    issues = [_issue(id="PIX-1", assignee="Chad", assigneeId="uuid-1")]
    assert run_audit.find_unassigned(issues) == []


# ── find_missing_descriptions ─────────────────────────────────────────────────


def test_find_missing_descriptions_flags_empty():
    issues = [_issue(id="PIX-1", description="   ")]
    result = run_audit.find_missing_descriptions(issues)
    assert len(result) == 1
    assert result[0]["id"] == "PIX-1"


def test_find_missing_descriptions_skips_populated():
    issues = [_issue(id="PIX-1", description="Has a description")]
    assert run_audit.find_missing_descriptions(issues) == []


def test_find_missing_descriptions_skips_archived():
    issues = [_issue(id="PIX-1", description="", archivedAt="2026-01-01")]
    assert run_audit.find_missing_descriptions(issues) == []


# ── check_estimate_coverage ───────────────────────────────────────────────────


def test_check_estimate_coverage_computes_pct():
    issues = [
        _issue(id="PIX-1", estimate={"value": 2, "name": "2"}),
        _issue(id="PIX-2", estimate=None),
        _issue(id="PIX-3", estimate={"value": 5, "name": "5"}),
    ]
    result = run_audit.check_estimate_coverage(issues)
    assert result["total_active"] == 3
    assert result["with_estimate"] == 2
    assert result["without_estimate"] == 1
    assert result["coverage_pct"] == round(2 / 3 * 100, 1)


def test_check_estimate_coverage_empty_is_zero():
    result = run_audit.check_estimate_coverage([])
    assert result["coverage_pct"] == 0


def test_check_estimate_coverage_ignores_archived():
    issues = [
        _issue(id="PIX-1", estimate=None, archivedAt="2026-01-01"),
        _issue(id="PIX-2", estimate={"value": 1, "name": "1"}),
    ]
    result = run_audit.check_estimate_coverage(issues)
    assert result["total_active"] == 1
    assert result["coverage_pct"] == 100.0


# ── check_archived_completeness ───────────────────────────────────────────────


def test_check_archived_completeness_flags_completed_not_archived():
    issues = [
        _issue(id="PIX-1", statusType="completed", archivedAt=None),
        _issue(id="PIX-2", statusType="completed", archivedAt="2026-01-01"),
    ]
    result = run_audit.check_archived_completeness(issues)
    assert result["total_completed"] == 2
    assert result["archived"] == 1
    assert result["not_archived"] == 1
    assert result["not_archived_list"][0]["id"] == "PIX-1"


# ── review_projects ───────────────────────────────────────────────────────────


def test_review_projects_counts_issues_per_project():
    issues = [
        _issue(id="PIX-1", project="Proj A", projectId="a"),
        _issue(id="PIX-2", project="Proj A", projectId="a", statusType="completed"),
        _issue(id="PIX-3", project="Proj B", projectId="b"),
    ]
    projects, flagged = run_audit.review_projects(issues)
    by_name = {p["name"]: p for p in projects}
    assert by_name["Proj A"]["issue_count"] == 2
    assert by_name["Proj A"]["completed_count"] == 1
    assert by_name["Proj B"]["issue_count"] == 1
    assert flagged == []


def test_review_projects_flags_fully_completed():
    issues = [
        _issue(id="PIX-1", project="Proj A", projectId="a", statusType="completed"),
    ]
    _projects, flagged = run_audit.review_projects(issues)
    assert flagged  # all issues completed -> flagged
    assert flagged[0]["name"] == "Proj A"


# ── fetch_issues.transform_to_flat ────────────────────────────────────────────


def test_transform_to_flat_flattens_nested_state():
    node = {
        "identifier": "PIX-1873",
        "title": "T",
        "description": "D",
        "state": {"id": "s", "name": "Done", "type": "completed"},
        "assignee": {"id": "u1", "name": "Chad", "email": "c@x.com"},
        "creator": {"id": "u2", "name": "Aly"},
        "project": {"id": "p1", "name": "Proj"},
        "cycle": {"id": "c1"},
        "labels": {"nodes": [{"id": "l1", "name": "bug"}]},
        "parent": {"id": "pp", "identifier": "PIX-1"},
        "estimate": 2,
        "priority": 1,
        "url": "https://u",
        "createdAt": "2026-01-01",
    }
    flat = fetch_issues.transform_to_flat(node)
    assert flat["id"] == "PIX-1873"
    assert flat["status"] == "Done"
    assert flat["statusType"] == "completed"
    assert flat["assignee"] == "Chad"
    assert flat["assigneeId"] == "u1"
    assert flat["createdBy"] == "Aly"
    assert flat["project"] == "Proj"
    assert flat["projectId"] == "p1"
    assert flat["cycleId"] == "c1"
    assert flat["labels"] == ["bug"]
    assert flat["parentId"] == "PIX-1"
    assert flat["estimate"] == {"value": 2, "name": "2"}
    assert flat["priority"] == {"value": 1, "name": ""}


def test_transform_to_flat_handles_nulls():
    node = {"identifier": "PIX-1", "title": "T"}
    flat = fetch_issues.transform_to_flat(node)
    assert flat["status"] is None
    assert flat["statusType"] is None
    assert flat["assignee"] is None
    assert flat["estimate"] is None
    assert flat["priority"] is None
    assert flat["labels"] == []
    assert flat["parentId"] is None
