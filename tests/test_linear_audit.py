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
remediate = _load_module("remediate")
refresh_dashboard = _load_module("refresh_dashboard")


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


# ── remediate.py tests ────────────────────────────────────────────────────────


def test_linear_client_auth_header_is_raw_key():
    client = remediate.LinearClient("lin_api_secret_key_123")
    assert client.headers["Authorization"] == "lin_api_secret_key_123"
    assert "Bearer" not in client.headers["Authorization"]
    assert client.headers["Content-Type"] == "application/json"


def _compute_apply(apply_arg: bool, dry_run_arg: bool) -> bool:
    return apply_arg and not dry_run_arg


def test_remediate_apply_flag_logic():
    # dry-run only
    assert _compute_apply(apply_arg=False, dry_run_arg=True) is False

    # apply only
    assert _compute_apply(apply_arg=True, dry_run_arg=False) is True

    # neither (default)
    assert _compute_apply(apply_arg=False, dry_run_arg=False) is False


def test_remediate_dry_run_does_not_call_api():
    missing = [_issue(id="PIX-10", title="Missing Desc", identifier="PIX-10")]
    results = remediate.remediate_descriptions(None, missing, apply=False)
    assert len(results) == 1
    assert results[0]["success"] == "dry_run"
    assert results[0]["identifier"] == "PIX-10"


# ── fetch_issues.py tests ─────────────────────────────────────────────────────


def test_fetch_all_issues_respects_max_pages(monkeypatch):
    calls = []

    def mock_post(url, headers=None, json=None, timeout=None):
        calls.append(json)

        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "data": {
                        "team": {
                            "name": "Engineering",
                            "issues": {
                                "edges": [{"node": {"identifier": f"PIX-{len(calls)}", "title": "T"}}],
                                "pageInfo": {"hasNextPage": True, "endCursor": f"cursor-{len(calls)}"},
                            },
                        }
                    }
                }

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    monkeypatch.setattr("time.sleep", lambda _: None)

    issues = fetch_issues.fetch_all_issues("test-key", "team-1", page_size=10, max_pages=3)
    assert len(issues) == 3
    assert len(calls) == 3


# ── refresh_dashboard.py tests ────────────────────────────────────────────────


def test_refresh_dashboard_progress_bar():
    assert refresh_dashboard.progress_bar(0, 10) == "░░░░░░░░░░ 0%"
    assert refresh_dashboard.progress_bar(5, 10) == "█████░░░░░ 50%"
    assert refresh_dashboard.progress_bar(10, 10) == "██████████ 100%"
    assert refresh_dashboard.progress_bar(0, 0) == "░░░░░░░░░░ 0%"


def test_refresh_dashboard_generate_content():
    sample_issues = [
        {
            "id": "p1",
            "identifier": "PIX-4126",
            "title": "Penetration Testing",
            "state": {"name": "Started", "type": "started"},
        },
        {
            "id": "c1",
            "identifier": "PIX-4126-1",
            "title": "Sub 1",
            "state": {"name": "Done", "type": "completed"},
            "parent": {"id": "p1"},
            "estimate": 3,
        },
        {
            "id": "c2",
            "identifier": "PIX-4126-2",
            "title": "Sub 2",
            "state": {"name": "Started", "type": "started"},
            "parent": {"id": "p1"},
            "estimate": 2,
        },
        {
            "id": "e1",
            "identifier": "PIX-4131",
            "title": "Enterprise Readiness",
            "state": {"name": "In Progress", "type": "started"},
        },
        {
            "id": "a1",
            "identifier": "PIX-4158",
            "title": "Quarterly Audit",
            "state": {"name": "Completed", "type": "completed"},
        },
    ]
    md, ws_entries, stats = refresh_dashboard.generate_dashboard_content(
        all_issues=sample_issues,
        now_str="2026-08-29 16:00 UTC",
    )
    assert "# Enterprise Readiness Program — Dashboard" in md
    assert stats["total_issues"] == 5
    assert stats["total_sub_issues"] == 2
    assert stats["total_done"] == 1
    assert stats["total_done_effort"] == 3
    assert stats["total_effort"] == 5
    assert len(ws_entries) == 1
    assert ws_entries[0]["ident"] == "PIX-4126"


# ── run_audit.load_issues validation tests ────────────────────────────────────


def test_load_issues_accepts_valid_dict_with_issues(tmp_path):
    f = tmp_path / "valid.json"
    f.write_text('{"shape": "linear_mcp_flat_v2", "issues": [{"id": "PIX-1", "title": "T"}]}')
    issues = run_audit.load_issues(f)
    assert len(issues) == 1
    assert issues[0]["id"] == "PIX-1"


def test_load_issues_accepts_valid_bare_list(tmp_path):
    f = tmp_path / "list.json"
    f.write_text('[{"id": "PIX-1", "title": "T"}]')
    issues = run_audit.load_issues(f)
    assert len(issues) == 1
    assert issues[0]["id"] == "PIX-1"


def test_load_issues_rejects_unknown_dict_shape(tmp_path):
    import pytest

    f = tmp_path / "bad_dict.json"
    f.write_text('{"error": "not found", "code": 404}')
    with pytest.raises(ValueError, match="expected object with 'issues' list"):
        run_audit.load_issues(f)


def test_load_issues_rejects_non_list_issues_field(tmp_path):
    import pytest

    f = tmp_path / "bad_field.json"
    f.write_text('{"issues": "not-a-list"}')
    with pytest.raises(ValueError, match="'issues' field must be a list"):
        run_audit.load_issues(f)


def test_load_issues_rejects_non_json_object(tmp_path):
    import pytest

    f = tmp_path / "primitive.json"
    f.write_text('"just a string"')
    with pytest.raises(ValueError, match="expected object or array"):
        run_audit.load_issues(f)


# ── cross-artifact check ──────────────────────────────────────────────────────


def test_committed_artifacts_are_in_sync():
    import json

    issues_path = LINEAR_AUDIT / "issues.json"
    audit_results_path = LINEAR_AUDIT / "audit_results.json"

    assert issues_path.exists(), "issues.json must exist"
    assert audit_results_path.exists(), "audit_results.json must exist"

    issues = run_audit.load_issues(issues_path)
    fresh_results = run_audit.run_audit(issues)
    with open(audit_results_path) as f:
        committed_results = json.load(f)

    assert fresh_results["summary"] == committed_results["summary"]
    assert fresh_results["acceptance_criteria_met"] == committed_results["acceptance_criteria_met"]
    assert len(fresh_results["duplicates"]) == len(committed_results["duplicates"])
    assert len(fresh_results["unassigned"]) == len(committed_results["unassigned"])
