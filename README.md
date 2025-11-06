# RBT166 - Travel Booking API

A modern travel booking platform powered by Amadeus API, enabling flight and hotel searches, price tracking, and itinerary management.

## 🚀 Tech Stack

- **Backend**: Django 5.0+ (REST API)
- **Frontend**: Next.js 14+ with TypeScript
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery + Celery Beat
- **API Integration**: Amadeus for Developers
- **Styling**: Tailwind CSS
- **Testing**: Pytest + Playwright
- **Deployment**: Render

## ✨ Core Features

### Phase 1: Foundation (Target: Dec 6, 2025)
- [x] Project setup and authentication
- [ ] Flight search API wrapper (#2)
- [ ] Hotel search API wrapper (#4)
- [ ] User authentication (#5)

### Phase 2: Core Booking (Target: Dec 20, 2025)
- [ ] Flight search UI (#3)
- [ ] Itinerary builder (#7)

### Phase 3: Advanced Features (Target: Jan 10, 2026)
- [ ] Price alert system with email notifications (#6)
- [ ] Performance optimization (#8)
- [ ] E2E testing with Playwright (#9)

### Phase 4: Polish & Launch (Target: Jan 17, 2026)
- [ ] Documentation and launch prep (#10)

## 📊 Impact Scoring Methodology

This project uses the **Impact v3** scoring system from project 131 (RBT-ai_project_status):

```python
impact_v3 = base_impact × field_multiplier × customer_multiplier × prevention_multiplier × doc_multiplier
```

**Work Type Base Scores**:
- `feat(critical)`: 150-250 points
- `feat(major)`: 100-150 points
- `feat(minor)`: 50-100 points
- `fix(critical)`: 120-200 points
- `perf`: 60-100 points
- `test`: 40-70 points
- `docs`: 20-40 points

**Multipliers**:
- **Field**: critical (3-4×), high (2-2.5×), medium (1.5-2×), low (1-1.5×)
- **Customer-facing**: 1.3× bonus
- **Prevention**: Tests (+10%), Docs (+5%), Monitoring (+5%) - stacking to max 1.21×

**Example Calculation**:
```
Flight Search API Integration:
Base: 120 (major feature, API integration)
Field: 2.0× (major feature)
Customer: 1.3× (customer-facing search)
Prevention: 1.1× (tests added)
Total: 120 × 2.0 × 1.3 × 1.1 = 343 points
```

### MVP Scope
- **Total Impact**: 2,765 points across 10 issues
- **Timeline**: 7 weeks (team) to 9-10 weeks (solo)
- **Cost Estimates**:
  - Budget: $6,160 (Juan + Martin, 9-10 weeks)
  - Recommended: $11,620 (Regan + Juan + Martin, 7 weeks)
  - Premium: $14,000 (Regan solo, 7 weeks)

## 🛠️ Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Backend Setup

```bash
# Clone repository
git clone https://github.com/boganfoo/rbt166-travel-booking-api.git
cd rbt166-travel-booking-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp backend/.env.example backend/.env

# Update .env with your credentials:
# - AMADEUS_API_KEY=your_key
# - AMADEUS_API_SECRET=your_secret
# - DATABASE_URL=postgresql://user:pass@localhost:5432/rbt166
# - REDIS_URL=redis://localhost:6379/0
# - SENDGRID_API_KEY=your_key (for email alerts)

# Run migrations
python backend/manage.py migrate

# Create superuser
python backend/manage.py createsuperuser

# Start development server
python backend/manage.py runserver
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Update .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

### Celery Setup (for price alerts)

```bash
# Terminal 1: Start Celery worker
celery -A backend worker -l info

# Terminal 2: Start Celery Beat scheduler
celery -A backend beat -l info
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Admin Panel**: http://localhost:8000/admin

## 🧪 Testing

```bash
# Backend tests
pytest backend/ -v --cov

# Frontend tests
cd frontend
npm test

# E2E tests (Playwright)
pytest tests/e2e/ --headed  # For debugging
pytest tests/e2e/  # Headless
```

## 🚀 Deployment

### Render Configuration

**Backend (Web Service)**:
- Build Command: `pip install -r requirements.txt && python backend/manage.py collectstatic --noinput && python backend/manage.py migrate`
- Start Command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
- Environment Variables: `AMADEUS_API_KEY`, `AMADEUS_API_SECRET`, `DATABASE_URL`, `REDIS_URL`, `SENDGRID_API_KEY`

**Frontend (Static Site)**:
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/out`
- Environment Variables: `NEXT_PUBLIC_API_URL`

**Celery Worker (Background Worker)**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `celery -A backend worker -l info`

**Celery Beat (Cron Job)**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `celery -A backend beat -l info`

## 📖 Architecture

```
┌─────────────────┐
│   Next.js UI    │
│  (TypeScript)   │
└────────┬────────┘
         │
         │ HTTP/REST
         ↓
┌─────────────────┐       ┌──────────────┐
│  Django API     │←─────→│  PostgreSQL  │
│  (DRF + Celery) │       │   Database   │
└────────┬────────┘       └──────────────┘
         │                         ↑
         │ API Calls               │ Task Queue
         ↓                         │
┌─────────────────┐       ┌──────────────┐
│  Amadeus API    │       │    Redis     │
│ (Flights/Hotels)│       │  (Cache +    │
└─────────────────┘       │   Broker)    │
                          └──────────────┘
```

## 🔗 Useful Links

- **Repository**: https://github.com/boganfoo/rbt166-travel-booking-api
- **Issues**: https://github.com/boganfoo/rbt166-travel-booking-api/issues
- **Milestones**: https://github.com/boganfoo/rbt166-travel-booking-api/milestones
- **Project Plan**: `docs/project_plan.md`
- **Amadeus API Docs**: https://developers.amadeus.com/self-service
- **Impact Scoring**: See "Impact Scoring Methodology" section above

## 📝 Development Guidelines

1. **All issues must include impact calculations** - See issue templates for examples
2. **Follow Django REST Framework best practices** - Use serializers, viewsets, permissions
3. **Write tests for all API endpoints** - Aim for >80% coverage
4. **Document all API endpoints** - Use docstrings + Swagger annotations
5. **Use conventional commits** - `feat:`, `fix:`, `perf:`, `docs:`, `test:`, `chore:`
6. **Never commit secrets** - Use `.env` files and environment variables

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feat/your-feature-name`
2. Make your changes and add tests
3. Run tests: `pytest backend/ -v`
4. Commit with conventional commits: `git commit -m "feat(api): add flight search caching"`
5. Push and create a PR: `git push origin feat/your-feature-name`

## 📄 License

Private project - All rights reserved.

## 👥 Team

- **Regan Behrendorff** (@boganfoo) - Architecture, Backend, DevOps
- **Juan Diego Gutierrez** (@1di210299) - Backend, API Integration
- **Martin Hakim** (@mahakim89) - Frontend, UI/UX

---

**Project Status**: 🚧 In Development (Phase 1 - Foundation)

**Last Updated**: 2025-11-08
