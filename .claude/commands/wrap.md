---
description: Wrap up current session with handoff document and Obsidian updates
---

# Wrap Up Session

Perform a comprehensive session wrap-up:

## 1. Session Summary
Create a brief summary of what was accomplished this session:
- Key completions
- Current in-progress work
- Important decisions made

## 2. Create Handoff Document
Generate a detailed handoff document (`HANDOFF_[task]_[date].md`) that includes:

### Essential Sections:
- **What We Were Doing:** Brief task summary
- **Completed This Session:** List accomplishments + files modified
- **In Progress:** Current task + exact next step + context needed
- **Remaining Tasks:** Checklist of what's left
- **Key Decisions:** Important choices and reasoning
- **Important Files:** Core files + their state
- **Mental Context:** The approach, why this way, what's tricky
- **When Resuming:** Step-by-step pickup instructions
- **Original Request:** Initial user request
- **Progress Estimate:** Completion percentage

Use the template from `SESSION_HANDOFF_TEMPLATE.md` if available.

## 3. Update Obsidian (if configured)
If `.session/obsidian-current-session` exists:
- Run `./finalize-session.sh` to update Obsidian session note
- Append session summary with:
  - Duration
  - Detailed breakdown (Added/Fixed/Patterns)
  - Mark as completed

## 4. Log Session Data (if applicable)
If `SESSION_CURRENT.json` exists:
- Calculate session duration
- Prepare session data for time logging
- Show summary for user to log manually if needed

## 5. Prepare for Compact
- Summarize key context that should survive compaction
- List critical files to remember
- Note any important state

## 6. Final Checklist
Confirm completion:
- [x] Session summary created
- [x] Handoff document generated
- [x] Obsidian updated (if configured)
- [x] Session logged (or prepared for logging)
- [x] Ready for context compact or fresh start

## 7. Provide Resume Instructions
Tell user exactly how to continue:
```
To resume: "Continue from HANDOFF_[filename].md"
```

---

**Execute all steps above automatically. Be thorough but concise.**
