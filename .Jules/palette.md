## 2024-08-05 - Enforce confirmation dialogs for bulk actions
**Learning:** Destructive or major bulk actions (like 'Apply All' or 'Revert All') in the CLI without confirmation can lead to accidental, potentially harmful system modifications and a poor user experience.
**Action:** Enforce confirmation dialogs (e.g., using `rich.prompt.Confirm`) for any destructive or major bulk actions to prevent accidental execution and improve safety.
