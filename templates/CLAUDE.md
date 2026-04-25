# Feedback Cluster Protocol

Paste this section into your project's `CLAUDE.md`. Adjust `<MEMORY_ROOT>` to point at where you keep your memory files.

---

## Feedback Cluster Protocol

Memory root: `<MEMORY_ROOT>`
Feedback at `<MEMORY_ROOT>/feedback-clusters/`.

- **Session start:** Read ALL global clusters + current project clusters before responding. Behavioral substrate. Skipping it means repeating old mistakes. ~2-3K tokens, non-negotiable.
- **"Feedback: text" from me:** Hook flags it. YOU pick the right cluster from context (project + content), append using the Rule + Why + How to apply format below.
- **Format (every entry):**
  ```markdown
  N. **[S#<session>] Rule in one line.** State the rule declaratively. **Why:** the incident or reasoning that produced this rule. **How to apply:** when this kicks in and the concrete action.
  ```
- **Hygiene:** Max ~20 rules per cluster. Beyond that, consolidate overlapping rules. Rules with the same trigger condition should merge.
- **Compression:** When a cluster gets too long, compress while preserving Rule + Why + How to apply structure. Don't compress to bare bullets. The `Why` is what makes rules apply at edge cases.
- **Project clusters:** Only loaded when that project is active. `<MEMORY_ROOT>/feedback-clusters/<project>/<category>.md`.
- **Conflicts:** When rules conflict, surface the conflict explicitly. Don't silently pick one.

---

## What this gives you

- Behavioral guidance that's topic-scoped, not buried in chronological order
- A capture protocol that costs you one trigger word
- A format that survives RLHF drift (rule alone gets pattern-matched; rule + why gets reasoning-applied)
- Per-cluster compression as files grow, instead of monolithic CLAUDE.md cleanup
