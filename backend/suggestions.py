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