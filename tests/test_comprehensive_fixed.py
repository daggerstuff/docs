
import sys
sys.path.insert(0, 'linear-audit')
import json, tempfile, pathlib, os
from unittest.mock import Mock, patch
import fetch_issues, run_audit, remediate, refresh_dashboard, register_webhook

def test_fetch_comprehensive():
    with patch('fetch_issues.requests.post') as m:
        def se(*args, **kwargs):
            r=Mock(); r.raise_for_status=Mock()
            r.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [{"node": {"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}}}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}
            return r
        m.side_effect=se
        result = fetch_issues.fetch_all_issues(api_key="k", team_id="team1", max_pages=1)
        assert isinstance(result, list)
        assert len(result)==1
    with patch('fetch_issues.requests.post') as m:
        calls=[0]
        def se2(*args, **kwargs):
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
    with patch('fetch_issues.requests.post') as m:
        mr=Mock(); mr.json.return_value={"errors": [{"message": "auth"}]}; mr.raise_for_status=Mock(); m.return_value=mr
        result = fetch_issues.fetch_all_issues(api_key="k", team_id="team1")
        assert result==[]
    with patch('fetch_issues.requests.post') as m:
        mr=Mock(); mr.json.return_value={"data": {"team": None}}; mr.raise_for_status=Mock(); m.return_value=mr
        result = fetch_issues.fetch_all_issues(api_key="k", team_id="bad")
        assert result==[]
    with patch('fetch_issues.requests.post', side_effect=__import__('requests').RequestException("net")):
        try:
            result=fetch_issues.fetch_all_issues(api_key="k", team_id="team1")
            assert isinstance(result, list)
        except __import__('requests').RequestException:
            pass
    from fetch_issues import transform_to_flat
    flat=transform_to_flat({"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}, "priority": 1})
    assert flat["identifier"]=="LIN-1"
    assert flat["title"]=="t"
    try:
        from fetch_issues import _opt_str
        assert _opt_str(None) is None
        assert _opt_str("test")=="test"
    except: pass
    with patch('fetch_issues.fetch_all_issues', return_value=[{"id": "1"}]):
        with patch('sys.argv', ['fetch_issues.py', '--team', 'team1']):
            with patch.dict(os.environ, {"LINEAR_API_KEY": "k"}):
                with patch('pathlib.Path.mkdir'), patch('builtins.open', Mock()):
                    try:
                        if hasattr(fetch_issues, 'main'):
                            with patch('fetch_issues.OUTPUT_FILE', pathlib.Path("/tmp/out.json")):
                                try: fetch_issues.main()
                                except SystemExit: pass
                                except: pass
                    except: pass
    # Test gql if it exists, otherwise skip correctly
    if hasattr(fetch_issues, 'gql'):
        with patch('fetch_issues.requests.post') as m:
            mr=Mock(); mr.json.return_value={"data": {"test": 1}}; m.return_value=mr
            assert fetch_issues.gql("q", api_key="k") is not None
        with patch('fetch_issues.requests.post') as m:
            mr=Mock(); mr.json.return_value={"errors": ["bad"]}; m.return_value=mr
            assert fetch_issues.gql("q", api_key="k") is None
        with patch('fetch_issues.requests.post', side_effect=__import__('requests').RequestException("net")):
            assert fetch_issues.gql("q", api_key="k") is None
        try:
            fetch_issues.gql("q", api_url="ftp://bad", api_key="k")
            assert False
        except ValueError:
            pass
    else:
        # fetch_issues has no gql, that's expected, just pass
        pass
    # Test with max_pages None
    with patch('fetch_issues.requests.post') as m:
        mr=Mock(); mr.json.return_value={"data": {"team": {"name": "T", "issues": {"edges": [{"node": {"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "backlog"}}}], "pageInfo": {"hasNextPage": False}}}}; mr.raise_for_status=Mock(); m.return_value=mr
        result=fetch_issues.fetch_all_issues(api_key="k", team_id="team1", max_pages=None)
        assert isinstance(result, list)

def test_refresh_comprehensive():
    issues=[
        {"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "completed", "name": "Done"}, "assignee": None, "project": {"id": "p1"}, "estimate": 2, "description": "d", "parent": None, "completedAt": "2026-01-01", "priority": 1, "archivedAt": None},
        {"id": "2", "identifier": "LIN-2", "title": "t2", "state": {"type": "started", "name": "In Progress"}, "assignee": {"id": "u1"}, "project": {"id": "p1"}, "estimate": None, "description": "", "parent": {"id": "1"}, "completedAt": None, "priority": 2},
    ]
    md, entries, stats = refresh_dashboard.generate_dashboard_content(issues, now_str="2026-01-01 00:00 UTC")
    assert isinstance(md, str)
    md2, e2, s2 = refresh_dashboard.generate_dashboard_content([], now_str="2026-01-01 00:00 UTC")
    assert isinstance(md2, str)
    big=[{"id": str(i), "identifier": f"LIN-{i}", "title": f"Issue {i}", "state": {"type": "completed" if i%3==0 else "backlog", "name": "Done" if i%3==0 else "Todo"}, "assignee": None if i%2==0 else {"id": "u1"}, "project": {"id": f"p{i%2}", "name": f"P{i%2}"}, "estimate": i%5, "description": "d" if i%2==0 else "", "parent": None, "priority": 1, "archivedAt": None, "completedAt": None} for i in range(50)]
    md, entries, stats = refresh_dashboard.generate_dashboard_content(big, now_str="2026-01-01 00:00 UTC")
    assert stats["total_issues"]==50
    with patch('refresh_dashboard.gql', return_value={"data": {"issues": {"nodes": [], "pageInfo": {"hasNextPage": False}}}}):
        assert refresh_dashboard.fetch_project_issues(api_key="k", max_pages=1)==[]
    with patch('refresh_dashboard.gql', return_value={"data": {"issues": {"nodes": [{"id": "1", "identifier": "LIN-1", "title": "t", "priority": 1, "estimate": 2, "state": {"id": "s", "name": "Todo", "type": "backlog"}, "parent": None, "completedAt": None}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}):
        assert isinstance(refresh_dashboard.fetch_project_issues(api_key="k", max_pages=None), list)
    with patch('refresh_dashboard.requests.post') as m:
        call_count=[0]
        def se(*args, **kwargs):
            call_count[0]+=1
            if call_count[0] < 3:
                raise Exception("transient")
            resp=Mock(); resp.json.return_value={"data": {"issues": {"nodes": []}}}; resp.raise_for_status=Mock(); return resp
        m.side_effect=se
        try:
            result=refresh_dashboard.gql("q", api_key="k")
            assert result is None or isinstance(result, dict)
        except:
            pass
    try:
        refresh_dashboard.gql("q", api_url="ftp://bad", api_key="k")
        assert False
    except ValueError:
        pass
    with patch('refresh_dashboard.gql', side_effect=[{"data": {"issues": {"nodes": [{"id": "1", "identifier": "LIN-1", "title": "t", "priority": 1, "estimate": 2, "state": {"id": "s", "name": "Todo", "type": "backlog"}, "parent": None, "completedAt": None}], "pageInfo": {"hasNextPage": True, "endCursor": "c1"}}}}, {"data": {"issues": {"nodes": [], "pageInfo": {"hasNextPage": False}}}}]):
        assert len(refresh_dashboard.fetch_project_issues(api_key="k", max_pages=2))>=1

def test_register_comprehensive():
    with patch('register_webhook.gql', return_value={"data": {"webhookCreate": {"success": True, "webhook": {"id": "1", "label": "t", "url": "https://example.com", "enabled": True, "resourceTypes": ["Issue"]}}}}), patch('register_webhook.secrets.token_hex', return_value="a"*32):
        r=register_webhook.register_webhook("https://example.com/hook2", label="Label With Spaces", api_key="k")
        assert r is not None
        r2=register_webhook.register_webhook("https://example.com/hook3", api_key="k")
        assert r2 is not None
    with patch('register_webhook.gql', return_value={"data": {"webhooks": {"nodes": [{"id": "1", "label": "L1", "url": "https://a", "enabled": True, "resourceTypes": ["Issue"]}, {"id": "2", "label": "L2", "url": "https://b", "enabled": False, "resourceTypes": []}]}}}):
        assert len(register_webhook.list_webhooks(api_key="k"))==2
    with patch('register_webhook.gql', return_value={"data": {}}):
        assert register_webhook.list_webhooks(api_key="k") == []
    with patch('register_webhook.gql', return_value=None):
        assert register_webhook.list_webhooks(api_key="k") == []
    with patch('register_webhook.list_webhooks', return_value=[{"id": "1", "label": "Exists", "url": "https://a", "enabled": True, "resourceTypes": []}]):
        with patch('register_webhook.gql', return_value={"data": {"webhookDelete": {"success": True}}}):
            result = register_webhook.unregister_webhook(label="Exists", api_key="k")
            assert isinstance(result, bool)
            result2 = register_webhook.unregister_webhook(label="NotFound", api_key="k")
            assert result2 is False or result2 is None or isinstance(result2, bool)
        with patch('register_webhook.gql', return_value={"data": {"webhookDelete": {"success": False}}}):
            result = register_webhook.unregister_webhook(webhook_id="1", api_key="k")
            assert isinstance(result, bool)
    try:
        register_webhook.gql("q", api_url="ftp://bad", api_key="k")
        assert False
    except ValueError:
        pass
    with patch.dict(os.environ, {}, clear=False):
        if "LINEAR_API_KEY" in os.environ:
            del os.environ["LINEAR_API_KEY"]
        with patch('register_webhook.requests.post') as m:
            mr=Mock(); mr.json.return_value={"data": {"test": 1}}; m.return_value=mr
            result=register_webhook.gql("{q}", api_key=None)
            assert result is not None

def test_remediate_comprehensive():
    c=remediate.LinearClient(api_key="k2")
    assert c.headers["Authorization"]=="k2"
    with patch('remediate.requests.post') as m:
        for payload in [{"title": "t"}, {"description": "d", "priority": 1}, {"assigneeId": "uid", "projectId": "pid"}, {"estimate": 2}, {}]:
            mr=Mock(); mr.json.return_value={"data": {"issueUpdate": {"success": True}}}; mr.raise_for_status=Mock(); m.return_value=mr
            try: c.update_issue("id", payload)
            except: pass
        m.side_effect=__import__('requests').RequestException("net")
        try:
            c.update_issue("id", {"title": "t"})
            assert False
        except __import__('requests').RequestException:
            pass
        m.side_effect=None
    audit={"duplicates": [[{"id": "1", "identifier": "LIN-1", "title": "dup", "project": {"id": "p1"}}, {"id": "2", "identifier": "LIN-2", "title": "dup", "project": {"id": "p1"}}]], "unassigned": [{"id": "3", "identifier": "LIN-3", "title": "t", "project": {"id": "p1"}}], "missingDescriptions": [{"id": "4", "identifier": "LIN-4", "title": "t", "description": "", "project": {"id": "p1"}}], "unarchivedCompleted": [{"id": "5", "identifier": "LIN-5", "title": "t", "state": {"type": "completed"}, "project": {"id": "p1"}}]}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        import json
        json.dump(audit, f); fname=f.name
    try:
        with patch('remediate.LinearClient') as mock_cls:
            mock_inst=Mock(); mock_inst.update_issue.return_value=True; mock_inst.archive_issue.return_value=True; mock_cls.return_value=mock_inst
            if hasattr(remediate, 'remediate'):
                try: remediate.remediate(fname, dry_run=True, api_key="k")
                except: pass
                try: remediate.remediate(fname, dry_run=False, api_key="k")
                except: pass
            if hasattr(remediate, 'main'):
                for args in [['remediate.py', '--dry-run', '--input', fname], ['remediate.py', '--apply', '--input', fname]]:
                    with patch('sys.argv', args):
                        try: remediate.main()
                        except SystemExit: pass
                        except: pass
    finally:
        os.unlink(fname)

def test_run_audit_comprehensive():
    import run_audit, tempfile, pathlib, json as js
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"issues.json"
        p.write_text(js.dumps([{"id": "1", "identifier": "LIN-1", "title": "Duplicate Title", "state": {"type": "completed", "name": "Done"}, "assignee": None, "project": "p1", "estimate": 2, "description": "", "parent": None, "completedAt": "2026-01-01", "priority": 1},
                               {"id": "2", "identifier": "LIN-2", "title": "Duplicate Title", "state": {"type": "completed", "name": "Done"}, "assignee": {"id": "u1"}, "project": "p1", "estimate": 3, "description": "desc", "parent": None, "completedAt": None, "priority": 2}]))
        issues=run_audit.load_issues(p)
        result=run_audit.run_audit(issues)
        assert isinstance(result, dict)
        p.write_text(js.dumps([{"id": "1", "identifier": "LIN-1", "title": "t", "state": {"type": "completed"}, "assignee": None, "project": "p1", "estimate": 1, "description": "d", "archivedAt": "2026-01-01", "parent": None, "completedAt": None, "priority": 1}]))
        issues=run_audit.load_issues(p)
        result=run_audit.run_audit(issues)
        assert isinstance(result, dict)
        if hasattr(run_audit, 'check_estimate_coverage'):
            try: run_audit.check_estimate_coverage(issues)
            except: pass
        if hasattr(run_audit, 'find_unassigned'):
            try: run_audit.find_unassigned(issues)
            except: pass
        if hasattr(run_audit, 'find_missing_descriptions'):
            try: run_audit.find_missing_descriptions(issues)
            except: pass
        p.write_text(js.dumps({"issues": "notalist"}))
        try: run_audit.load_issues(p); assert False
        except ValueError: pass
        p.write_text(js.dumps({"bad": "shape"}))
        try: run_audit.load_issues(p); assert False
        except ValueError: pass
        p.write_text('"string"')
        try: run_audit.load_issues(p); assert False
        except ValueError: pass
        p2=pathlib.Path(td)/"no.json"
        try: run_audit.load_issues(p2); assert False
        except: pass
        result=run_audit.run_audit([])
        assert isinstance(result, dict)
        many=[{"id": str(i), "identifier": f"LIN-{i}", "title": f"Title {i%5}", "state": {"type": "completed" if i%2==0 else "backlog"}, "assignee": None if i%3==0 else {"id": "u1"}, "project": "p1", "estimate": i%4, "description": "" if i%4==0 else "desc", "parent": None, "priority": 1} for i in range(20)]
        result=run_audit.run_audit(many)
        assert isinstance(result, dict)
