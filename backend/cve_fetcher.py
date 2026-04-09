import requests
import time

def get_cve_data(package_name):
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
            # This is the part that extracts the actual score
            cvss_data = metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", [])
            if cvss_data:
                score = cvss_data[0].get("cvssData", {}).get("baseScore")
                if score:
                    scores.append(score)
        
        return {
            "package": package_name,
            "cve_count": len(vulnerabilities),
            "avg_cvss": sum(scores) / len(scores) if scores else 0 # THIS KEY IS MISSING
        }
    
    except Exception:
        return {
            "package": package_name,
            "cve_count": 0,
            "avg_cvss": 0 # Default to 0 if the API fails
        }