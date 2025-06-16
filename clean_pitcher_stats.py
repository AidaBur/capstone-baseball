import pandas as pd
import os

folder_path = "data"
combined = []

for filename in os.listdir(folder_path):
    if filename.startswith("pitcher_stats_") and filename.endswith(".csv"):
        year = filename.split("_")[-1].split(".")[0]
        df = pd.read_csv(os.path.join(folder_path, filename))

        # Remove trailing summary row if present
        df = df[df["Statistic"] != "Statistic"]

        df["Year"] = int(year)
        df = df[df["Name"] != "To Be Determined"]

        def parse_number(val):
            try:
                return float(val)
            except:
                return None

        df["Value"] = df["#"].apply(parse_number)
        combined.append(df[["Year", "Statistic", "Name", "Team", "Value"]])

final_df = pd.concat(combined)
final_df.to_csv("data/pitcher_stats_cleaned.csv", index=False)
print("✅ Saved as data/pitcher_stats_cleaned.csv")
