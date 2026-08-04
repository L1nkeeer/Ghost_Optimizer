## 2024-08-04 - Enforcing Confirmation Dialogs for Bulk Actions
**Learning:** Destructive or major bulk actions in a CLI (such as 'Apply All' or 'Revert All') can lead to unintended system changes and poor UX if executed accidentally. Prompting for confirmation prevents these errors.
**Action:** Always enforce confirmation dialogs (e.g., using `rich.prompt.Confirm`) for bulk actions, and provide visual feedback (like `MUTED` status) when actions are aborted.
