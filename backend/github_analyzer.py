import requests
from datetime import datetime
from pypi_fetcher import get_repo_url


def extract_repo_name(url):
    if not url or "github.com" not in url:
        return None

    parts = url.split("github.com/")
    repo_part = parts[1].strip("/")
    repo_parts = repo_part.split("/")

    if len(repo_parts) < 2:
        return None

    return repo_parts[0] + "/" + repo_parts[1]


def get_github_data(package_name):

    repo_url = get_repo_url(package_name)
    repo = extract_repo_name(repo_url)
    # fallback mapping for popular packages
    common_map = {
        "numpy": "numpy/numpy",
        "pandas": "pandas-dev/pandas",
        "django": "django/django",
        "flask": "pallets/flask",
        "requests": "psf/requests",
        "fastapi": "tiangolo/fastapi"
    }

    if not repo:
        repo = common_map.get(package_name)

    print("Repo URL:", repo_url)
    print("Repo:", repo)

    if not repo:
        return {"stars": 0, "open_issues": 0, "last_updated_days": 999}

    url = f"https://api.github.com/repos/{repo}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "test-agent"
    }

    response = requests.get(url, headers=headers)

    print("GitHub API URL:", url)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.text[:200])  # first 200 chars

    if response.status_code != 200:
        return {"stars": 0, "open_issues": 0, "last_updated_days": 999}

    data = response.json()

    return {
        "stars": data.get("stargazers_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "last_updated_days": 0
    }