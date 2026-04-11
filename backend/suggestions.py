import requests
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_pypi_keywords(package_name):
    """Extract keywords and classifiers from PyPI to describe what the package does."""
    try:
        res = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=8)
        if res.status_code != 200:
            return []
        info = res.json().get("info", {})

        keywords = []

        # Pull explicit keywords field
        raw_keywords = info.get("keywords") or ""
        keywords += [k.strip() for k in raw_keywords.replace(",", " ").split() if k.strip()]

        # Pull meaningful topic classifiers (e.g. "Scientific/Engineering :: Machine Learning")
        for clf in info.get("classifiers", []):
            if clf.startswith("Topic ::"):
                parts = clf.split(" :: ")
                if len(parts) >= 3:
                    keywords.append(parts[-1].lower().replace(" ", "-"))

        return list(set(keywords))[:5]  # cap at 5 to keep search focused
    except Exception:
        return []


def search_github_alternatives(package_name, keywords):
    """Use GitHub Search API to find Python packages related to the same keywords."""
    if not keywords:
        keywords = [package_name]

    query = f"{' '.join(keywords[:3])} language:python topic:python"
    url = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dependency-risk-analyzer",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        res = requests.get(url, headers=headers, params={"q": query, "sort": "stars", "per_page": 15}, timeout=8)
        if res.status_code != 200:
            return []

        candidates = []
        for repo in res.json().get("items", []):
            # Use the repo name as-is and also try with hyphens (PyPI convention)
            raw_name = repo.get("name", "")
            pypi_name = raw_name.lower()
            if pypi_name == package_name.lower() or len(pypi_name) > 40:
                continue
            # Verify it actually exists on PyPI before adding
            if _exists_on_pypi(pypi_name):
                candidates.append(pypi_name)
            elif _exists_on_pypi(raw_name.lower().replace("_", "-")):
                candidates.append(raw_name.lower().replace("_", "-"))
            if len(candidates) >= 6:
                break

        return candidates
    except Exception:
        return []


def _exists_on_pypi(package_name):
    """Quick check if a package exists on PyPI."""
    try:
        res = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        return res.status_code == 200
    except Exception:
        return False


def get_alternatives(package_name):
    """Find alternative package names using PyPI keywords + GitHub Search."""
    keywords = get_pypi_keywords(package_name)
    return search_github_alternatives(package_name, keywords)


def get_suggestion(cve_count, stars, last_updated_days):
    if cve_count == 0 and last_updated_days < 30:
        return "Safe"
    if stars > 5000 and last_updated_days < 90:
        return "Actively maintained"
    if last_updated_days > 180:
        return "Outdated – risky"
    if cve_count > 5:
        return "High risk – consider replacing"
    return "Moderate risk"
