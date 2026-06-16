import pandas as pd
import matplotlib.pyplot as plt

# 1. Load your master dataset
df = pd.read_csv("aditya_l1_master_dataset.csv", parse_dates=['datetime'])
df.set_index('datetime', inplace=True)

# 2. Initialize a dual-axis plot
fig, ax1 = plt.subplots(figsize=(14, 7))

# 3. Plot Soft X-Rays (SoLEXS) on the primary Y-axis (Left)
color = 'royalblue'
ax1.set_xlabel('Time of Observation (UTC)', fontsize=12, fontweight='bold')
ax1.set_ylabel('SoLEXS Soft X-Rays (Avg Counts)', color=color, fontsize=12, fontweight='bold')
ax1.plot(df.index, df['soft_xray_solexs'], color=color, linewidth=2, label='SoLEXS (Soft X-Ray)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

# 4. Instantiate a second Y-axis that shares the same X-axis
ax2 = ax1.twinx()  

# 5. Plot Hard X-Rays (HEL1OS) on the secondary Y-axis (Right)
color = 'crimson'
ax2.set_ylabel('HEL1OS Hard X-Rays (Avg Counts)', color=color, fontsize=12, fontweight='bold')
ax2.plot(df.index, df['hard_xray_hel1os'], color=color, linewidth=1.5, alpha=0.8, label='HEL1OS (Hard X-Ray)')
ax2.tick_params(axis='y', labelcolor=color)

# 6. Title and layout tweaks
plt.title('Aditya-L1 Coordinated Solar Observation (2026-06-13)\nSynchronized SoLEXS & HEL1OS Time-Series', fontsize=14, fontweight='bold')
fig.tight_layout()

print("📊 Generating your multi-instrument solar plot... look for the popup window!")
plt.show()