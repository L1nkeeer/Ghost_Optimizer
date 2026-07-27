## 2024-05-24 - Enforcing Confirmation Dialogs for Bulk Actions
**Learning:** Destructive or major bulk actions in a CLI/TUI application (such as 'Apply All' or 'Revert All') can easily be triggered accidentally if they are a single key press away. Adding a confirmation prompt prevents unintended sweeping changes to the system.
**Action:** Always wrap major bulk actions or destructive operations with a confirmation dialog (e.g. `rich.prompt.Confirm`) using the application's unified color palette.
