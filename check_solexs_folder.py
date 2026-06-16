import os
from astropy.io import fits

# 1. Get the exact folder where this Python script is running
current_folder = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
print(f"📍 Script is currently running inside: {current_folder}\n")

# 2. Look around the current folder to see what is actually there
all_items = os.listdir(current_folder)
print("Items found right next to this script:")
for item in all_items:
    print(f" -> {item}")
print("-" * 60)

# 3. Try to automatically detect the SoLEXS folder name even if the spelling is slightly different
solexs_folder = None
for item in all_items:
    if "slx" in item.lower() or "solexs" in item.lower():
        # Check if it's a directory or a compressed file
        if os.path.isdir(os.path.join(current_folder, item)):
            solexs_folder = item
            break

# 4. If found, let's search deep inside it for .fits files
if solexs_folder:
    print(f"🎯 Auto-Detected SoLEXS Folder: '{solexs_folder}'\n")
    print(f"Searching deep inside it for science files...")
    
    solexs_fits = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(current_folder, solexs_folder)):
        for filename in filenames:
            if filename.endswith('.fits') or filename.endswith('.fits.gz'):
                solexs_fits.append(os.path.join(dirpath, filename))
                
    print(f"Found {len(solexs_fits)} .fits files inside!")
    for i, path in enumerate(solexs_fits):
        print(f" [{i}] {os.path.basename(path)}")
else:
    print("❌ Could not find any folder with 'SLX' or 'SoLEXS' next to this script.")
    print("👉 Action: Move your downloaded SoLEXS folder into the exact same folder as this script!")