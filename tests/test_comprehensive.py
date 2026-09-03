
import sys
sys.path.insert(0, 'linear-audit')
import json, tempfile, pathlib, os
from unittest.mock import Mock, patch
import fetch_issues, run_audit, remediate, refresh_dashboard, register_webhook
def test_fetch():
    with patch('fetch_issues.requests.post') as m:
        def se(*a, **kw):
            r=Mock(); r.raise_for_status=Mock()
            r.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [{"node": {"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}}}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}
            return r
        m.side_effect=se
        result = fetch_issues.fetch_all_issues(api_key="k", team_id="team1", max_pages=1)
        assert len(result)==1
    from fetch_issues import transform_to_flat
    flat=transform_to_flat({"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}, "priority": 1})
    assert flat.get("identifier")=="LIN-1" or flat.get("id")=="LIN-1"
def test_refresh():
    md, entries, stats = refresh_dashboard.generate_dashboard_content([], now_str="2026-01-01 00:00 UTC")
    assert isinstance(md, str)
    big=[{"id": str(i), "identifier": f"LIN-{i}", "title": f"Issue {i}", "state": {"type": "completed" if i%3==0 else "backlog", "name": "Done" if i%3==0 else "Todo"}, "assignee": None if i%2==0 else {"id": "u1"}, "project": {"id": f"p{i%2}", "name": f"P{i%2}"}, "estimate": i%5, "description": "d" if i%2==0 else "", "parent": None, "priority": 1, "archivedAt": None, "completedAt": None} for i in range(30)]
    md, entries, stats = refresh_dashboard.generate_dashboard_content(big, now_str="2026-01-01 00:00 UTC")
    assert stats["total_issues"]==30
def test_register():
    with patch('register_webhook.gql', return_value={"data": {"webhooks": {"nodes": []}}}):
        assert register_webhook.list_webhooks(api_key="k") == []
    with patch('register_webhook.gql', return_value={"data": {"webhookCreate": {"success": True, "webhook": {"id": "1", "label": "t", "url": "https://example.com", "enabled": True, "resourceTypes": ["Issue"]}}}}), patch('register_webhook.secrets.token_hex', return_value="a"*32):
        r=register_webhook.register_webhook("https://example.com", label="t", api_key="k")
        assert r is not None
def test_remediate():
    c=remediate.LinearClient(api_key="k")
    assert "Authorization" in c.headers
    with patch('remediate.requests.post') as m:
        mr=Mock(); mr.json.return_value={"data": {"issueUpdate": {"success": True}}}; mr.raise_for_status=Mock(); m.return_value=mr
        assert c.update_issue("id", {"title": "t"}) is True
def test_run_audit():
    import tempfile, pathlib, json as js
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"issues.json"
        p.write_text(js.dumps([{"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}, "project": "p1", "estimate": 1}]))
        issues=run_audit.load_issues(p)
        result=run_audit.run_audit(issues)
        assert isinstance(result, dict)
def test_fetch_extra():
    with patch('fetch_issues.requests.post') as m:
        calls=[0]
        def se2(*a, **kw):
            calls[0]+=1
            r=Mock(); r.raise_for_status=Mock()
            if calls[0]==1:
                r.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [{"node": {"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}}}], "pageInfo": {"hasNextPage": True, "endCursor": "c1"}}}}}
            elif calls[0]==2:
                r.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [{"node": {"id": "2", "identifier": "LIN-2", "title": "t2", "state": {"type": "backlog"}}}], "pageInfo": {"hasNextPage": True, "endCursor": "c2"}}}}}
            else:
                r.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [], "pageInfo": {"hasNextPage": False}}}}}
            return r
        m.side_effect=se2
        result = fetch_issues.fetch_all_issues(api_key="k", team_id="team1", max_pages=5)
        assert len(result)>=2
def test_refresh_extra():
    with patch('refresh_dashboard.gql', return_value={"data": {"issues": {"nodes": [{"id": "1", "identifier": "LIN-1", "title": "t", "priority": 1, "estimate": 2, "state": {"id": "s", "name": "Todo", "type": "backlog"}, "parent": None, "completedAt": None}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}):
        assert isinstance(refresh_dashboard.fetch_project_issues(api_key="k", max_pages=None), list)
def test_register_extra():
    with patch('register_webhook.list_webhooks', return_value=[{"id": "1", "label": "Exists", "url": "https://a", "enabled": True, "resourceTypes": []}]):
        with patch('register_webhook.gql', return_value={"data": {"webhookDelete": {"success": True}}}):
            result = register_webhook.unregister_webhook(label="Exists", api_key="k")
            assert isinstance(result, bool)
def test_remediate_extra():
    with patch('remediate.requests.post') as m:
        mr=Mock(); mr.json.return_value={"data": {"issueArchive": {"success": True}}}; mr.raise_for_status=Mock(); m.return_value=mr
        c=remediate.LinearClient(api_key="k")
        assert c.archive_issue("id") is True
def test_run_audit_extra():
    import tempfile, pathlib, json as js
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"issues.json"
        p.write_text(js.dumps([{"id": "1", "identifier": "LIN-1", "title": "Duplicate Title", "state": {"type": "completed", "name": "Done"}, "assignee": None, "project": "p1", "estimate": 2, "description": "", "parent": None, "completedAt": "2026-01-01", "priority": 1},
                               {"id": "2", "identifier": "LIN-2", "title": "Duplicate Title", "state": {"type": "completed", "name": "Done"}, "assignee": {"id": "u1"}, "project": "p1", "estimate": 3, "description": "desc", "parent": None, "completedAt": None, "priority": 2}]))
        issues=run_audit.load_issues(p)
        result=run_audit.run_audit(issues)
        assert isinstance(result, dict)
