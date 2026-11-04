# px CLI and Eve Agents

`px` is the CLI tool (`tools/px/`) used to invoke **Eve agents** — specialized
AI agents for the Pixelated Empathy therapeutic training platform.

## What px does

- Invokes Eve agents running as services on the fleet host (by default
  `http://127.0.0.1:<port>`, see the port map below)
- Provides commands to call specific agent tools (e.g.
  `px invoke eve evaluate_corpus_gate`)
- Formats agent responses with smart formatting (scores, findings, health
  checks, async tasks)
- Manages agent configuration from `agents/px.config.json`

## Eve agent (from px config)

Agent: `eve`

- Endpoint: `http://127.0.0.1:2015`
- Tools: `clean_corpus`, `replace_slop`, `regenerate_record`,
  `evaluate_corpus_gate`
- Async: false, Timeout: 30000ms

## Fleet endpoints

`agents/px.config.json` holds all 8 agents and their default endpoints:

| Agent      | Endpoint                |
| ---------- | ----------------------- |
| supervisor | `http://127.0.0.1:2000` |
| advisor    | `http://127.0.0.1:2005` |
| content    | `http://127.0.0.1:2010` |
| eve        | `http://127.0.0.1:2015` |
| intake     | `http://127.0.0.1:2020` |
| pipeline   | `http://127.0.0.1:2025` |
| qa         | `http://127.0.0.1:2030` |
| session    | `http://127.0.0.1:2035` |

Two environment overrides change where they resolve, applied in this order:

- `PX_FLEET_HOST` — swaps the hostname on every endpoint, keeping each agent's
  port. Use this when the fleet runs on another machine.
- `PX_LOCAL=1` — points every agent at `http://localhost:${PX_LOCAL_PORT:-2000}`
  (the local stub server from `px serve`). This is what `px-agents.yml` CI
  uses.

`px config` prints the resolved endpoints. Fleet deployment is documented in
`agents/deploy/README.md`.

## Why agents use px

px CLI is the standardized way to:

- Invoke any Eve agent (advisor, content, qa, pipeline, intake, session, eve,
  supervisor)
- Route requests to the correct agent endpoint
- Get formatted, readable output
- Integrate with git hooks (pre-commit, pre-push, post-merge, pr-open, pr-merge)

The px config at `agents/px.config.json` defines 8 agents with their endpoints
and available tools, enabling the team to invoke specialized AI functionality
from the terminal.

## Related issues

- #5446: Remove hardcoded pnpm version and fix px-cli filter
- #5447: Fix CI pnpm setup and px-cli build filter
