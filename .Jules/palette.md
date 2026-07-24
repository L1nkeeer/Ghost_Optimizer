## 2025-05-18 - Added Bulk Action Confirmations
**Learning:** Users often trigger destructive or bulk actions accidentally in CLI apps without a safety net.
**Action:** Implemented a UX convention to always use `rich.prompt.Confirm` before executing major bulk actions (like 'Apply All' or 'Revert All') to prevent unintended changes.
