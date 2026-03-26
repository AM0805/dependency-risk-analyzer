import requests

def get_cve_data(package_name):
    # Fetching up to 20 vulnerabilities to calculate average impact
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package_name}&resultsPerPage=20"
    
    try:
        response = requests.get(url, timeout=10)
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