# Full-corpus SFT tool-structure audit — 2026-10-20

The exact v4 training payload used by W&B job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` contains 171,261 trajectories and
1,056,820 messages. A privacy-preserving structural scan found:

| Message/structure | Count |
|---|---:|
| User messages | 522,658 |
| Assistant messages | 534,162 |
| Assistant messages containing tool calls | **0** |
| Tool-result messages | **0** |
| Rows containing any tool call or tool result | **0 / 171,261** |

The payload schema contains only `role`, `content`, and `weight` for each
message. This is a structural finding; no message text was printed or included
in this report.

The separate first-party synthetic agent-tool SFT release is structurally
different: its 960 training trajectories contain 1,200 structured assistant
tool-call messages and 1,200 matched tool-result messages. Its validation and
test partitions each contain 120 rows with 150 tool calls. The external
prompt-disjoint 120-case heldout evaluation has zero exact user-prompt overlap
with train, validation, or test. Within the synthetic release's own splits,
some exact user-prompt templates recur across splits (60 unique prompt strings
shared train/validation and 60 train/test); the launcher reports this overlap.
Therefore the external prompt-disjoint suite, not the internal validation/test
prompts, is the clean evaluation for generalization.

The contrast provides a direct task-alignment explanation for the consistent
v55/v56/v60 result: full-corpus checkpoints return text but make zero tool
calls on the synthetic agent-tool suite, while the base makes 131 rounds.
Plain-conversation SFT supplied no supervised tool-call behavior. This does
not prove that missing tool examples are the only cause, nor does it measure
clinical quality or safety. A tool-specific SFT run is the natural next
experiment, but the W&B launch is currently pending recovery of the already
uploaded model resource and a training-job ID.

The 960-row release passed its existing hash, row-reference, tool-call match,
heldout exclusion, and packaging checks in dry-run mode. Train payload SHA-256
is `010322208f7938085de42fdd8d2c9e529c94ac1024fd02847c6d31d4edb15d78`;
external test SHA-256 is
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`.
