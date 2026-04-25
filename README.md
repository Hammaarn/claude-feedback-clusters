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

## Token economics (the selling point)

This is the part that matters for anyone who's watched their context bloat over months.

### Hook cost: zero tokens per prompt

The hook is pure regex on user input. It runs in roughly 10ms, makes zero LLM calls, and adds zero tokens to your prompt cost.

The only time the hook adds tokens is when `Feedback:` triggers. In that case it injects roughly 50 tokens of routing instruction into that one turn's context. That's the entire cost.

### Cluster loading vs monolithic CLAUDE.md

| What loads | Monolithic `CLAUDE.md` | Cluster system |
|---|---|---|
| Bootloader / protocol | Grows into one large file over time | Stays small (~1-2K tokens) |
| Behavioral rules | Loaded as system context every prompt | Read once at session start via tool calls |
| Project-specific rules | All projects' rules always in context | Only the active project's clusters load |
| Cache write (first call) | Full rule corpus | Bootloader + only active clusters |
| Cache read (subsequent) | ~10% of full corpus per prompt | ~10% of active subset per prompt |

### Concrete example

Suppose your full ruleset is 30K tokens, but only 40% of those rules apply to your current project.

- **Monolithic CLAUDE.md:** ~30K token cache write on the first call, then ~3K tokens (cache reads) every subsequent prompt. The other 60% of rules are paid for on every turn even when irrelevant.
- **Cluster system:** ~12K token cache write (bootloader + active clusters), then ~1.2K tokens per subsequent prompt. The 60% of irrelevant rules don't load at all.

Over a 50-prompt session, that's roughly the difference between 177K and 71K tokens spent on rule context. About 60% reduction without losing any behavioral coverage.

### The bigger win is attention, not just tokens

Models have finite attention. A 30K-token wall gets skimmed. Topic-scoped clusters of 3-5K each stay legible. The rules you wrote actually get applied at the moment they should fire.

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
