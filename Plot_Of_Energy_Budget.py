import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
url = "https://earthenergyflows.com/04-2000-03-2024.xlsx"
df = pd.read_excel(url, sheet_name=0, skiprows=1)

# Combine year/month into a datetime
df["Date"] = pd.to_datetime(df["Year"].astype(int).astype(str) + "-" + df["Month"].astype(int).astype(str))

# Net TOA flux
net = df["Net TOA"]  # check exact column name; might differ

# Compute 12-month running mean
net_rolling12 = net.rolling(window=12, center=True).mean()

# Fit a linear trend
# We'll use a simple least-squares fit to the rolling mean (ignoring NaNs)
mask = ~np.isnan(net_rolling12)
times = (df["Date"][mask] - df["Date"][mask].min()).dt.days
# convert time to years for trend slope
years = times / 365.25
slope, intercept = np.polyfit(years, net_rolling12[mask], 1)

# Create plot
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], net, color="lightgray", label="Monthly Net TOA")
plt.plot(df["Date"], net_rolling12, color="blue", label="12‑month mean")
plt.plot(df["Date"][mask], intercept + slope * years, color="red", linestyle="--", label=f"Trend ≈ {slope*365.25:.3f} W/m² per year")

plt.xlabel("Date")
plt.ylabel("Net TOA Flux (W/m²)")
plt.title("CERES EBAF Edition 4.2 – Global Net TOA Flux (2000–2024)")
plt.legend()
plt.grid(True)
plt.show()

