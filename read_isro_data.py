import numpy as np
import pandas as pd
from astropy.io import fits

# The exact path to your HEL1OS science file
science_file = r"HLS_20260613_000010_43182sec_lev1_V111\2026\06\13\HLS_20260613_000010_43182sec_lev1_V111\cdte\hel1os_cdte_spectra_cdte1.fits"

try:
    with fits.open(science_file, ignore_missing_end=True) as hdul:
        print("🎉 Map Locked! Unpacking HEL1OS Science File...")
        print("-" * 50)
        
        spectrum_data = hdul[1].data
        
        # 1. Manually pull the exact columns we discovered
        time_array = spectrum_data['TSTART'] # Using TSTART as our base timestamp
        counts_matrix = spectrum_data['COUNTS']
        exposure_array = spectrum_data['EXPOSURE']
        
        print(f"-> Found {len(time_array)} raw rows of data.")
        print(f"-> Raw Counts Matrix Shape: {counts_matrix.shape}")
        
        # 2. Flatten the 511-channel matrix into a single 1D total count array
        total_counts = np.sum(counts_matrix, axis=1)
        
        # 3. Create a pristine, clean Pandas DataFrame
        df = pd.DataFrame({
            'Time_Seconds': time_array,
            'Total_Counts': total_counts,
            'Exposure': exposure_array
        })
        
        # 4. Optional but highly recommended: Calculate Counts Per Second (CPS)
        # This standardizes data if exposure times vary slightly
        df['Counts_Per_Second'] = df['Total_Counts'] / df['Exposure']

    print("\n🚀 SUCCESS! The HEL1OS time-series has been completely unlocked.")
    print("-" * 50)
    print("--- FIRST 5 ROWS OF YOUR HACKATHON DATASET ---")
    print(df.head())
    
    # 5. Save it to a clean CSV file
    df.to_csv("clean_hel1os_timeseries.csv", index=False)
    print("\n💾 Saved clean data to 'clean_hel1os_timeseries.csv'!")

except Exception as e:
    print(f"\n❌ Error processing data: {e}")