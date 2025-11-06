"""
Update .title file based on environment (local vs Codespace) and current PR.

Format:
- Local: "131 | PR-111 | Short Name"
- Codespace: "131 | PR-111 | Short Name | CS"

Detects:
- Project number from repo name (e.g., "rbt166-travel-booking-api" -> "131")
- PR number and title from current branch
- Codespace environment from CODESPACE_NAME env var
"""
from __future__ import annotations

import os
import re
import subprocess
import json
from pathlib import Path


def get_repo_slug() -> str:
    """Get repository owner/name from git remote."""
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Failed to get git remote URL")

    url = result.stdout.strip()

    # Extract owner/repo from URL
    if url.startswith("git@github.com:"):
        slug = url.split(":", 1)[1].replace(".git", "")
    elif url.startswith("https://github.com/"):
        slug = url.split("https://github.com/", 1)[1].replace(".git", "")
    else:
        raise RuntimeError(f"Unrecognized git remote format: {url}")

    return slug


def get_repo_name_from_slug(slug: str) -> str:
    """Extract just the repo name from owner/repo slug."""
    return slug.split("/")[-1]


def extract_project_number(repo_name: str) -> str:
    """Extract project number from repo name (e.g., '131-RBT-...' -> '131')."""
    match = re.search(r'(\d+)[-_]', repo_name)
    if not match:
        raise RuntimeError(f"Could not extract project number from repo: {repo_name}")
    return match.group(1)


def get_current_branch() -> str:
    """Get current git branch name."""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Failed to get current branch")
    return result.stdout.strip()


def categorize_work(title: str, branch: str) -> str:
    """
    Determine work category from PR title and branch name.

    Returns single-word prefix: RENDER, GUI, CLI, API, DATA, DOCS, INFRA, FIX, FEAT, etc.
    """
    title_lower = title.lower()
    branch_lower = branch.lower()

    # Check for specific keywords in title/branch
    if any(word in title_lower or word in branch_lower for word in ['render', 'deploy', 'staging']):
        return "RENDER"
    elif any(word in title_lower or word in branch_lower for word in ['gui', 'dashboard', 'ui', 'interface']):
        return "GUI"
    elif any(word in title_lower or word in branch_lower for word in ['cli', 'command', 'script']):
        return "CLI"
    elif any(word in title_lower or word in branch_lower for word in ['api', 'endpoint', 'rest']):
        return "API"
    elif any(word in title_lower or word in branch_lower for word in ['data', 'analysis', 'report', 'metrics']):
        return "DATA"
    elif any(word in title_lower or word in branch_lower for word in ['doc', 'readme', 'guide']):
        return "DOCS"
    elif any(word in title_lower or word in branch_lower for word in ['infra', 'ci', 'cd', 'pipeline']):
        return "INFRA"
    elif any(word in title_lower or word in branch_lower for word in ['fix', 'bug', 'issue', 'hotfix']):
        return "FIX"
    elif any(word in title_lower or word in branch_lower for word in ['feat', 'feature', 'add', 'enhance']):
        return "FEAT"
    elif any(word in title_lower or word in branch_lower for word in ['refactor', 'cleanup', 'improve']):
        return "REFACTOR"
    elif any(word in title_lower or word in branch_lower for word in ['test', 'qa', 'coverage']):
        return "TEST"
    elif any(word in title_lower or word in branch_lower for word in ['cache', 'db', 'database']):
        return "DB"
    else:
        return "DEV"


def get_pr_info(branch: str, repo_slug: str) -> tuple[str | None, str | None, str]:
    """
    Extract PR number from branch and fetch actual PR title from GitHub.

    Examples:
    - "pr/copilot-swe-agent/111" -> ("111", "Actual PR Title from GitHub", "RENDER")
    - "feature/add-dashboard" -> (None, "Add Dashboard", "GUI")
    - "copilot/enhance-coauthor" -> ("108", "Enhance co-author attribution", "FEAT")

    Returns: (pr_number, short_name, category)
    """
    # Try to extract PR number from branch name (e.g., pr/copilot-swe-agent/111)
    pr_match = re.search(r'/(\d+)$', branch)
    pr_number = pr_match.group(1) if pr_match else None

    short_name = None
    full_title = ""

    # If no PR number in branch name, try to find PR by branch name
    if not pr_number:
        try:
            result = subprocess.run(
                ["gh", "pr", "list", "--head", branch, "--json", "number,title", "--limit", "1", "--repo", repo_slug],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                if data:
                    pr_number = str(data[0].get("number", ""))
                    full_title = data[0].get("title", "")
                    short_name = full_title[:40] + "..." if len(full_title) > 40 else full_title
        except Exception:
            pass  # Fall back to direct PR fetch or branch parsing

    # If we have a PR number but no title yet, fetch it
    if pr_number and not short_name:
        try:
            result = subprocess.run(
                ["gh", "pr", "view", pr_number, "--json", "title", "--repo", repo_slug],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                full_title = data.get("title", "")
                # Truncate and clean up title
                short_name = full_title[:40] + "..." if len(full_title) > 40 else full_title
        except Exception:
            pass  # Fall back to branch parsing    # Fallback: extract from branch name if GitHub fetch failed
    if not short_name:
        parts = branch.split('/')
        if len(parts) > 1:
            short_name = parts[-2] if pr_number and len(parts) > 2 else parts[-1]
            short_name = short_name.replace('-', ' ').title()
            if len(short_name) > 40:
                short_name = short_name[:40] + '...'
        else:
            short_name = branch.replace('-', ' ').title()[:40]
        full_title = short_name

    # Determine category
    category = categorize_work(full_title, branch)

    return pr_number, short_name, category


def is_codespace() -> bool:
    """Check if running in a GitHub Codespace."""
    return bool(os.getenv("CODESPACE_NAME"))


def generate_title() -> str:
    """
    Generate .title content based on current environment.

    New format: "131 #111 CATEGORY: Description (CS)"
    Examples:
    - "131 #111 RENDER: Fix deployment issues (CS)"
    - "131 #108 DATA: Add co-author impact"
    - "131 CLI: Quick analysis scripts"
    """
    repo_slug = get_repo_slug()
    repo_name = get_repo_name_from_slug(repo_slug)
    project_num = extract_project_number(repo_name)
    branch = get_current_branch()
    pr_number, short_name, category = get_pr_info(branch, repo_slug)
    in_codespace = is_codespace()

    # Build title: "131 #111 CATEGORY: Description (CS)"
    if pr_number:
        title = f"{project_num} #{pr_number} {category}: {short_name}"
    else:
        title = f"{project_num} {category}: {short_name}"

    if in_codespace:
        title += " (CS)"

    return title


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    title_file = project_root / ".title"

    try:
        title = generate_title()
        title_file.write_text(title + "\n")
        print(f"Updated .title: {title}")
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
