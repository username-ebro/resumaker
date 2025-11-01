# CLAUDE SECURITY GUIDELINES

**CRITICAL: READ THIS BEFORE EVERY COMMIT**

This document contains mandatory security rules that Claude Code MUST follow when working on this project.

## 🔴 RULE #1: NEVER COMMIT SESSION/HANDOFF FILES

**The Problem:** Session documentation (HANDOFF, SESSION, ANALYSIS files) contain API keys from the development environment.

**This has happened 15+ times. It MUST stop.**

### Files That MUST NEVER Be Committed:
- `HANDOFF_*.md`
- `SESSION_*.md`
- `*_HANDOFF_*.md`
- `ANALYSIS_*.md`
- `DEPLOYMENT_*.md` (except official docs)
- Any file created during a coding session that contains:
  - API keys
  - Environment variables
  - Auth tokens
  - Database credentials

### Exceptions (OK to commit):
- `README.md`
- `CONTEXT.md`
- `CHANGELOG.md`
- Official project documentation
- `.env.example` (examples only, never real values)

## 🔴 RULE #2: CHECK .gitignore BEFORE COMMITS

**Before running ANY `git add` or `git commit` command:**

1. Run: `git status`
2. Review the files being committed
3. Check if any match the patterns above
4. If yes → STOP and ask the user
5. If no → Proceed

## 🔴 RULE #3: USE BRANCHES FOR ALL COMMITS

**NEVER commit directly to `main` or `master`**

Pre-commit hooks will block this, but don't rely on them:

1. Always create a branch: `git checkout -b feature/description`
2. Commit to the branch
3. Let the user review before merging

## 🔴 RULE #4: API KEYS ONLY IN ENVIRONMENT VARIABLES

**Sources of API Keys:**
- `.env` files (already in .gitignore)
- Environment variables
- Secrets managers

**NEVER in:**
- Source code
- Documentation files
- Comments
- Commit messages
- Console logs

## 🔴 RULE #5: VALIDATE PRE-COMMIT HOOKS RAN

**After EVERY commit, verify:**

```bash
# You should see these pass:
Detect secrets...........................................................Passed
Detect hardcoded secrets.................................................Passed
detect private key.......................................................Passed
```

**If they don't run → STOP and investigate why**

## ⚠️ When In Doubt

**If you're unsure whether a file should be committed:**

1. ASK THE USER FIRST
2. Show them the file contents
3. Wait for explicit approval
4. Document the decision

## 📋 Quick Checklist Before Every Commit

- [ ] Did I run `git status` and review all files?
- [ ] Are there any HANDOFF/SESSION/ANALYSIS files?
- [ ] Did I check for API keys in the diff?
- [ ] Am I on a feature branch (not main)?
- [ ] Did pre-commit hooks run and pass?
- [ ] Have I shown the user what files will be committed?

## 🚨 If You Accidentally Commit a Secret

1. **STOP immediately**
2. **Tell the user right away**
3. **Do NOT push to GitHub**
4. Use `git reset --soft HEAD~1` to undo the commit
5. Remove the secret from the file
6. Add the file pattern to .gitignore
7. Commit again (without the secret)

## 💡 Remember

**The user NEVER asks you to commit API keys.**

If you find yourself committing a file with an API key, you're doing something wrong.

---

## ✅ What IS Okay: Working with API Keys in Chat

**IMPORTANT: Sharing API keys in Claude Code chat is acceptable and not a security issue.**

### Why This Is Safe:

1. **Claude Code has full file system access** - I can already read `.env`, `backend/.env`, and any file containing keys
2. **Claude Code has git push access** - I already have write access to your repositories
3. **The real threat vector is GitHub/public exposure** - NOT chat with Claude
4. **Pre-commit hooks and .gitignore prevent the actual problem** - Keys going to GitHub

### What This Means:

- ✅ **You can paste API keys in chat when troubleshooting** - This is not meaningfully different from me reading them from `.env`
- ✅ **You can ask me to help update API keys** - I can read and write to `.env` files directly
- ✅ **You don't need overly complex workarounds** - The security system prevents GitHub exposure, which is what matters
- ⚠️ **Just don't commit them to GitHub** - That's what our pre-commit hooks prevent

### The Real Security Boundary:

```
✅ SAFE:
- API keys in .env files (blocked by .gitignore)
- API keys in Claude Code chat (not committed anywhere)
- API keys in Railway environment variables

❌ DANGEROUS:
- API keys in files that get committed to GitHub
- API keys in source code
- API keys in documentation that gets pushed
```

### Trust Model:

If you trust Claude Code with:
- File system access to read your `.env`
- Git push access to your repositories
- Ability to run terminal commands

Then you can trust Claude Code with:
- API keys shared in chat for troubleshooting
- Helping you rotate/update keys
- Working with secrets when needed

**Bottom line: Don't let security theater get in the way of productivity. The pre-commit hooks and .gitignore are the actual security measures.**

---

**This file should be reviewed quarterly and updated based on incidents.**

Last updated: 2025-11-01
Last incident: Anthropic API key in HANDOFF_COMPONENTS_ANIMATIONS_OCT19.md
Security clarification added: 2025-11-01 (API keys in chat are okay)
