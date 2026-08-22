import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

df = pd.read_csv("electricity_consumption_based_weather_dataset.csv")

print("Dataset loaded!")
print("Rows:", len(df))

# DATE FEATURES
df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_of_year"] = df["date"].dt.dayofyear

# Seasonal cyclical features
import numpy as np

df["sin_day"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
df["cos_day"] = np.cos(2 * np.pi * df["day_of_year"] / 365)

# Temperature features
df["temp_avg"] = (df["TMAX"] + df["TMIN"]) / 2
df["temp_range"] = df["TMAX"] - df["TMIN"]

df = df.dropna()

features = [
    "AWND",
    "PRCP",
    "TMAX",
    "TMIN",
    "temp_avg",
    "temp_range",
    "year",
    "month",
    "sin_day",
    "cos_day"
]

X = df[features]
y = df["daily_consumption"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_predictions)
rf_rmse = mean_squared_error(y_test, rf_predictions) ** 0.5
rf_r2 = r2_score(y_test, rf_predictions)

# GRADIENT BOOSTING
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

gb_model.fit(X_train, y_train)

gb_predictions = gb_model.predict(X_test)

gb_mae = mean_absolute_error(y_test, gb_predictions)
gb_rmse = mean_squared_error(y_test, gb_predictions) ** 0.5
gb_r2 = r2_score(y_test, gb_predictions)

# -----------------------------
# COMPARE MODELS
# -----------------------------

print("\n====================================")
print("        MODEL COMPARISON")
print("====================================")

print("\nRandom Forest")
print("MAE :", round(rf_mae, 2))
print("RMSE:", round(rf_rmse, 2))
print("R²  :", round(rf_r2, 4))

print("\nGradient Boosting")
print("MAE :", round(gb_mae, 2))
print("RMSE:", round(gb_rmse, 2))
print("R²  :", round(gb_r2, 4))

# SELECT BEST MODEL
if gb_r2 > rf_r2:
    best_model = gb_model
    best_name = "Gradient Boosting"
    best_r2 = gb_r2
else:
    best_model = rf_model
    best_name = "Random Forest"
    best_r2 = rf_r2

print("BEST MODEL")
print("Selected:", best_name)
print("R²:", round(best_r2, 4))


# SAVE MODEL
joblib.dump(best_model, "ecotrack_model.pkl")

print("\nModel saved as ecotrack_model.pkl")