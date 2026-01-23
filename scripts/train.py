import json
import joblib
import os
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Ensure output folders exist
os.makedirs("Model", exist_ok=True)
os.makedirs("Metrics", exist_ok=True)

# Load dataset
X, y = load_wine(return_X_y=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=1.0))
])

# Train model
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

metrics = {
    "mse": mse,
    "r2": r2
}

# Save artifacts
joblib.dump(pipeline, "Model/model.pkl")
with open("Metrics/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# Print for CI logs
print("MSE:", mse)
print("R2:", r2)
