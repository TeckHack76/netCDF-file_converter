# batch_extract.py
import glob
import os
import pandas as pd
from extract_profile import extract_one  # import function from previous file

def batch_process(nc_folder="data", out_folder="processed", max_files=None, max_rows_per_file=None):
    os.makedirs(out_folder, exist_ok=True)
    nc_files = sorted(glob.glob(os.path.join(nc_folder, "*.nc")))
    if max_files:
        nc_files = nc_files[:max_files]
    list_of_csvs = []
    for nc in nc_files:
        print("Processing:", nc)
        df = extract_one(nc, max_rows=max_rows_per_file)
        if df.empty:
            print("No rows from", nc)
            continue
        out_csv = os.path.join(out_folder, os.path.splitext(os.path.basename(nc))[0] + ".csv")
        df.to_csv(out_csv, index=False)
        list_of_csvs.append(out_csv)
    # Optionally combine
    if list_of_csvs:
        combined = pd.concat([pd.read_csv(p) for p in list_of_csvs], ignore_index=True)
        combined.to_parquet(os.path.join(out_folder, "combined.parquet"), index=False)
        combined.to_csv(os.path.join(out_folder, "combined.csv"), index=False)
        print("Saved combined.parquet and combined.csv in", out_folder)

if __name__ == "__main__":
    batch_process(nc_folder="data", out_folder="processed", max_files=10)
