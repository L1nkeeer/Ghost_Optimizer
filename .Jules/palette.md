## 2024-05-18 - Bulk Action Confirmations
**Learning:** Destructive or major bulk actions in the CLI (such as "Apply All" or "Revert All") can lead to accidental system changes if not confirmed.
**Action:** Enforce confirmation dialogs using `rich.prompt.Confirm` for all bulk action commands to prevent accidental execution.
