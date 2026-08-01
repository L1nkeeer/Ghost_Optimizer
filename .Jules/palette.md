## 2024-05-24 - Bulk Action Confirmation
**Learning:** Destructive or major bulk actions (like Apply All or Revert All) can be accidentally triggered, leading to unwanted system changes.
**Action:** Always wrap major bulk actions in a confirmation dialog (e.g., `rich.prompt.Confirm`) before execution and provide contextual feedback on cancellation.
