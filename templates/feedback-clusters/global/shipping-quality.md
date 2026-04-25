---
name: global-shipping-quality
description: Verification layers, human gates, feature completeness, and quality standards
type: feedback-cluster
scope: global
---
# Shipping & Quality

Add rules here about what counts as "done", what requires human approval before shipping, and quality standards.

Example topics this cluster handles:
- What "complete" means for a feature
- Which actions require explicit user approval (deploys, schema changes, force pushes)
- Verification steps before reporting work as done
- Standards for tests, types, and reviews
- How to handle disabled or deprecated systems

Use the format spec at `feedback-clusters/_format-spec.md`.

<!-- Example entry (delete when you add your own):

1. **[S#1] Never auto-deploy to production — always surface and wait for approval.** **Why:** S#0, auto-deploy fired on a half-finished branch and broke production migration. **How to apply:** before any `vercel deploy` / `git push origin main` / production-affecting command, (a) surface the action, (b) state what will be deployed, (c) wait for explicit approval.

-->
