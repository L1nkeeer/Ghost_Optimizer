## 2024-08-02 - Enforce Confirmation Dialogs for Bulk Actions
**Learning:** Destructive or major bulk actions in a CLI without confirmation can lead to accidental, potentially system-altering changes, causing a poor user experience.
**Action:** Always prompt the user for confirmation (e.g., using `rich.prompt.Confirm`) before executing bulk actions like 'Apply All' or 'Revert All', and provide clear visual feedback upon cancellation.
