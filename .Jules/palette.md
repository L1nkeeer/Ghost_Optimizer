## 2024-05-24 - Enforce Confirmation Dialogs for Bulk CLI Actions
**Learning:** Destructive or massive bulk actions in CLI apps (e.g., 'Apply All' or 'Revert All') must prompt the user for confirmation. Users can easily misclick or mistype a command, leading to accidental system-wide changes.
**Action:** Use `rich.prompt.Confirm` to add confirmation steps before executing any significant bulk actions to ensure a safer and more intentional user experience.
