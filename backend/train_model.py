import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

FEATURES = ["cve_count", "avg_cvss", "stars", "open_issues", "last_updated_days"]
TARGET = "risk_score"


def load_data(path="training_data.csv"):
    df = pd.read_csv(path)
    df = df.dropna(subset=FEATURES + [TARGET])
    return df[FEATURES], df[TARGET]


def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"R²:   {r2_score(y_test, y_pred):.4f}")

    return model, scaler


def save(model, scaler):
    joblib.dump(model, "risk_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("Saved risk_model.pkl and scaler.pkl")


if __name__ == "__main__":
    X, y = load_data()
    print(f"Training on {len(X)} samples")
    model, scaler = train(X, y)
    save(model, scaler)
