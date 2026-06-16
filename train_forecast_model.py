import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

print("🔄 Loading engineered features...")
df = pd.read_csv("aditya_l1_features.csv", parse_dates=['datetime'], index_col='datetime')

# 1. CREATE THE TARGET VARIABLE (10-Minute Shift)
# We want to use CURRENT features to predict the soft X-ray value 10 minutes from now
df['target_10min_future'] = df['soft_xray_solexs'].shift(-10)
df_ml = df.dropna() # Remove the last 10 rows because they don't have a future target yet

# 2. DEFINE FEATURES (X) AND TARGET (y)
feature_cols = ['hard_xray_hel1os', 'soft_xray_solexs', 'hel_slope', 'sol_slope', 'sol_rolling_mean_5min', 'hel_rolling_std_5min']
X = df_ml[feature_cols]
y = df_ml['target_10min_future']

# 3. SPLIT DATA (Chronological split for time-series, NEVER random shuffle!)
# We use the first 70% of the day for training, and reserve the remaining 30% for testing
split_idx = int(len(X) * 0.70)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"📊 Training rows: {len(X_train)} | Testing rows: {len(X_test)}")

# 4. INITIALIZE AND TRAIN THE ML MODEL
print("🤖 Training Random Forest Regressor...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. GENERATE PREDICTIONS
print("🔮 Forecasting 10 minutes into the future...")
y_pred = model.predict(X_test)

# Convert predictions back to a Series with matching time indexes for easy plotting
predictions_df = pd.DataFrame(index=y_test.index)
predictions_df['Actual_Future_Value'] = y_test
predictions_df['Predicted_Future_Value'] = y_pred

# 6. EVALUATE PERFORMANCE METRICS
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print("\n📋 MODEL PERFORMANCE METRICS:")
print("-" * 40)
print(f"-> Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"-> R² Score (Variance Explained): {r2:.4f} (Target: Closer to 1.0 is perfect)")
print("-" * 40)

# 7. PLOT THE PREDICTIONS VS ACTUAL DATA
plt.figure(figsize=(14, 6))
plt.plot(predictions_df.index, predictions_df['Actual_Future_Value'], label='Actual Sun Behavior', color='royalblue', linewidth=2)
plt.plot(predictions_df.index, predictions_df['Predicted_Future_Value'], label='Model 10-Min Forecast', color='orange', linestyle='--', linewidth=2)
plt.title("Aditya-L1 Solar Flare Forecasting Model (10-Minute Advance Horizon)", fontsize=14, fontweight='bold')
plt.xlabel("Time (UTC)", fontsize=12)
plt.ylabel("Soft X-Ray Flux Intensity", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

print("📊 Drawing forecast comparison graph...")
plt.show()