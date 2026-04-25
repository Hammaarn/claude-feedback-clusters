# Cluster Entry Format

Every cluster entry uses three parts. This format is load-bearing. Bullet-only rules drift. Rules with `Why` survive RLHF gradient pull toward agreeable interpretation.

## The format

```markdown
N. **[S#<session>] Rule stated in one line.** Optional clarifying sentence. **Why:** the incident, mechanism, or reasoning behind the rule. **How to apply:** the trigger condition and the concrete action.
```

## Each part, what it does

### Rule
- One declarative sentence
- States the behavior to encode
- Imperative voice ("Don't X", "Always Y", "When X, do Y")
- Should make sense without the Why. The Why is for edge cases, not for understanding the rule.

**Bad:** *"Be careful with deploys"* (vague, no behavior)
**Good:** *"Never auto-deploy to production. Always surface and wait for approval."* (specific, actionable)

### Why
- The incident, mechanism, or stated preference that produced the rule
- Includes session reference (`S#42`) when applicable, so you can trace context later
- Direct quotes from the user are highest-signal. Preserve them.

**Bad:** *"Why: it's important"* (no information)
**Good:** *"Why: S#37, auto-deploy fired on a half-finished branch and broke production migration. User: 'never deploy without me clicking deploy.'"*

### How to apply
- The trigger condition (when this rule fires)
- The concrete action (what to do)
- Sub-points (a), (b), (c) for multi-step responses

**Bad:** *"How to apply: be careful"*
**Good:** *"How to apply: before any `vercel deploy` / `git push origin main` / production-affecting command, (a) surface the action, (b) wait for explicit approval, (c) confirm what will be deployed."*

## Why this format works

The base model (any LLM) drifts under RLHF gradient pull toward agreeable interpretation. A bare rule like *"don't auto-deploy"* gets pattern-matched against surface text. Pattern-matching fails at edge cases (what about staging? what about preview deploys? what about hotfixes?).

The `Why` makes the rule reasoning-applied instead of pattern-matched. Knowing *why* a rule exists lets the model judge whether a new situation falls inside or outside its scope.

The `How to apply` makes the rule operational. Without it, rules drift into philosophy ("be careful") instead of behavior ("surface the command and wait").

## Hygiene

- Max ~20 rules per cluster. Beyond that, consolidate.
- When two rules have the same trigger condition, merge them.
- When a rule gets superseded, mark it `[DEPRECATED, replaced by N]` rather than deleting. Old session references should still resolve.
- Compress aggressively when a cluster grows. Preserve Rule + Why + How to apply structure. Don't compress to bare bullets.
- Direct quotes from the user are evidence. Never paraphrase them away.

## Numbering

Rules are numbered for cross-reference (`see rule 17`). When you add a rule, use the next available number. Don't reuse old numbers even if rules were deprecated. The visual order in the file doesn't have to match numerical order. The number is what's load-bearing for cross-reference.
