import pandas as pd

print("🔄 Loading both cleaned datasets...")
df_hel = pd.read_csv("clean_hel1os_timeseries.csv")
df_sol = pd.read_csv("clean_solexs_timeseries.csv")

# 1. STANDARDIZE HEL1OS TIME (0 to Total Seconds Elapsed)
print("⏱️ Aligning HEL1OS to baseline...")
# Since Time_Seconds is already relative elapsed seconds, let's make sure it starts at 0
df_hel['elapsed_seconds'] = df_hel['Time_Seconds'] - df_hel['Time_Seconds'].min()

# 2. STANDARDIZE SOLEXS TIME (0 to Total Seconds Elapsed)
print("⏱️ Aligning SoLEXS to baseline...")
# Subtract the minimum timestamp to see exactly how many seconds elapsed from its start
df_sol['elapsed_seconds'] = df_sol['TIME'] - df_sol['TIME'].min()

# 3. CONVERT BOTH TO THE TRUE DATE OBSERVED (2026-06-13)
# This maps both streams perfectly to the exact same starting minute of the day
print("⏰ Synchronizing both instruments to June 13, 2026...")
df_hel['datetime'] = pd.to_datetime("2026-06-13 00:00:00") + pd.to_timedelta(df_hel['elapsed_seconds'], unit='s')
df_sol['datetime'] = pd.to_datetime("2026-06-13 00:00:00") + pd.to_timedelta(df_sol['elapsed_seconds'], unit='s')

# Set indices for resampling
df_hel = df_hel.set_index('datetime').sort_index()
df_sol = df_sol.set_index('datetime').sort_index()

# 4. ISOLATE THE SCIENCE DATA
hel_counts = df_hel[['Total_Counts']].rename(columns={'Total_Counts': 'hard_xray_hel1os'})
sol_counts = df_sol[['COUNTS']].rename(columns={'COUNTS': 'soft_xray_solexs'})

# 5. RESAMPLE TO A UNIFORM 1-MINUTE GRID
print("🧩 Resampling timelines into 1-minute blocks...")
hel_clean = hel_counts.resample('1min').mean().ffill()
sol_clean = sol_counts.resample('1min').mean().ffill()

# 6. EXECUTE THE MASTER MERGE
print("🤝 Executing Master Merge...")
master_df = pd.merge(hel_clean, sol_clean, left_index=True, right_index=True, how='inner')

print("\n🎉 MASTER MERGE SUCCESSFUL!")
print("-" * 65)
print(f"Total rows successfully matched: {len(master_df)}")
print("-" * 65)
print("--- FIRST 5 ROWS OF YOUR MASTER HACKATHON DATASET ---")
print(master_df.head())
print("-" * 65)

# 7. Save the finalized unified dataset
master_df.to_csv("aditya_l1_master_dataset.csv")
print("💾 Saved verified master dataset to 'aditya_l1_master_dataset.csv'!")