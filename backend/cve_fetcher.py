import requests
import time
from services.cache import get_from_cache, set_cache

def get_cve_data(package_name):
    key = f"cve:{package_name}"
    cached = get_from_cache(key)
    if cached:
        return cached

    print(f"CACHE MISS: {key}")
    # Fetching up to 20 vulnerabilities to calculate average impact
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package_name}&resultsPerPage=20"
    
    # Retry up to 3 times — NVD rate-limits unauthenticated requests
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 429:
                time.sleep(6 * (attempt + 1))  # back off: 6s, 12s, 18s
                continue
            data = response.json()
            break
        except Exception:
            if attempt == 2:
                return {"package": package_name, "cve_count": 0, "avg_cvss": 0}
            time.sleep(3)
    else:
        return {"package": package_name, "cve_count": 0, "avg_cvss": 0}

    try:
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        
        scores = []
        for v in vulnerabilities:
            metrics = v.get("cve", {}).get("metrics", {})
            cvss_data = metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", [])
            if cvss_data:
                score = cvss_data[0].get("cvssData", {}).get("baseScore")
                if score:
                    scores.append(score)
        
        result = {
            "package": package_name,
            "cve_count": len(vulnerabilities),
            "avg_cvss": sum(scores) / len(scores) if scores else 0
        }
    
    except Exception:
        result = {
            "package": package_name,
            "cve_count": 0,
            "avg_cvss": 0
        }

    set_cache(key, result)
    return result