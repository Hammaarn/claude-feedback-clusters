# Memory Bank (Router)

> Router, not database. One-liner pointers only. HARD LIMIT: 100 lines.
> Add overflow to a separate parking-lot file or external notes vault.

## Always Active
1. Memory bank = source of truth (this file + feedback clusters).
2. Feedback clusters live at `feedback-clusters/global/*.md` and `feedback-clusters/<project>/*.md`.
3. This file stays under 100 lines. Overflow lives elsewhere.

## Feedback Clusters (READ ALL AT SESSION START)
Path: `feedback-clusters/`

**Global** (always loaded):
- [behavioral](feedback-clusters/global/behavioral.md) — partnership values, cognitive patterns, interpersonal rules
- [shipping-quality](feedback-clusters/global/shipping-quality.md) — verification layers, human gates, feature completeness
- [technical](feedback-clusters/global/technical.md) — framework gotchas, tool usage, technical rules
- [token-process](feedback-clusters/global/token-process.md) — token discipline, session management, process hygiene

**Project** (loaded when project is active):
- Add per-project clusters here as projects emerge.

**Capture:** `Feedback: text` → hook flags → Claude routes to the right cluster.

## Active Projects
<!-- Add pointers to project memory files here as you build them up -->

## Reference
<!-- Add pointers to external resources, dashboards, dev environments -->

## Pending
<!-- Open commitments — only items you've explicitly greenlit -->
