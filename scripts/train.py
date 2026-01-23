import json
import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Ensure output folders exist
os.makedirs("Model", exist_ok=True)
os.makedirs("Metrics", exist_ok=True)

# Load Wine Quality dataset (RED)
df = pd.read_csv(
    "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    sep=";"
)

X = df.drop("quality", axis=1)
y = df["quality"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=1.0))
])

# Train
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

metrics = {"mse": mse, "r2": r2}

# Save artifacts
joblib.dump(pipeline, "Model/model.pkl")

with open("Metrics/metrics.json", "w") as f:
    json.dump(metrics, f)

print("MSE:", mse)
print("R2:", r2)
