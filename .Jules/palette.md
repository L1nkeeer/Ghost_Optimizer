## 2024-05-15 - Enforcing Confirmation Dialogs for Bulk Actions
**Learning:** Destructive or major bulk actions in a CLI/TUI without confirmation can lead to unintended consequences and poor user experience. Enforcing confirmation dialogs gives users a chance to reconsider.
**Action:** Always prompt the user for confirmation using `rich.prompt.Confirm` before executing bulk actions like "Apply All" or "Revert All".
