# extract_profile.py
import netCDF4 as nc
import pandas as pd
import numpy as np
import sys
import os

def safe_read(ds, names):
    """Try reading multiple possible variable names (first that exists)."""
    if isinstance(names, str):  # if you pass a single name
        names = [names]
    for n in names:
        if n in ds.variables:
            return ds[n][:].filled(np.nan)
    return None

def decode_char_array(x):
    """If x is an array of characters (bytes), join into a string."""
    try:
        return "".join(x.astype(str)).strip()
    except Exception:
        try:
            return str(x[0])
        except Exception:
            return ""


def extract_one(nc_path, max_rows=None):

    ds = nc.Dataset(nc_path, "r")

    # Metadata
    platform_var = ds.variables.get("PLATFORM_NUMBER")
    if "PLATFORM_NUMBER" in ds.variables:
        platform = (
        "".join(p.decode("utf-8") for p in ds["PLATFORM_NUMBER"][0].data if p not in [b"--", b""])
        .strip()
    )
    else:
        platform = "unknown"


    cycle = int(ds["CYCLE_NUMBER"][0]) if "CYCLE_NUMBER" in ds.variables else -1
    lat = float(ds["LATITUDE"][0]) if "LATITUDE" in ds.variables else np.nan
    lon = float(ds["LONGITUDE"][0]) if "LONGITUDE" in ds.variables else np.nan
    time = pd.to_datetime(ds["JULD"][:], origin="1950-01-01", unit="D")[0] if "JULD" in ds.variables else None

    # Core measurements (try adjusted first, fall back to raw)
    pres = safe_read(ds, ["PRES_ADJUSTED", "PRES"])
    temp = safe_read(ds, ["TEMP_ADJUSTED", "TEMP"])
    sal  = safe_read(ds, ["PSAL_ADJUSTED", "PSAL"])

    if pres is None or temp is None:
        print("⚠️ No pres/temp in", nc_path)
        return pd.DataFrame()

    n_profiles, n_levels = pres.shape

    records = []
    for i in range(n_profiles):
        p = pres[i, :]
        t = temp[i, :] if temp is not None else np.full_like(p, np.nan)
        s = sal[i, :] if sal is not None else np.full_like(p, np.nan)

        df = pd.DataFrame({
            "platform_number": platform,
            "cycle_number": cycle,
            "time": time,
            "latitude": lat,
            "longitude": lon,
            "pressure_dbar": p.flatten(),
            "temperature_C": t.flatten(),
            "salinity_psu": s.flatten()
        }).dropna(subset=["pressure_dbar", "temperature_C"])

        if max_rows:
            df = df.head(max_rows)

        records.append(df)

    if records:
        return pd.concat(records, ignore_index=True)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_profile.py <path_to_nc> [out_csv]")
        sys.exit(1)
    nc_path = sys.argv[1]   # ✅ now it's clear this is the file path string
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(nc_path)[0] + ".csv"
    df = extract_one(nc_path)
    df.to_csv(out, index=False)
    print("Saved", out)
    print(df.head())