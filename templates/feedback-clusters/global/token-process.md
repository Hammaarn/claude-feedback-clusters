---
name: global-token-process
description: Token discipline, session management, process hygiene, and focus management
type: feedback-cluster
scope: global
---
# Token & Process

Add rules here about how to spend tokens efficiently, when to use cheaper models, how to manage long sessions, and process hygiene.

Example topics this cluster handles:
- When to use Haiku vs. Sonnet vs. Opus
- How to read large files (limit/offset, head_limit on grep)
- When to delegate to subagents vs. do it inline
- How to handle context approaching limits
- When to push back on user requests that would burn tokens unnecessarily

Use the format spec at `feedback-clusters/_format-spec.md`.

<!-- Example entry (delete when you add your own):

1. **[S#1] Use limit/offset on large file reads.** **Why:** S#0, reading an 80K-character file consumed half the session's token budget for context that wasn't needed. **How to apply:** when a file is larger than ~500 lines, read with explicit `limit` and `offset` parameters. For grep, use `head_limit` to cap matches. If you need the whole file, justify that need.

-->
