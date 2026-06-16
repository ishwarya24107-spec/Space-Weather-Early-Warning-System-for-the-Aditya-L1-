import pandas as pd
from astropy.io import fits

# 1. Direct path to your newly discovered light-curve file
solexs_lc_file = r"AL1_SLX_L1_20260613_v1.0\AL1_SLX_L1_20260613_v1.0\SDD2\AL1_SOLEXS_20260613_SDD2_L1.lc.gz"

try:
    print(f"Opening compressed SoLEXS Light Curve: {solexs_lc_file}...\n")
    
    # 2. Open the .gz file directly using astropy
    with fits.open(solexs_lc_file, ignore_missing_end=True) as hdul:
        print("🎉 SUCCESS! Connected to the underlying SoLEXS Data File.")
        print("-" * 50)
        hdul.info() # Print internal sections
        
        # 3. Pull the main data table (usually index 1 for light curves)
        data_table = hdul[1].data
        df = pd.DataFrame(data_table)
        
    print("\n--- AVAILABLE SOLEXS COLUMNS ---")
    print(df.columns.tolist())
    
    print("\n--- FIRST 5 ROWS OF RAW SOLEXS DATA ---")
    print(df.head())
    
    # 4. Save a clean copy so we can merge it later
    df.to_csv("clean_solexs_timeseries.csv", index=False)
    print("\n💾 Saved clean data to 'clean_solexs_timeseries.csv'!")

except Exception as e:
    print(f"\n❌ Error processing SoLEXS file: {e}")