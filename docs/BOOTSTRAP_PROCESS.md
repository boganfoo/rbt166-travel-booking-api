# Bootstrap Process - New Project Setup

> **Created**: 2025-11-07
> **For**: Project 166 (rbt166-travel-booking-api)
> **Source**: Project 131 workflows

---

## Overview

This document describes the complete process for bootstrapping a new project with:
- Copilot instructions (minimal with referral pattern)
- .title workflow (auto-updating window title)
- CI/CD workflows (GitHub Actions)
- Pre-commit hooks
- Codespace configuration (32GB)

---

## Prerequisites

- GitHub CLI (`gh`) installed
- Python 3.11+ installed
- Node.js 18+ installed
- Pre-commit installed (`pip install pre-commit`)

---

## Step 1: Create Repository

```bash
# Create repository on GitHub
gh repo create <owner>/<repo-name> --public --add-readme

# Clone locally
gh repo clone <owner>/<repo-name>
cd <repo-name>
```

**For Project 166**:
```bash
gh repo clone boganfoo/rbt166-travel-booking-api
cd rbt166-travel-booking-api
```

---

## Step 2: Seed Copilot Workflow

### 2.1 Minimal Copilot Instructions

Create `.github/copilot-instructions.md` with:
- Project-specific context (tech stack, impact scoring)
- Response format rules (minimal in chat, save to markdown)
- Quick commands
- Issue label taxonomy

**See**: `.github/copilot-instructions.md` (created by seed script)

### 2.2 Response Format Documentation

Copy response format docs to `docs/copilot/`:
- `COPILOT_RESPONSE_FORMAT_GUIDE.md` (format selection guide)
- `COPILOT_RESPONSE_FORMAT_V5_HYBRID.md` (default format)
- `COPILOT_RESPONSE_FORMAT_V1_COMPACT.md` (simple format)

---

## Step 3: Seed .title Workflow

### 3.1 Title Generation Script

Copy `scripts/update_title.py` and adapt:
- Change project number (131 → 166)
- Change repository owner (rbtrends2 → boganfoo)
- Change repository name

**Result**: Window title format "166 #N CATEGORY: Description"

### 3.2 Git Hooks

Copy `.githooks/` directory:
- `post-checkout` (auto-refresh on branch switch)
- `post-commit` (auto-refresh after commits)

Configure git:
```bash
git config core.hooksPath .githooks
```

---

## Step 4: Seed CI/CD Workflows

### 4.1 Pre-commit Configuration

Copy `.pre-commit-config.yaml`:
- trailing-whitespace, end-of-file-fixer
- black, isort (Python formatting)
- flake8 (linting)

Install hooks:
```bash
pre-commit install
```

### 4.2 GitHub Actions Workflows

Copy `.github/workflows/`:
- `security-scan.yml` (dependency scanning, secrets detection)
- `auto-version.yml` (automatic versioning)

Adapt repository references (131 → 166, rbtrends2 → boganfoo)

---

## Step 5: Create Codespace Configuration

### 5.1 Devcontainer Configuration

Create `.devcontainer/devcontainer.json` with:
- **RAM**: 32GB
- **CPUs**: 4
- **Storage**: 64GB
- **Image**: Python 3.11 + Node.js 18
- **Extensions**: Python, Pylance, Black, Playwright, Copilot
- **Ports**: 8000 (Django), 3000 (Next.js), 5432 (PostgreSQL), 6379 (Redis)

### 5.2 Post-create Commands

Auto-run on codespace creation:
```bash
pip install -r requirements.txt
pre-commit install
npm install --prefix frontend
```

---

## Step 6: Create Codespace

### Via GitHub CLI
```bash
gh codespace create --repo <owner>/<repo-name> --machine largePremiumLinux
```

**For Project 166**:
```bash
gh codespace create --repo boganfoo/rbt166-travel-booking-api --machine largePremiumLinux
```

### Via GitHub UI

1. Go to repository: https://github.com/boganfoo/rbt166-travel-booking-api
2. Click "Code" → "Codespaces" → "New codespace"
3. Select machine type: "32-core • 64 GB RAM • 128 GB storage"
4. Click "Create codespace"

---

## Step 7: Verify Setup

### 7.1 Check .title Workflow

```bash
# Generate window title
python scripts/update_title.py

# Verify output
cat .title

# Expected: "166 #N CATEGORY: Description"
```

### 7.2 Check Pre-commit

```bash
# Run pre-commit checks
pre-commit run --all-files

# Expected: All checks pass
```

### 7.3 Check Copilot Instructions

Open Copilot Chat and ask:
```
What response format should I use?
```

Expected: Copilot references V5 Hybrid format and saves details to markdown.

---

## Automation Script

**One-command bootstrap**:
```bash
python tmp/seed_project_166_complete.py
```

This script automates all steps above:
1. Clone repository (if not exists)
2. Create minimal copilot instructions
3. Copy response format docs
4. Copy and adapt .title workflow
5. Copy git hooks
6. Copy pre-commit config
7. Copy GitHub Actions workflows
8. Create devcontainer config (32GB)
9. Create bootstrap documentation

**Runtime**: ~2-3 minutes

---

## Verification Checklist

- [ ] Repository cloned locally
- [ ] `.github/copilot-instructions.md` exists (minimal format)
- [ ] `docs/copilot/` contains response format docs
- [ ] `scripts/update_title.py` exists and adapted for project 166
- [ ] `.githooks/` directory exists with post-checkout, post-commit
- [ ] Git configured to use `.githooks` (`git config core.hooksPath .githooks`)
- [ ] `.pre-commit-config.yaml` exists
- [ ] Pre-commit hooks installed (`pre-commit install`)
- [ ] `.github/workflows/` contains security-scan.yml, auto-version.yml
- [ ] `.devcontainer/devcontainer.json` exists (32GB config)
- [ ] Codespace created via CLI or UI
- [ ] Window title generates correctly (166 #N CATEGORY: Description)
- [ ] Pre-commit checks pass
- [ ] Copilot uses minimal response format

---

## Troubleshooting

### Issue: .title workflow not working

**Solution**:
```bash
# Check git hooks configured
git config core.hooksPath

# Should output: .githooks

# If not, configure:
git config core.hooksPath .githooks

# Make hooks executable (Linux/Mac)
chmod +x .githooks/*
```

### Issue: Pre-commit fails on first run

**Solution**:
```bash
# Install pre-commit hooks
pre-commit install

# Run auto-fixes
pre-commit run --all-files

# Commit fixes
git add -A
git commit -m "chore: pre-commit auto-fixes"
```

### Issue: Codespace creation fails

**Solution**:
- Check repository is public or you have access
- Verify machine type is available (largePremiumLinux for 32GB)
- Try creating via GitHub UI if CLI fails

---

## Next Steps After Bootstrap

1. **Initialize Django Project**:
   ```bash
   django-admin startproject backend .
   cd backend && python manage.py startapp api
   ```

2. **Initialize Next.js Project**:
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --app
   ```

3. **Configure Amadeus API**:
   ```bash
   # Create .env file
   cp backend/.env.example backend/.env

   # Add credentials:
   AMADEUS_API_KEY=your_key
   AMADEUS_API_SECRET=your_secret
   ```

4. **Start Development**:
   ```bash
   # Backend
   python backend/manage.py runserver

   # Frontend (separate terminal)
   cd frontend && npm run dev
   ```

5. **Create First Issue**:
   ```bash
   gh issue create --title "Setup Project Foundation" --label "feat(major),size:L,impact:250"
   ```

---

**Bootstrap complete!** Ready to begin Phase 1 development.

