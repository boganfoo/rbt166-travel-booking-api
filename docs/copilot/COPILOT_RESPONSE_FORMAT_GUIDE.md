# Copilot Response Format Guide

> **Purpose**: Help select the right response format and ensure quality compliance
> **Created**: 2025-10-22 (PR #83)
> **Related**: docs/COPILOT_RESPONSE_FORMATS_INDEX.md

---

## Quick Format Selection

Use this decision tree to pick the right format variant:

```
Is this PR work (vs one-off question)?
├─ NO → Answer directly, no format needed
└─ YES → Continue
    │
    Is this a trivial change (<10 lines, obvious fix)?
    ├─ YES → Use V1 Compact
    └─ NO → Continue
        │
        Is this exploratory/experimental work?
        ├─ YES → Use V3 Narrative
        └─ NO → Continue
            │
            Is this a multi-day PR with many tasks?
            ├─ YES → Use V4 Checklist
            └─ NO → Continue
                │
                Is this architecturally complex (3+ ACs, multiple systems)?
                ├─ YES → Use V2 Detailed
                └─ NO → Use V5 Hybrid (DEFAULT)
```

**When in doubt**: Use **V5 Hybrid**

---

## Format Cheat Sheet

| Work Type                     | Format       | Key Sections                    |
| ----------------------------- | ------------ | ------------------------------- |
| Quick fix (<10 lines)         | V1 Compact   | Changes + AC + Actions          |
| Standard feature (1-2 ACs)    | V5 Hybrid    | What + Problems + AC + Actions  |
| Complex feature (3+ ACs)      | V2 Detailed  | Technical + Bugfix + AC + Menu  |
| Exploratory/architecture work | V3 Narrative | Work + Problems + Evidence      |
| Multi-day PR (many tasks)     | V4 Checklist | ✅ Done + ⏳ In Progress + Menu |
| Documentation only            | V1 Compact   | Minimal overhead                |
| Bug investigation             | V2 Detailed  | Root cause analysis             |

---

## Required Elements (ALL FORMATS)

Every response for PR work **MUST** include:

### 1. AC Progress Section

```markdown
## Acceptance Criteria Progress (PR #N)

**PR**: https://github.com/{owner}/{repo}/pull/{N} — [{PR Title}]

✅ AC #1: [Description] — Evidence: [file path]
⬜️ AC #2: [Description] — Blocker: [what's missing]
```

**Requirements**:

- Read from `docs/acceptance/pr-N/ACCEPTANCE_CRITERIA.md`
- Mark each AC: ✅ complete or ⬜️ incomplete
- Provide evidence file paths for completed items
- Include PR link at top of section

### 2. Testing Metrics

```markdown
**Testing Metrics**:

- Tests Run: X passed, Y failed
- Coverage: X% (target: 80%+)
- Test Command: pytest tests/test\_\*.py -v --cov
```

### 3. Pylance Error Check

```markdown
**Pylance Error Check**:

- Modified Files: [file1.py, file2.py]
- Pylance Errors: X errors (target: 0)
- Check Command: pyright [files]
```

### 4. Pre-commit Status

```markdown
**Pre-commit**: Pass ✅ / Fail ❌ / Not Run
```

If fail, state what needs fixing.

### 5. Commit Readiness

```markdown
**Commit Readiness**: ✅ YES / ❌ NO ([specific reason])
```

Must be explicit with blocker if NO.

### 6. Suggested Commit

```markdown
## Suggested Commit

\`\`\`
<type>(<scope>): <description>

[Optional body]
[Optional footer]
\`\`\`

**Impact Estimate**: [estimated v3 score] ([work type], [priority], [N] files touched)
**Evidence**: [key files changed]
```

Must reflect work done in current conversation.

### 7. Next Immediate Actions

```markdown
## Next Immediate Actions

### #1 QA Progression

[Most important quality/testing action with specific command]

### #1 AC Progression

[Most important AC completion step citing specific number]

---

## Standard Actions (Reference)

If above recommendations don't apply or additional options needed:

- continue QA work on current PR following QA tag workflow
- run pre-commit workflow until green: python tmp/precommit_until_clean.py
- run tests for this PR and check coverage: pytest tests/test_X -v --cov
- gather evidence artifacts and update AC document with links
- no further changes needed

### PR-Specific Context Actions

[Include context-specific actions for current PR if not covered by #1 recommendations above]
```

Must be at the **very end** of response.

---

## Validation Tool

Use the validator to check format compliance:

```bash
# Validate a saved response
python tmp/validate_copilot_response.py response.md

# Validate with verbose output
python tmp/validate_copilot_response.py response.md --verbose

# Strict mode (warnings become violations)
python tmp/validate_copilot_response.py response.md --strict
```

Exit codes:

- `0`: Valid format
- `1`: Has violations
- `2`: File error

---

## Good vs Bad Examples

### ✅ Good Example 1: V5 Hybrid (Standard Feature)

```markdown
### What Changed

**Files**:

- `scripts/analyzer.py` (modified, 300 lines) — Added impact scoring
- `tests/test_analyzer.py` (added, 150 lines) — Full test coverage

**Key Changes**:

- Implemented weighted impact calculation using time investment
- Fixed edge case for empty commits (returned 0 instead of crashing)
- Refactored to use strategy pattern for different impact algorithms

**Why This Approach**: Strategy pattern allows easy addition of new scoring
algorithms without modifying core logic.

---

### Problems Solved

**Issue**: Division by zero for commits with no time data

- **Root Cause**: WakaTime API returns null for very old commits
- **Solution**: Default to 1.0 hours when time_investment is None
- **Prevention**: Added validation in fuse_time_and_impact.py

---

### AC Progress (PR #45)

**PR**: https://github.com/rbtrends2/131-RBT-ai_project_status/pull/45 — [Add impact scoring]

✅ **AC #1**: Impact calculator functional

- Evidence: `scripts/analyzer.py` lines 100-250
- Verification: `python scripts/analyzer.py --test` outputs valid scores

⬜️ **AC #2**: Integration tests

- Status: 60% complete
- Next: Add mock GitHub API responses for edge cases

**Quality**:

- Tests: 28/28 ✅ | Coverage: 95% ✅ | Pylance: 0 ✅ | Pre-commit: Pass ✅

**Ready**: ❌ NO (AC #2 incomplete)

---

## Suggested Commit
```

feat(analyzer): add weighted impact scoring with time investment

Implements AC #1 for PR #45 with strategy pattern for extensibility.

- Added time-weighted impact calculation (time_investment \* impact_score)
- Fixed division by zero for commits missing WakaTime data (default 1.0h)
- Implemented strategy pattern for multiple scoring algorithms
- Added 28 unit tests with 95% coverage

Evidence: scripts/analyzer.py, tests/test_analyzer.py
Tests: pytest tests/test_analyzer.py -v --cov

```

**Impact Estimate**: 78.5 (feature work, major scope, 2 files touched)
**Evidence**: scripts/analyzer.py (+300 lines), tests/test_analyzer.py (+150 lines)

---

## Next Immediate Actions

### #1 QA Progression
Add mock GitHub API responses for edge case testing → pytest tests/test_analyzer.py::test_api_edge_cases -v --cov

### #1 AC Progression
Complete AC #2 integration tests (currently 60% done) → add 3 remaining test scenarios for API error handling

---

## Standard Actions (Reference)

If above recommendations don't apply or additional options needed:

- continue QA work on current PR following QA tag workflow
- run pre-commit workflow until green: python tmp/precommit_until_clean.py
- run tests for this PR and check coverage: pytest tests/test_X -v --cov
- gather evidence artifacts and update AC document with links
- no further changes needed

### PR-Specific Context Actions

- refactor strategy pattern to support additional scoring algorithms
- benchmark performance with 10k commit dataset
```

**Why this is good**:

- ✅ Clear file paths with line ranges
- ✅ Explains rationale ("Why This Approach")
- ✅ Documents problem and solution
- ✅ Provides verification commands
- ✅ All required sections present
- ✅ PR link at top of AC section
- ✅ Suggested commit reflects actual work done
- ✅ Impact estimate with justification
- ✅ #1 QA/AC give specific next steps
- ✅ Next Immediate Actions at very end
- ✅ Action Menu at end
- ✅ Explicit commit readiness with reason

---

### ✅ Good Example 2: V1 Compact (Quick Fix)

```markdown
**Modified**: `config/author_rates.json`
**Key**: Added rate for new developer @alice (45 AUD/hr)

✅ AC #1: Rate table updated — Evidence: config/author_rates.json line 23
✅ AC #2: Validation passes — Evidence: pytest tests/test_rates.py (3/3 ✅)

**Tests**: 3/3 ✅ | **Coverage**: 100% ✅ | **Pylance**: 0 ✅ | **Pre-commit**: Pass ✅

**Ready**: ✅ YES

**Next**:

- commit and push changes
- no further changes needed
```

**Why this is good**:

- ✅ Minimal overhead for simple change
- ✅ All required elements present (AC, tests, readiness)
- ✅ Clear evidence links
- ✅ Appropriate for scope of work

---

### ✅ Good Example 3: V2 Detailed (Complex Feature)

```markdown
### Technical Details

**Files Changed**:

- `scripts/analyzer.py` (modified, 450 → 620 lines) — Core analysis engine
- `scripts/utils/impact_calculator.py` (added, 380 lines) — Impact scoring module
- `scripts/utils/time_fusion.py` (modified, 200 → 280 lines) — Enhanced fusion logic
- `tests/test_impact_calculator.py` (added, 450 lines) — Comprehensive test suite
- `config/impact_weights.json` (added) — Configurable scoring weights

**Key Changes**:

- Implemented multi-layer impact scoring with weighted factors
- Added configurable weight system for different project types
- Refactored time fusion to handle missing WakaTime data gracefully
- Added caching layer to avoid redundant calculations
- Implemented validation for all weight configurations

**Dependencies**:

- Added: scipy==1.11.0 (statistical functions for scoring)
- Updated: numpy from 1.24.0 to 1.26.0 (security patch)

**Architecture Notes**:

- Uses strategy pattern for impact algorithms (easy to extend)
- Maintains backward compatibility with v1 scoring API
- Config-driven weights avoid hardcoding business rules
- Cache invalidation on config changes

---

### Bugfixing Log

**Problems Encountered**:

1. **Issue**: Scipy import failed on Windows

   - **Root Cause**: Scipy requires specific BLAS library on Windows
   - **Solution**: Added platform-specific install instructions to README
   - **Prevention**: Test on Windows VM before marking complete

2. **Issue**: Cache returning stale data after config update
   - **Root Cause**: Cache key didn't include config file hash
   - **Solution**: Include config hash in cache key calculation
   - **Prevention**: Added test for cache invalidation on config change

**Ongoing Issues**:

- Performance with >50k commits (takes 45s, target <10s) — investigating parallel processing

---

### AC Progress (PR #47)

**PR**: https://github.com/rbtrends2/131-RBT-ai_project_status/pull/47 — [Multi-layer impact scoring]

✅ **AC #1**: Configurable weight system

- Evidence: `config/impact_weights.json`, `impact_calculator.py` lines 50-120
- Verification: `python scripts/analyzer.py --config custom_weights.json` applies weights
- Notes: Supports project-specific overrides

✅ **AC #2**: Multi-layer scoring implementation

- Evidence: `impact_calculator.py` with 4 scoring layers (raw/enriched/advanced/fusion)
- Verification: 45 tests in test_impact_calculator.py, all layers tested independently
- Notes: Each layer can be disabled via config

⬜️ **AC #3**: Performance optimization (<10s for 50k commits)

- Status: 40% complete (currently 45s, target 10s)
- Blocker: Parallel processing not yet implemented
- Workaround: Using sequential processing with progress bar
- ETA: 4 hours to implement multiprocessing

✅ **AC #4**: Documentation and examples

- Evidence: `docs/IMPACT_SCORING.md` (2400 words), inline docstrings
- Verification: Sphinx docs build successfully, 98% API coverage

**Testing Metrics**:

- Tests Run: 87 passed, 0 failed, 2 skipped (performance benchmarks)
- Coverage: 94% overall (target: 80%+)
  - impact_calculator.py: 97% (368/379 statements)
  - time_fusion.py: 92% (138/150 statements)
  - analyzer.py: 89% (245/275 statements, missing error paths)
- Test Command: `pytest tests/test_impact*.py -v --cov=scripts --cov-report=html:docs/acceptance/pr-47/evidence/coverage/`
- Coverage Report: `docs/acceptance/pr-47/evidence/coverage/index.html`

**Pylance Error Check**:

- Modified Files: analyzer.py, impact_calculator.py, time_fusion.py
- Pylance Errors: 0 errors (target: 0) ✅
- Warnings: 1 unused import in test file (cleaned)
- Check Command: pyright scripts/analyzer.py scripts/utils/\*.py

**QA Checklist**:

- [x] All AC items have evidence files
- [x] Tests pass with 80%+ coverage (94% achieved)
- [x] Pylance errors = 0 for all modified files
- [x] Pre-commit hooks pass (black, isort, flake8)
- [x] Documentation updated (IMPACT_SCORING.md, docstrings)
- [ ] Performance benchmark met (45s vs 10s target)
- [ ] Manual smoke test completed (pending AC #3)

**Commit Readiness**: ❌ NOT READY (AC #3 incomplete, performance target not met)

---

## Action Menu

### Standard Actions (Always Available)

- continue work on incomplete AC items and gather evidence
- run pre-commit workflow until green: python tmp/precommit_until_clean.py
- run tests for this PR and check coverage: pytest -v --cov
- run smoke tests in Render staging with Playwright MCP tool

### PR-Specific Actions

- implement parallel processing for AC #3 using multiprocessing.Pool
- add performance benchmark tests to track progress toward 10s target
- consider splitting PR (merge current work, defer performance to follow-up)
- profile code with cProfile to identify bottlenecks
- no further changes needed
```

**Why this is good**:

- ✅ Comprehensive technical context
- ✅ Documents architecture decisions
- ✅ Detailed bugfixing log with prevention
- ✅ Granular coverage metrics
- ✅ Clear blockers with ETAs
- ✅ QA checklist with checkboxes
- ✅ Multiple action options

---

## ❌ Bad Example 1: Missing Required Sections

```markdown
I updated the analyzer script to add impact scoring. It works now.

The tests pass.

Let me know if you need anything else.
```

**Problems**:

- ❌ No AC progress section
- ❌ No Pylance check
- ❌ No file paths or evidence
- ❌ No commit readiness statement
- ❌ No testing metrics
- ❌ No suggested commit message
- ❌ No prioritized next actions (#1 QA, #1 AC)
- ❌ Vague descriptions

**Fix**: Use V1 Compact at minimum, include all required sections (AC progress, suggested commit, next immediate actions).

---

## ❌ Bad Example 2: Inconsistent Readiness

```markdown
### AC Progress (PR #50)

✅ AC #1: Feature implemented
✅ AC #2: Tests passing
✅ AC #3: Documentation updated

**Tests**: 42/42 ✅ | **Coverage**: 98% ✅ | **Pylance**: 0 ✅

**Ready**: ❌ NO (needs review)

### Next Steps

- request code review
- no further changes needed
```

**Problems**:

- ❌ All ACs complete but marked NOT READY (inconsistent)
- ❌ "needs review" is not a blocker (that's normal PR flow)
- ❌ Missing PR link at top of AC section
- ❌ No suggested commit message
- ❌ No Next Immediate Actions section (just "Next Steps")
- ❌ Not using #1 QA Progression / #1 AC Progression format

**Fix**: Should be ✅ READY since all ACs complete. Code review happens after marking ready. Add suggested commit and prioritized #1 QA/#1 AC actions.

---

## ❌ Bad Example 3: Next Immediate Actions Not at End

```markdown
### AC Progress (PR #52)

✅ AC #1: Done
⬜️ AC #2: In progress

**Ready**: ❌ NO (AC #2 incomplete)

---

## Next Immediate Actions

### #1 QA Progression

Complete integration tests

### #1 AC Progression

Finish AC #2 implementation

---

## Additional Notes

Here are some extra thoughts about the implementation...
[300 more lines]
```

**Problems**:

- ❌ Content after Next Immediate Actions (violates placement rule)
- ❌ Missing PR link
- ❌ Missing testing metrics
- ❌ Missing Pylance check
- ❌ Missing suggested commit message before Next Immediate Actions
- ❌ Next actions lack specific commands (should be exact pytest/pyright commands)
- ❌ Missing Standard Actions (Reference) section
- ❌ Missing PR-Specific Context Actions section

**Fix**: Move Next Immediate Actions to absolute end, add suggested commit with impact estimate, make #1 actions specific with commands, include reference sections.

---

## ❌ Bad Example 4: No Evidence or Verification

```markdown
### AC Progress (PR #55)

✅ AC #1: Feature works
✅ AC #2: Tests added
⬜️ AC #3: Still working on it

**Ready**: ❌ NO
```

**Problems**:

- ❌ No evidence file paths for completed ACs
- ❌ No verification commands
- ❌ No specific blocker for AC #3
- ❌ No reason for NOT READY
- ❌ Missing all quality metrics
- ❌ Missing PR link
- ❌ No Action Menu

**Fix**: Add evidence paths, verification commands, specific blockers, and all required sections.

---

## ❌ Bad Example 5: Vague File References

```markdown
### What Changed

**Files**: Updated some Python files and config

**Changes**: Fixed bugs and added features

### AC Progress (PR #60)

✅ AC #1: Done — Evidence: see the code
✅ AC #2: Done — Evidence: in the tests

**Ready**: ✅ YES
```

**Problems**:

- ❌ No specific file paths (which Python files?)
- ❌ No line ranges
- ❌ Vague evidence ("see the code", "in the tests")
- ❌ No testing metrics
- ❌ No verification commands
- ❌ Missing PR link
- ❌ No Action Menu

**Fix**: Provide exact file paths with line ranges, specific evidence, verification commands.

---

## Pre-Response Checklist

Before sending a response for PR work, verify:

- [ ] Included AC Progress section with PR link at top
- [ ] Each AC marked with ✅ or ⬜️
- [ ] Evidence file paths for completed ACs (with line ranges if code)
- [ ] Verification commands for each AC
- [ ] Testing metrics (tests run, coverage %)
- [ ] Pylance error check for modified files
- [ ] Pre-commit status
- [ ] Explicit commit readiness (YES/NO with reason if NO)
- [ ] Suggested Commit section with impact estimate and evidence
- [ ] Commit message reflects actual work done in conversation
- [ ] Next Immediate Actions at the very end
- [ ] #1 QA Progression with specific command
- [ ] #1 AC Progression citing specific AC number
- [ ] Standard Actions (Reference) section present
- [ ] PR-Specific Context Actions when applicable
- [ ] No content after Next Immediate Actions

**Validation**: Run `python tmp/validate_copilot_response.py` on response before sending.

---

## Tips for High-Quality Responses

### 1. Be Specific with File Paths

❌ Bad: "Updated the analyzer"
✅ Good: "`scripts/analyzer.py` lines 100-250"

### 2. Provide Verification Commands

❌ Bad: "Tests pass"
✅ Good: "`pytest tests/test_analyzer.py -v` (28/28 passed)"

### 3. Explain Blockers Clearly

❌ Bad: "Not ready"
✅ Good: "❌ NO (AC #2 incomplete - awaiting API key from ops team, ETA 2 hours)"

### 4. Link to Evidence

❌ Bad: "Code is done"
✅ Good: "Evidence: `analyzer.py` lines 100-250, `tests/test_analyzer.py` (95% coverage)"

### 5. Write Commit Messages Based on Work Done

❌ Bad: Generic template like "feat: update analyzer"
✅ Good: Specific details like "feat(analyzer): add weighted impact scoring with time investment - Implemented strategy pattern, added 28 tests with 95% coverage"

### 6. Make #1 Actions Actionable

❌ Bad: "#1 QA Progression: Add more tests"
✅ Good: "#1 QA Progression: Add mock GitHub API responses for edge case testing → pytest tests/test_analyzer.py::test_api_edge_cases -v --cov"

### 5. Categorize Actions

❌ Bad: Long bullet list of mixed actions
✅ Good: Separate Standard Actions (always same) from PR-Specific Actions (contextual)

### 6. Include PR Context

❌ Bad: AC section with no PR reference
✅ Good: "**PR**: https://github.com/owner/repo/pull/45 — [Add impact scoring]"

---

## Format References

- **V1 Compact**: docs/COPILOT_RESPONSE_FORMAT_V1_COMPACT.md
- **V2 Detailed**: docs/COPILOT_RESPONSE_FORMAT_V2_DETAILED.md
- **V3 Narrative**: docs/COPILOT_RESPONSE_FORMAT_V3_NARRATIVE.md
- **V4 Checklist**: docs/COPILOT_RESPONSE_FORMAT_V4_CHECKLIST.md
- **V5 Hybrid (Recommended)**: docs/COPILOT_RESPONSE_FORMAT_V5_HYBRID.md
- **Format Index**: docs/COPILOT_RESPONSE_FORMATS_INDEX.md

---

## Validator Integration

The validator (`tmp/validate_copilot_response.py`) checks for:

**Required**:

- AC Progress section with PR link
- AC items with ✅/⬜️ checkboxes
- Evidence references
- Testing metrics
- Commit readiness statement
- Action Menu at end

**Recommended** (warnings):

- Pylance error check
- Pre-commit status
- Files changed section
- File paths in evidence

Run validator after generating response:

```bash
# Save response to file
cat > response.md

# Validate
python tmp/validate_copilot_response.py response.md

# Exit code 0 = valid, 1 = violations
echo $?
```

---

## Version History

- **2025-10-22**: Initial creation (PR #83)
- **Future**: Add format for specific edge cases as needed

---

## Quick Links

- [Validator Script](../tmp/validate_copilot_response.py)
- [Test Suite](../tests/test_response_validator.py)
- [Copilot Instructions](.github/copilot-instructions.md)
- [Format Index](./COPILOT_RESPONSE_FORMATS_INDEX.md)
