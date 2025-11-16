import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel data
url = "https://earthenergyflows.com/04-2000-03-2024.xlsx"
df = pd.read_excel(url, sheet_name=0, skiprows=1)

# Inspect the columns
print(df.head())

# Suppose the net flux column is named "Net TOA" (check your sheet)
# Create a time axis
df["Date"] = pd.to_datetime(df["Year"].astype(int).astype(str) + "-" + df["Month"].astype(int).astype(str))

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["Net TOA"], label="Net TOA Flux (W/m²)")
plt.xlabel("Year")
plt.ylabel("Net TOA Flux (W/m²)")
plt.title("CERES EBAF – Global Net Energy Imbalance (April 2000 - March 2024)")
plt.grid(True)
plt.legend()
plt.show()

