"""
Feedback Capture Hook. Detects feedback trigger and flags for Claude to route.

Hooks into: UserPromptSubmit
Trigger: Message starts with "Feedback:" or "Feedback " (case-insensitive)
Format: "Feedback: text goes here" or "Feedback text goes here"

This hook does NOT write to files or route to clusters.
It only detects the trigger and injects a routing instruction into Claude's context.
Claude has full conversation context and knows which project/domain, so Claude does the routing.

Self-regulating: fires on every prompt, does nothing if no "Feedback" trigger.
No feedback loop risk: UserPromptSubmit only fires on human input.

Zero dependencies. Stdlib only.
"""

import json
import re
import sys


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    message = input_data.get("prompt", "")
    if not message:
        return

    # Check for feedback trigger: starts with "Feedback" (case-insensitive)
    match = re.match(r"^feedback\s*[:\-]?\s*(.+)", message.strip(), re.IGNORECASE | re.DOTALL)
    if not match:
        return  # No trigger, silent exit

    feedback_text = match.group(1).strip()

    # Inject routing instruction into Claude's context
    context = (
        f"[FEEDBACK CAPTURED] User flagged feedback: \"{feedback_text}\"\n"
        "ACTION: Determine the right cluster based on current project + content, "
        "then append to the appropriate feedback-clusters/ file using the "
        "Rule + Why + How to apply format. "
        "Path: <memory-root>/feedback-clusters/<project>/<category>.md "
        "or <memory-root>/feedback-clusters/global/<category>.md"
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }))


if __name__ == "__main__":
    main()
