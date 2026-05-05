"""
ML-Based Traffic Prediction — CSE112 Bonus
Uses scikit-learn to predict congestion levels from temporal patterns.
"""

import json
import math
import random

# ============================================================
# SYNTHETIC TRAINING DATA from provided traffic patterns
# ============================================================

TRAFFIC_DATA = [
    # road_id, hour, day_type(0=weekday,1=weekend), flow, capacity
    {"road": "1-3",   "morning": 2800, "afternoon": 1500, "evening": 2600, "night": 800,  "cap": 3000},
    {"road": "2-5",   "morning": 3000, "afternoon": 1600, "evening": 2800, "night": 650,  "cap": 3200},
    {"road": "3-5",   "morning": 3200, "afternoon": 1700, "evening": 3100, "night": 800,  "cap": 3500},
    {"road": "4-2",   "morning": 3600, "afternoon": 1800, "evening": 3300, "night": 750,  "cap": 3800},
    {"road": "7-8",   "morning": 3200, "afternoon": 1700, "evening": 3000, "night": 700,  "cap": 3500},
    {"road": "13-4",  "morning": 3800, "afternoon": 2000, "evening": 3500, "night": 800,  "cap": 4000},
    {"road": "14-13", "morning": 3600, "afternoon": 1900, "evening": 3300, "night": 750,  "cap": 3800},
    {"road": "F1-5",  "morning": 3300, "afternoon": 2200, "evening": 3100, "night": 1200, "cap": 3500},
    {"road": "F1-2",  "morning": 3000, "afternoon": 2000, "evening": 2800, "night": 1100, "cap": 3200},
    {"road": "3-6",   "morning": 1800, "afternoon": 1400, "evening": 1900, "night": 500,  "cap": 2000},
    {"road": "6-9",   "morning": 1700, "afternoon": 1300, "evening": 1800, "night": 450,  "cap": 1800},
    {"road": "9-10",  "morning": 1800, "afternoon": 1200, "evening": 1700, "night": 400,  "cap": 1900},
    {"road": "8-12",  "morning": 2400, "afternoon": 1300, "evening": 2200, "night": 500,  "cap": 2600},
    {"road": "5-11",  "morning": 2900, "afternoon": 1500, "evening": 2700, "night": 650,  "cap": 3100},
]

def generate_training_samples():
    """Generate hourly samples from daily patterns."""
    X, y = [], []
    period_map = {
        range(6, 10):  "morning",
        range(10, 16): "afternoon",
        range(16, 21): "evening",
    }
    for row in TRAFFIC_DATA:
        cap = row["cap"]
        for road_idx, road_id in enumerate([row["road"]]):
            for hour in range(24):
                # Determine period
                period = "night"
                for hour_range, p in period_map.items():
                    if hour in hour_range:
                        period = p
                        break

                flow = row[period]
                # Add synthetic variation (±15%)
                for day_type in [0, 1]:
                    multiplier = 0.85 if day_type == 1 else 1.0  # weekends less traffic
                    noisy_flow = flow * multiplier * (1 + (hash(f"{road_id}{hour}{day_type}") % 30 - 15) / 100)
                    congestion = min(noisy_flow / cap, 1.0)
                    # Features: hour, day_type, capacity, hour_sin, hour_cos
                    hour_sin = math.sin(2 * math.pi * hour / 24)
                    hour_cos = math.cos(2 * math.pi * hour / 24)
                    X.append([hour, day_type, cap / 4000, hour_sin, hour_cos, road_idx / len(TRAFFIC_DATA)])
                    y.append(congestion)
    return X, y


class LinearRegressionModel:
    """Simple linear regression — no external dependencies needed."""
    def __init__(self):
        self.weights = None
        self.bias = 0
        self.mean_X = None
        self.std_X = None

    def _normalize(self, X):
        return [[(x - m) / (s if s > 0 else 1) for x, m, s in zip(row, self.mean_X, self.std_X)] for row in X]

    def fit(self, X, y, lr=0.01, epochs=500):
        n, p = len(X), len(X[0])
        self.mean_X = [sum(row[j] for row in X) / n for j in range(p)]
        self.std_X  = [math.sqrt(sum((row[j] - self.mean_X[j])**2 for row in X) / n) for j in range(p)]
        Xn = self._normalize(X)
        self.weights = [0.0] * p
        self.bias = 0.0
        for _ in range(epochs):
            preds = [sum(w * x for w, x in zip(self.weights, row)) + self.bias for row in Xn]
            errors = [p - t for p, t in zip(preds, y)]
            grad_w = [sum(errors[i] * Xn[i][j] for i in range(n)) / n for j in range(p)]
            grad_b = sum(errors) / n
            self.weights = [w - lr * g for w, g in zip(self.weights, grad_w)]
            self.bias -= lr * grad_b
        return self

    def predict(self, X):
        Xn = self._normalize(X)
        return [max(0, min(1, sum(w * x for w, x in zip(self.weights, row)) + self.bias)) for row in Xn]

    def score(self, X, y):
        preds = self.predict(X)
        ss_res = sum((p - t)**2 for p, t in zip(preds, y))
        mean_y = sum(y) / len(y)
        ss_tot = sum((t - mean_y)**2 for t in y)
        return 1 - ss_res / ss_tot if ss_tot > 0 else 0


def train_traffic_model():
    """Train and return the ML model with performance metrics."""
    X, y = generate_training_samples()
    # Split 80/20
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LinearRegressionModel()
    model.fit(X_train, y_train)
    train_r2 = model.score(X_train, y_train)
    test_r2  = model.score(X_test, y_test)

    return model, {"train_r2": round(train_r2, 4), "test_r2": round(test_r2, 4),
                   "samples": len(X), "features": 6}


def predict_congestion(hour, day_type=0, capacity=3000, road_idx=0, model=None):
    """Predict congestion ratio for given conditions."""
    if model is None:
        model, _ = train_traffic_model()
    hour_sin = math.sin(2 * math.pi * hour / 24)
    hour_cos = math.cos(2 * math.pi * hour / 24)
    features = [[hour, day_type, capacity / 4000, hour_sin, hour_cos, road_idx / len(TRAFFIC_DATA)]]
    pred = model.predict(features)[0]
    level = "CRITICAL" if pred > 0.85 else "HIGH" if pred > 0.65 else "MODERATE" if pred > 0.45 else "LOW"
    return {"congestion_ratio": round(pred, 3), "level": level, "hour": hour}


def get_daily_prediction(road_name="1-3", day_type=0, model=None):
    """Get 24-hour congestion prediction for a road."""
    if model is None:
        model, _ = train_traffic_model()
    road_names = [r["road"] for r in TRAFFIC_DATA]
    road_idx = road_names.index(road_name) if road_name in road_names else 0
    cap = TRAFFIC_DATA[road_idx]["cap"]
    predictions = []
    for hour in range(24):
        p = predict_congestion(hour, day_type, cap, road_idx, model)
        predictions.append(p)
    return predictions


if __name__ == "__main__":
    print("Training ML Traffic Prediction Model...")
    model, metrics = train_traffic_model()
    print(f"Train R²: {metrics['train_r2']} | Test R²: {metrics['test_r2']}")
    print(f"Training samples: {metrics['samples']}")
    pred = predict_congestion(8, 0, 3000, 0, model)
    print(f"8AM Weekday prediction: {pred}")
