## 2024-03-24 - Enforce confirmation dialogs for destructive/bulk actions
**Learning:** Users can accidentally trigger major system changes (like "Apply All" or "Revert All" tweaks) by mis-pressing a key. Missing confirmation dialogues for such wide-ranging changes is a critical usability oversight that violates standard UX conventions.
**Action:** Always wrap major or destructive bulk actions with a confirmation prompt (e.g. `rich.prompt.Confirm`) requiring explicit user intent before execution.
