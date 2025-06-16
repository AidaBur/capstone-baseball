import pandas as pd
import os

folder_path = "data"
combined = []

for filename in os.listdir(folder_path):
    if filename.startswith("player_stats_") and filename.endswith(".csv"):
        year = filename.split("_")[-1].split(".")[0]
        df = pd.read_csv(os.path.join(folder_path, filename))

        # Remove trailing summary row if present
        df = df[df["Statistic"] != "Statistic"]

        df["Year"] = int(year)

        # Exclude rows with placeholder player names
        df = df[df["Name"] != "To Be Determined"]

        # Convert values to numeric
        def parse_number(val):
            try:
                return float(val)
            except:
                return None

        df["Value"] = df["#"].apply(parse_number)

        combined.append(df[["Year", "Statistic", "Name", "Team", "Value"]])

# Combine all years into one DataFrame
final_df = pd.concat(combined)

# Save to file
final_df.to_csv("statistics_cleaned.csv", index=False)
print("✅ Done! Saved as statistics_cleaned.csv")
