import pandas as pd
import os

folder_path = "data"
combined = []

for filename in os.listdir(folder_path):
    if filename.startswith("events_") and filename.endswith(".csv"):
        year = filename.split("_")[-1].split(".")[0]
        df = pd.read_csv(os.path.join(folder_path, filename))
        df["Year"] = int(year)
        combined.append(df[["Date", "Description", "Year"]])

final_df = pd.concat(combined)
final_df.to_csv("data/events_cleaned.csv", index=False)
print("✅ Saved as data/events_cleaned.csv")
