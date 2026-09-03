
import sys
sys.path.insert(0, 'linear-audit')
from unittest.mock import Mock, patch
import fetch_issues, run_audit, remediate, refresh_dashboard, register_webhook
def test_fetch():
    with patch('fetch_issues.requests.post') as m:
        def se(*a, **kw):
            r=Mock(); r.raise_for_status=Mock()
            r.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [{"node": {"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}}}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}
            return r
        m.side_effect=se
        assert len(fetch_issues.fetch_all_issues(api_key="k", team_id="team1", max_pages=1))==1
def test_refresh():
    md, _, stats = refresh_dashboard.generate_dashboard_content([], now_str="2026-01-01 00:00 UTC")
    assert isinstance(md, str)
def test_register():
    with patch('register_webhook.gql', return_value={"data": {"webhooks": {"nodes": []}}}):
        assert register_webhook.list_webhooks(api_key="k")==[]
def test_remediate():
    c=remediate.LinearClient(api_key="k")
    assert "Authorization" in c.headers
def test_run_audit():
    import tempfile, pathlib, json as js
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"x.json"
        p.write_text(js.dumps([{"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}, "project": "p1", "estimate": 1}]))
        assert len(run_audit.load_issues(p))==1
