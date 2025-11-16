import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# 1. Load CERES EBAF data
# -------------------------------
# Replace with the actual path to the downloaded Excel file
file_path = "04-2000-03-2024.xlsx"

# Load the sheet (usually first sheet)
df = pd.read_excel(file_path, sheet_name=0, skiprows=1)

# Combine year and month into datetime
df["Date"] = pd.to_datetime(df["Year"].astype(int).astype(str) + "-" + df["Month"].astype(int).astype(str))

# Column containing Net TOA flux (check sheet for exact name)
net = df["Net TOA"]  # adjust if necessary

# -------------------------------
# 2. Compute 12-month rolling mean
# -------------------------------
net_rolling12 = net.rolling(window=12, center=True).mean()

# -------------------------------
# 3. Fit linear trend
# -------------------------------
mask = ~np.isnan(net_rolling12)
times = (df["Date"][mask] - df["Date"][mask].min()).dt.days
years = times / 365.25  # convert to years
slope, intercept = np.polyfit(years, net_rolling12[mask], 1)

# -------------------------------
# 4. Plot
# -------------------------------
plt.figure(figsize=(14, 7))
plt.pl

