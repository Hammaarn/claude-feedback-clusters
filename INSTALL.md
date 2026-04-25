# Install

5 steps, ~2 minutes.

## 1. Pick your memory directory

Wherever your `CLAUDE.md` and any project memory already live. Common choices:
- `~/.claude/memory/` (global)
- `~/.claude/projects/<your-project-id>/memory/` (Claude Code's per-project memory)
- A folder in your repo (e.g. `<repo>/.claude/memory/`)

This guide uses `<MEMORY_ROOT>` as a placeholder.

## 2. Drop the hook

```bash
cp hooks/feedback-capture.py ~/.claude/hooks/feedback-capture.py
chmod +x ~/.claude/hooks/feedback-capture.py   # POSIX
```

Windows: same place, no chmod needed. `~/.claude/hooks/` = `%USERPROFILE%\.claude\hooks\`.

## 3. Wire the hook in `~/.claude/settings.json`

Add this to the `hooks` block (create one if it doesn't exist):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/feedback-capture.py"
          }
        ]
      }
    ]
  }
}
```

Windows users: use the full path (`python C:\\Users\\<you>\\.claude\\hooks\\feedback-capture.py`) or ensure `python` resolves on PATH.

## 4. Drop the cluster templates

```bash
cp -r templates/feedback-clusters <MEMORY_ROOT>/feedback-clusters
cp templates/MEMORY.md <MEMORY_ROOT>/MEMORY.md   # only if you don't already have one
```

You now have:
```
<MEMORY_ROOT>/
├── MEMORY.md
└── feedback-clusters/
    └── global/
        ├── behavioral.md
        ├── shipping-quality.md
        ├── technical.md
        └── token-process.md
```

## 5. Add the protocol to your `CLAUDE.md`

Paste the contents of `templates/CLAUDE.md` into your project's `CLAUDE.md`. Replace `<MEMORY_ROOT>` with the actual path you picked.

The minimal version:

```markdown
# Feedback Cluster Protocol
Memory root: <MEMORY_ROOT>
Feedback at `<MEMORY_ROOT>/feedback-clusters/`.

- **Session start:** Read ALL global clusters + current project clusters before responding. Behavioral substrate — skip = repeat old mistakes.
- **"Feedback: text" from me:** Hook flags. YOU pick the right cluster from context (project + content), append using the Rule + Why + How to apply format.
- **Hygiene:** Max ~20 rules per cluster. Beyond → consolidate overlapping rules.
```

## Test it

Restart Claude Code, then in any session:

```
Feedback: when reviewing code, always check for hardcoded secrets before approving
```

Claude should:
1. Acknowledge the feedback
2. Pick a cluster (probably `shipping-quality.md` or you might have a `security.md`)
3. Append the rule in the Rule + Why + How to apply format
4. Surface what it wrote so you can verify

Open the cluster file. New entry should be there.

## Troubleshooting

**Hook didn't fire:** Run `python ~/.claude/hooks/feedback-capture.py < /dev/null` — if it errors, your Python install or path is wrong. Check `~/.claude/settings.json` syntax (JSON validator).

**Claude wrote to the wrong cluster:** Tell it. The next session will land it correctly because the cluster you tell it about is now in context. Move the entry manually if you want to fix it now.

**Rules not being followed:** Check `MEMORY.md` actually points at the cluster files, and your `CLAUDE.md` includes the session-start instruction. The protocol depends on Claude reading clusters at start; without that read, the rules don't enter context.

**Want to compress a bloated cluster:** Ask Claude to compress it while preserving the Rule + Why + How to apply structure. Don't compress to bare bullets — `Why` is what makes rules apply at edge cases.
