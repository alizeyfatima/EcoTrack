import joblib
import numpy as np
import pandas as pd

# Load trained model
model = joblib.load("ecotrack_model.pkl")


def predict_consumption(date, wind_speed, precipitation,
                        max_temp, min_temp):

    date = pd.to_datetime(date)

    day_of_year = date.dayofyear

    # Create the same features used during training
    temp_avg = (max_temp + min_temp) / 2
    temp_range = max_temp - min_temp

    sin_day = np.sin(
        2 * np.pi * day_of_year / 365
    )

    cos_day = np.cos(
        2 * np.pi * day_of_year / 365
    )

    data = pd.DataFrame([{
        "AWND": wind_speed,
        "PRCP": precipitation,
        "TMAX": max_temp,
        "TMIN": min_temp,
        "temp_avg": temp_avg,
        "temp_range": temp_range,
        "year": date.year,
        "month": date.month,
        "sin_day": sin_day,
        "cos_day": cos_day
    }])

    prediction = model.predict(data)[0]

    return prediction