def get_suggestion(cve_count):
    if cve_count == 0:
        return "Safe"
    elif cve_count <= 2:
        return "Update to latest version"
    else:
        return "High risk – consider replacing package"