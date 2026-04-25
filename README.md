# Claude Feedback Clusters

A memory system for Claude Code that decomposes behavioral guidance into topic-specific cluster files and captures new corrections via a one-word trigger.

**What it solves:** `CLAUDE.md` grows into a wall of mixed rules, gets ignored as it bloats, and you forget what's already in there. One file is a graveyard for guidance.

**What it does:**
- Splits behavioral rules into **topic clusters** (`behavioral.md`, `technical.md`, `shipping-quality.md`, etc.)
- Loads only the relevant ones at session start
- Captures new feedback with a single trigger word. Claude routes it to the right cluster automatically.
- Uses a `Rule + Why + How to apply` format that survives RLHF drift

---

## How it works

### 1. You write a feedback line
```
Feedback: don't auto-deploy to production, always ask first
```

### 2. The hook detects the trigger
`feedback-capture.py` fires on `UserPromptSubmit`, sees the `Feedback:` prefix, injects a routing instruction into Claude's context. **Zero LLM calls. Pure regex.**

### 3. Claude classifies and writes
Claude already has full conversation context. It picks the right cluster (`shipping-quality.md` for this one) and appends the rule in the standard format.

### 4. Next session loads it back
Session-start protocol reads all global clusters plus active-project clusters. The rule is now substrate for every future response.

---

## Token economics (real numbers)

These numbers come from the author's actual setup, measured today. Your numbers will differ depending on how much of your guidance is project-specific, how many projects you run, and how often you switch contexts within a session. The patterns hold across setups even if the absolute numbers shift.

### Hook cost: zero tokens per prompt

The hook is pure regex on user input. It runs in roughly 10ms, makes zero LLM calls, and adds zero tokens to your prompt cost. The only time it adds tokens is when `Feedback:` triggers, in which case it injects ~50 tokens of routing instruction into that one turn's context. That's the entire cost.

### Author's actual setup

Token counts approximate (markdown averages ~3.5 chars per token).

**Bootloader, loaded as system context every prompt:**
- `CLAUDE.md`: ~2,900 tokens

**Loaded once per session via tool reads (then cached in conversation context):**
- `MEMORY.md` router: ~2,000 tokens
- 6 global clusters: ~12,650 tokens combined
  - `agent-dispatch.md`: ~1,475
  - `behavioral.md`: ~2,900
  - `character-pipeline.md`: ~850
  - `shipping-quality.md`: ~1,825
  - `technical.md`: ~3,500
  - `token-process.md`: ~2,090

**Project clusters, only loaded when that project is active:**
- 3 projects currently with clusters, ~2,000 tokens combined when relevant project is loaded

### What this would look like as monolithic CLAUDE.md

If every rule from every cluster lived in one `CLAUDE.md`:
- ~20,000 tokens loaded as system context **every prompt**
- All projects' rules always in context, even when working on a different project

### Where the savings actually come from

Honest framing: when most of your ruleset is genuinely global (loads regardless of project), per-session token savings are modest. The wins are structural:

1. **System-context surface stays small.** ~2,900 tokens of `CLAUDE.md` vs ~20,000 tokens. System context is sent every prompt and is the hardest to control for bloat. Keeping it small keeps it maintainable.

2. **Project switching is free.** With 3 active projects each carrying ~2,000 tokens of project-specific rules, monolithic mode pays all of them on every prompt regardless of which project you're in. Cluster mode loads only the current project's slice. The more projects you have, the bigger this gets.

3. **Per-cluster compression is tractable.** This repo's author just compressed `behavioral.md` from ~5,800 tokens to ~2,900 tokens (50% reduction) without losing any rules, in one editing pass. Try compressing a 20K monolithic file and you risk breaking unrelated rules. Per-cluster compression is the only realistic path to keeping the system maintainable over years.

4. **Attention budget is the bigger win.** Models have finite attention. A 20K monolithic CLAUDE.md gets skimmed; topic-scoped clusters of 2-3K each get attended to and applied. Token cost is similar; behavioral compliance is not.

### Estimating your own numbers

```bash
# Bootloader
wc -c CLAUDE.md

# All cluster content
wc -c <memory-root>/feedback-clusters/global/*.md
wc -c <memory-root>/feedback-clusters/<project>/*.md

# Divide bytes by ~3.5 to approximate tokens
```

Higher savings if you have many projects with substantial project-specific rules. Lower savings if your guidance is mostly global. Maintenance benefit applies regardless of setup.

---

## The format

Every entry uses three parts. This is load-bearing. Bullet-only rules drift. Rules with `Why` survive because Claude reasons about them instead of pattern-matching the surface text.

```markdown
**[S#42] Don't auto-deploy without asking.** State the rule in one line.
**Why:** You shipped a broken migration in S#37 because auto-deploy fired on a half-finished branch.
**How to apply:** Before any `vercel deploy` / `git push origin main` / production-affecting command, surface the action and wait for explicit approval.
```

Why each part matters:
- **Rule**: the behavior to encode
- **Why**: the incident or reasoning, so the rule applies at edge cases instead of pattern-matching surface
- **How to apply**: the trigger condition and concrete action, so it's not just a philosophy statement

---

## Why this beats one big CLAUDE.md

| One CLAUDE.md | Cluster system |
|---|---|
| Grows past attention budget, gets skimmed | Topic-scoped, attention-sized |
| New rules buried in chronological order | New rules land in their domain |
| Conflicting rules invisible | Domain conflicts surface |
| User has to manually classify and append | One trigger word, Claude routes |
| Hard to compress without losing context | Per-cluster compression sweeps |
| All rules loaded every session | Only active-project clusters loaded |

---

## Install

See [INSTALL.md](INSTALL.md). 5 steps, ~2 minutes.

```bash
# Quick version
cp hooks/feedback-capture.py ~/.claude/hooks/
cp -r templates/feedback-clusters ~/.claude/<your-memory-dir>/
# Then wire the hook in ~/.claude/settings.json (see INSTALL.md)
# Then add the protocol section to your CLAUDE.md (see templates/CLAUDE.md)
```

---

## What ships in this repo

```
claude-feedback-clusters/
├── README.md                          this file
├── INSTALL.md                         setup walkthrough
├── LICENSE                            MIT
├── hooks/
│   └── feedback-capture.py            the single hook (zero deps, stdlib only)
├── templates/
│   ├── CLAUDE.md                      protocol section to paste into yours
│   ├── MEMORY.md                      router template
│   ├── _format-spec.md                the Rule+Why+HowToApply spec, in detail
│   └── feedback-clusters/global/      starter clusters with header frontmatter
│       ├── behavioral.md
│       ├── shipping-quality.md
│       ├── technical.md
│       └── token-process.md
```

No dependencies. No build step. The hook is around 50 lines of Python stdlib.

---

## Customising clusters

Default clusters work for most Claude Code use. Want different topics? Rename or add `.md` files in `feedback-clusters/global/`. Claude reads the filename plus frontmatter `description` to know what belongs where.

For project-specific clusters, drop them under `feedback-clusters/<project-name>/`. They only load when that project is active.

---

## License

MIT. Use it, fork it, ship your own version.
