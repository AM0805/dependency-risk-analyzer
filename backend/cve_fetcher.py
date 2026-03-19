import requests


def get_cve_data(package_name):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package_name}&resultsPerPage=20"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        cve_items = data.get("vulnerabilities", [])
        
        return {
            "package": package_name,
            "cve_count": len(cve_items)
        }
    
    except Exception as e:
        return {
            "package": package_name,
            "cve_count": 0,
            "error": str(e)
        }
