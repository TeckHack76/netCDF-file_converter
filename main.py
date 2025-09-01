# main.py
import argparse
import os
from download_profiles import download_file
from extract_profile import extract_one
import pandas as pd

def run_pipeline(url, out_folder="processed"):
    os.makedirs(out_folder, exist_ok=True)

    # Step 1: Download
    print(f"⬇️ Downloading {url} ...")
    local_nc = download_file(url, out_folder)

    # Step 2: Extract
    print(f"📂 Extracting {local_nc} ...")
    df = extract_one(local_nc)

    if df.empty:
        print("⚠️ No valid data extracted.")
        return

    # Step 3: Save CSV
    out_csv = os.path.splitext(local_nc)[0] + ".csv"
    df.to_csv(out_csv, index=False)
    print(f"✅ Saved {out_csv}")
    print("📊 First 5 rows:\n", df.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argo .nc → CSV Converter")
    parser.add_argument("url", help="URL of the Argo .nc file")
    parser.add_argument("--out", default="processed", help="Output folder")
    args = parser.parse_args()

    run_pipeline(args.url, args.out)
