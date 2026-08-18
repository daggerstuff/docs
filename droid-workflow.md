# Droid Workflow Playbook (Repo)

> Repo-level supplement to the global Factory Missions README at
> `~/.factory/missions/README.md`. Lives here so you don't have to leave the
> repo to recall the recovery moves.

## Quick Start

| Scope                             | Workflow             |
| --------------------------------- | -------------------- |
| Single feature, well-scoped       | `/spec` or Shift+Tab |
| Multi-feature, ≥5 files, refactor | `/missions`          |
| Routine fix                       | direct edit          |

Templates:

- `IMPLEMENTATION_PLAN.template.md` — copy to a scoped filename.
- `.factory/rules/droid-workflow.md` — repo-specific rules.

## Prompt Shape (always)

```text
[Goal in one sentence]

[Context: file paths, ticket URLs, related code]

[Boundaries: what's out of scope]

[Workflow hint: /spec, /missions, or direct]

[Verify: concrete command and expected result]
```

## Phase Shape (Spec / Missions)

```markdown
### Phase N — <name>

**Goal**: ... **Changes**: <file paths> **Verify**: <one concrete command>
**Rollback**: <feature flag or git revert> **Status**: [ ] not started · [ ] in
progress · [ ] complete
```

## Mission Recovery (shortcuts)

- Frozen? "Re-assess and continue."
- Worker stuck? "Mark complete; move on."
- Milestone blocked? "Tell me what's blocking."
- Plan drift? "Drop X, add Y, re-plan."

Full table: `~/.factory/missions/README.md`.
