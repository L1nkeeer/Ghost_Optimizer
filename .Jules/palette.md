## 2024-07-29 - Enforce Confirmation for Bulk TUI Actions
**Learning:** Destructive or major bulk actions in a CLI/TUI can be triggered accidentally, leading to severe unintended system modifications.
**Action:** Always prompt the user for confirmation using `rich.prompt.Confirm` before executing any bulk or destructive actions in the TUI.
