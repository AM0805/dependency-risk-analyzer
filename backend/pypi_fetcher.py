import requests

def get_repo_url(package_name):
    
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        info = data.get("info", {})
        project_urls = info.get("project_urls", {})
        
        repo_url = (
            project_urls.get("Source")
            or project_urls.get("Homepage")
            or project_urls.get("Repository")
            or info.get("home_page")
            or ""
        )
        
        return repo_url
    
    except:
        return ""