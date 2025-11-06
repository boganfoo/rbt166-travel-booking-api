# Copilot Response Format V5 - Hybrid (RECOMMENDED)

**Philosophy**: Balance between detail and brevity. Comprehensive without being overwhelming.

---

## When to Use This Format

✅ **Use for**:

- Multi-step PR work (2+ acceptance criteria)
- Complex features requiring multiple files
- Bug fixes that need explanation
- Refactoring with architectural implications

❌ **Don't use for**:

- Simple typo fixes
- Documentation-only changes
- Single-line config updates
- Quick clarification questions

For those cases, use **V1 Compact** instead.

---

## Response Structure

### Part 1: What Changed (ALWAYS INCLUDE)

**Files**:

- `path/file1.py` (modified) — Brief description
- `path/file2.py` (added, 200 lines) — Brief description

**Key Changes**:

- Implemented X feature
- Fixed Y bug
- Refactored Z component

**Why This Approach**: [1-2 sentence rationale if non-obvious]

---

### Part 2: Problems Solved (INCLUDE IF APPLICABLE)

**Issue**: [Brief description of problem encountered]

- **Root Cause**: [Why it happened]
- **Solution**: [How you fixed it]
- **Prevention**: [How to avoid in future]

[Repeat for multiple issues, max 3]

---

### Part 3: Test Links (INCLUDE FOR BACKEND/FULL-STACK WORK)

**Quick Navigation**:

```
Localhost:     http://localhost:8000
PR Staging:    https://ai-project-status-pr-{N}.onrender.com
Production:    https://ai-project-status.onrender.com
```

**Current PR Links** (replace {N} with actual PR number):

- Admin: https://ai-project-status-pr-{N}.onrender.com/admin
- API: https://ai-project-status-pr-{N}.onrender.com/api/
- Dashboard: https://ai-project-status-pr-{N}.onrender.com/github-dashboard/

**Reference**: See `docs/TEST_LINKS.md` for full list

---

### Part 4: AC Progress (ALWAYS INCLUDE FOR PR WORK)

**PR**: https://github.com/{owner}/{repo}/pull/{N} — [{PR Title}]

✅ **AC #1**: [Title from ACCEPTANCE_CRITERIA.md]

- Evidence: `path/to/file.py`, `evidence/report.md`
- Verification: [How to confirm it works]

⬜️ **AC #2**: [Title from ACCEPTANCE_CRITERIA.md]

- Status: [Percentage complete or blocker]
- Next: [What needs to happen]

✅ **AC #3**: [Title from ACCEPTANCE_CRITERIA.md]

- Evidence: 31 tests, 98% coverage
- Verification: `pytest tests/test_*.py -v`

**Quality**:

- Tests: X/X ✅ | Coverage: XX% ✅ | Pylance: 0 ✅ | Pre-commit: [Pass/Fail/Not Run]

**Ready**: ✅ YES / ❌ NO ([specific blocker])

---

### Part 5: Next Steps (ALWAYS INCLUDE)

**Priority 1** (do this next):

- [Highest-priority action to move work forward]

**Priority 2** (then this):

- [Second-priority action]

**Quality Gates**:

- [Any quality checks needed before commit]

**Alternative Paths**:

- [Other approaches if user wants different direction]

**Or**:

- no further changes needed

---

## Real Example

### What Changed

**Files**:

- `scripts/check_pr_coverage.py` (modified, 614 lines) — Added `--mode developer-readiness` flag
- `scripts/utils/developer_capability_utils.py` (added, 359 lines) — Developer analysis module
- `tests/test_developer_capability.py` (added, 537 lines) — Comprehensive test suite

**Key Changes**:

- Implemented developer capability analysis with role matching and capacity scoring
- Integrated into existing PR coverage checker as optional mode
- Added exit code system: 0 (success), 1 (risks), 2 (errors)

**Why This Approach**: Separate module keeps existing role-bucket logic unchanged while enabling new analysis mode. Both can coexist without conflicts.

---

### Problems Solved

**Issue**: UnicodeEncodeError on Windows terminals

- **Root Cause**: Emoji characters (✅, ❌) can't render in cp1252 encoding
- **Solution**: Replaced with ASCII markers ([OK], [X], [!])
- **Prevention**: Test all terminal output on Windows cmd.exe early

---

### Test Links (PR #81)

**Quick Navigation**:

```
Localhost:     http://localhost:8000
PR Staging:    https://ai-project-status-pr-81.onrender.com
Production:    https://ai-project-status.onrender.com
```

**PR #81 Staging**:

- Admin: https://ai-project-status-pr-81.onrender.com/admin
- API: https://ai-project-status-pr-81.onrender.com/api/
- Dashboard: https://ai-project-status-pr-81.onrender.com/github-dashboard/

---

### AC Progress (PR #81)

**PR**: https://github.com/rbtrends2/131-RBT-ai_project_status/pull/81 — [Automate PR coverage check for role-based ticket assignments]

✅ **AC #1**: Manually runnable helper for PR auditing

- Evidence: `scripts/check_pr_coverage.py --mode developer-readiness`
- Verification: Runs successfully with exit code 0, generates report

✅ **AC #2**: Incorporates role capabilities for mahakim89 and 1di210299

- Evidence: `developer_capability_utils.py` with role_match_score(), capacity_score()
- Verification: 31 tests pass, reads from config/developer_roles.json

✅ **AC #3**: Human-readable summary with exit codes

- Evidence: `evidence/developer_readiness_report.md` with [OK]/[X] markers
- Verification: Exit codes work: 0=success, 1=risks, 2=errors

✅ **AC #4**: Usage documentation with readiness factors

- Evidence: Docstring lines 1-66 with scoring formulas
- Verification: `python scripts/check_pr_coverage.py --help` shows updated docs

✅ **AC #5**: QA workflow plan with evidence links

- Evidence: `docs/acceptance/pr-81/PR_QA_WORKFLOW_PLAN.md` (604 lines)
- Verification: All 5 ACs have evidence sections, workflow documented

**Quality**:

- Tests: 43/43 ✅ | Coverage: 99% ✅ | Pylance: 0 errors ✅ | Pre-commit: Pass ✅

**Ready**: ✅ YES (all ACs complete, all quality gates pass)

---

### Next Steps

**Priority 1** (merge now):

- Commit all changes with descriptive message
- Push to remote branch `copilot/automate-pr-coverage-check`
- Request PR review from team

**Priority 2** (optional follow-up):

- Deploy to staging for smoke test (not blocking merge)
- Create follow-up issue for cost optimization mode
- Add performance benchmarks

**Quality Gates**:

- [x] All tests passing
- [x] Pre-commit hooks clean
- [x] Evidence collected
- [x] QA plan complete

**Or**:

- no further changes needed

---

## Format Selection Guide

| Work Type                | Use Format    | Reason              |
| ------------------------ | ------------- | ------------------- |
| Quick fix (<10 lines)    | V1 Compact    | Minimal overhead    |
| Feature (1-2 ACs)        | **V5 Hybrid** | Balanced detail     |
| Complex feature (3+ ACs) | V2 Detailed   | Full context needed |
| Exploratory work         | V3 Narrative  | Explain reasoning   |
| Multi-day PR             | V4 Checklist  | Progress tracking   |
| Documentation only       | V1 Compact    | No code complexity  |
| Architecture change      | V3 Narrative  | Story matters       |
| Bug investigation        | V2 Detailed   | Root cause analysis |

**Default choice**: When in doubt, use **V5 Hybrid**.

---

## Checklist Before Responding

Before sending response, verify:

- [ ] Included "What Changed" section
- [ ] Included "Problems Solved" section (if applicable)
- [ ] Included "Test Links" section (for backend/full-stack work)
- [ ] Included "AC Progress" section (if PR work)
- [ ] **Included PR link** at top of AC Progress section (format: https://github.com/{owner}/{repo}/pull/{N})
- [ ] Included Pylance status for modified files
- [ ] Included pre-commit status
- [ ] Included "Next Steps" with priority order
- [ ] Listed specific files with line ranges (not vague references)
- [ ] Provided verification commands for evidence
- [ ] Stated commit readiness explicitly (YES/NO with reason)
- [ ] Offered "no further changes needed" option

If any checkbox unchecked, add that section before sending.
