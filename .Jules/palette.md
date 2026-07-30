## 2024-05-20 - Enforcing confirmation on destructive bulk actions
**Learning:** Bulk actions like Apply All or Revert All in the CLI can be destructive or major system changes. The UI requires user confirmation before execution.
**Action:** Use `rich.prompt.Confirm.ask` to confirm these actions in the CLI.
