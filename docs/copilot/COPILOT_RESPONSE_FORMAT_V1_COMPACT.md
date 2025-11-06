# Copilot Response Format V1 - Compact

**Philosophy**: Minimal overhead, maximum clarity. Surface only essential information.

---

## Response Structure

### 1. Direct Answer (if applicable)

[Answer to user's question - skip if performing actions]

### 2. Changes Summary

**Modified**: `file1.py`, `file2.json`
**Added**: `new_module.py` (150 lines)
**Key**: Implemented X feature, fixed Y bug, refactored Z

### 3. AC Status (PR #N)

✅ AC #1: [title] — Evidence: [file/commit]
⬜️ AC #2: [title] — Blocker: [what's missing]
✅ AC #3: [title] — Evidence: [file/commit]

**Tests**: 43/43 ✅ | **Coverage**: 99% ✅ | **Pylance**: 0 errors ✅ | **Pre-commit**: Pass ✅

**Ready**: ✅ YES / ❌ NO ([reason])

### 4. Next Actions

- [highest priority action]
- [alternative approach]
- [quality gate check]
- no further changes needed

---

## Example Output

**Modified**: `scripts/analyzer.py`, `tests/test_analyzer.py`
**Key**: Added impact scoring with time weighting

✅ AC #1: Impact calculator — Evidence: analyzer.py lines 45-120
✅ AC #2: Unit tests — Evidence: coverage.html (95%)
⬜️ AC #3: Integration test — Blocker: staging env not ready

**Tests**: 28/28 ✅ | **Coverage**: 95% ✅ | **Pylance**: 0 ✅ | **Pre-commit**: Pass ✅

**Ready**: ❌ NO (AC #3 incomplete, staging blocked)

**Next**:

- create mock integration test for local validation
- request staging environment access
- run pre-commit workflow
- no further changes needed
