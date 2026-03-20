import joblib
import numpy as np

model = joblib.load("risk_model.pkl")
scaler = joblib.load("scaler.pkl")


def get_ml_risk_analysis(cve_count, stars, open_issues, last_updated_days):
    features = np.array([[cve_count, stars, open_issues, last_updated_days]])
    scaled_features = scaler.transform(features)
    score = model.predict(scaled_features)[0]

    risk_score = int(np.clip(score, 0, 100))

    if risk_score < 30:
        status = "Low Risk"
    elif risk_score < 70:
        status = "Medium Risk"
    else:
        status = "High Risk"

    return risk_score, status
