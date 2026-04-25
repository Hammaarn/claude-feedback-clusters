---
name: global-technical
description: Framework-specific gotchas, tool usage, and technical rules that apply across projects
type: feedback-cluster
scope: global
---
# Technical

Add rules here about framework gotchas, debugging patterns, tool usage, and technical conventions that apply across multiple projects.

Example topics this cluster handles:
- Framework quirks that bit you once and shouldn't again (React useEffect deps, Next.js cache, etc.)
- Tool preferences (which package manager, which linter config)
- Debugging patterns that worked
- Hash-and-verify vs. eyeball-comparison rules
- Cache invalidation rules

Use the format spec at `feedback-clusters/_format-spec.md`.

<!-- Example entry (delete when you add your own):

1. **[S#1] Never use array/object references as React useEffect dependencies.** **Why:** S#0, infinite re-render spawned thousands of Node instances and crashed the dev machine. Reference identity changes every render. **How to apply:** use primitive values (strings, numbers, booleans) or memoized references (`useMemo`, `useCallback`) as deps. When in doubt, log the dep array and watch for shape changes between renders.

-->
