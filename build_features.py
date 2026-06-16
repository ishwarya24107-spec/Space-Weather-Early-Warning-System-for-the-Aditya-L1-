import pandas as pd

print("🔄 Loading master dataset...")
# FIXED: Changed 'index_index' to 'index_col' so Pandas reads it correctly!
df = pd.read_csv("aditya_l1_master_dataset.csv", parse_dates=['datetime'], index_col='datetime')

print("📈 Calculating Rate of Change (Slopes)...")
# Sudden jumps in slope indicate the start of an explosive flare phase
df['hel_slope'] = df['hard_xray_hel1os'].diff()
df['sol_slope'] = df['soft_xray_solexs'].diff()

print("🧹 Calculating Rolling Statistical Metrics...")
# Smooth out background noise using a 5-minute moving average
df['sol_rolling_mean_5min'] = df['soft_xray_solexs'].rolling(window=5).mean()
# Measure volatility/spikes using a 5-minute rolling standard deviation
df['hel_rolling_std_5min'] = df['hard_xray_hel1os'].rolling(window=5).std()

# Drop the first few rows because rolling calculations need at least 5 rows to start
df_cleaned = df.dropna()

print("-" * 60)
print(f"Features successfully engineered! New matrix shape: {df_cleaned.shape}")
print("-" * 60)
print(df_cleaned[['hard_xray_hel1os', 'hel_slope', 'sol_rolling_mean_5min']].head())
print("-" * 60)

# Save your new feature matrix for your ML model
df_cleaned.to_csv("aditya_l1_features.csv")
print("💾 Saved engineered feature matrix to 'aditya_l1_features.csv'!")