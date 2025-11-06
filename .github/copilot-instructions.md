# Project 166 - Travel Booking API - Copilot Instructions

> **Project**: RBT166 Travel Booking API
> **Repository**: https://github.com/boganfoo/rbt166-travel-booking-api
> **Tech Stack**: Django 5.0+, Next.js 14+, PostgreSQL, Redis, Celery, Amadeus API
> **Last Updated**: 2025-11-07

---

## Response Format (CRITICAL)

**Use minimal responses with command palette**:

1. **In chat**: Provide brief summary with command to run
2. **Save details**: Write comprehensive analysis to markdown file

**Format**:
```
✅ [Brief action taken]

Details saved to: docs/work-logs/YYYY-MM-DD-{description}.md

Command:
    python scripts/some_command.py --args
```

**See**: `docs/copilot/COPILOT_RESPONSE_FORMAT_GUIDE.md` for format selection guide

**Default format**: V5 Hybrid (balanced detail)

---

## Project-Specific Context

### Impact Scoring Methodology (v3)

**Formula**:
```python
impact_v3 = base_impact × field_multiplier × customer_multiplier × prevention_multiplier × doc_multiplier
```

**Work Type Base Scores**:
- `feat(critical)`: 150-250 base
- `feat(major)`: 100-150 base
- `feat(minor)`: 50-100 base
- `fix(critical)`: 120-200 base
- `perf`: 60-100 base
- `test`: 40-70 base
- `docs`: 20-40 base

**Multipliers**:
- **Field**: critical (3-4×), high (2-2.5×), medium (1.5-2×), low (1-1.5×)
- **Customer-facing**: 1.3× bonus
- **Prevention**: Tests (+10%), Docs (+5%), Monitoring (+5%) - stacking to max 1.21×

**See**: README.md "Impact Scoring Methodology" section for detailed examples

---

## Tech Stack

**Backend**:
- Django 5.0+ with Django REST Framework
- PostgreSQL (primary database)
- Redis (caching + Celery broker)
- Celery + Celery Beat (background jobs)

**Frontend**:
- Next.js 14+ with App Router
- TypeScript (strict mode)
- Tailwind CSS
- React Hook Form

**API Integration**:
- Amadeus for Developers (flights, hotels)
- SendGrid (email notifications)

**Testing**:
- Pytest (backend unit/integration)
- Playwright (E2E)

**Deployment**:
- Render (backend web service, Celery worker, Celery Beat)
- Render (frontend static site)

---

## Development Workflow

### Window Title Generation

**Auto-updates** on branch switch and commits via `.githooks/`:

```bash
# Title format: "166 #N CATEGORY: Description"
python scripts/update_title.py
```

**Categories**: RENDER, GUI, CLI, API, DATA, DOCS, INFRA, FIX, FEAT, REFACTOR, TEST, DB, DEV

### Pre-commit Quality Gates

**Run before every commit**:
```bash
pre-commit run --all-files
```

**Hooks**: trailing-whitespace, end-of-file-fixer, black, isort, flake8

### Acceptance Criteria Tracking

**Location**: `docs/acceptance/pr-{N}/ACCEPTANCE_CRITERIA.md`

**Format**:
```markdown
⬜️ AC #1: [Description]
✅ AC #2: [Description] — Evidence: [file path]
```

---

## Quick Commands

### Development
```bash
# Backend
python backend/manage.py runserver

# Frontend
cd frontend && npm run dev

# Celery worker
celery -A backend worker -l info

# Celery beat
celery -A backend beat -l info
```

### Testing
```bash
# Backend tests
pytest backend/ -v --cov

# Frontend tests
cd frontend && npm test

# E2E tests
pytest tests/e2e/ --headed  # Debug mode
pytest tests/e2e/  # Headless
```

### Deployment
```bash
# Collect static files
python backend/manage.py collectstatic --noinput

# Run migrations
python backend/manage.py migrate

# Start production server
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

---

## Documentation

- **Response Formats**: `docs/copilot/COPILOT_RESPONSE_FORMAT_GUIDE.md`
- **Impact Methodology**: README.md "Impact Scoring Methodology" section
- **Bootstrap Process**: `docs/BOOTSTRAP_PROCESS.md`
- **API Documentation**: http://localhost:8000/api/docs (Swagger UI)

---

## Issue Labels

**Feature Types**:
- `feat(critical)`, `feat(major)`, `feat(minor)`

**Bug Severity**:
- `fix(critical)`, `fix(high)`, `fix(medium)`

**Domains**:
- `backend`, `frontend`, `api`, `ui`, `devops`, `security`, `celery`, `notifications`, `qa`, `playwright`

**Sizes**:
- `size:XS` (10-50), `size:S` (50-100), `size:M` (100-200), `size:L` (200-350), `size:XL` (350-500)

---

**Remember**: Save detailed analysis to markdown files, keep chat responses minimal with command palette.

