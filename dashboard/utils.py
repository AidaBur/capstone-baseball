import os
import pandas as pd

def aggregate_event_counts():
    rows = []
    for file in os.listdir("../data"):
        if file.startswith("events_") and file.endswith(".csv"):
            year = int(file.split("_")[1].split(".")[0])
            df = pd.read_csv(f"../data/{file}")
            rows.append({"Year": year, "Event Count": len(df)})
    return pd.DataFrame(rows).sort_values("Year")

def aggregate_player_stats(stat_name):
    rows = []
    for file in os.listdir("../data"):
        if file.startswith("player_stats_") and file.endswith(".csv"):
            year = int(file.split("_")[2].split(".")[0])
            df = pd.read_csv(f"../data/{file}")
            df = df[df["Statistic"] == stat_name]
            df = df[df["#"] != "--"]
            df["#"] = pd.to_numeric(df["#"], errors="coerce")
            total = df["#"].sum()
            rows.append({"Year": year, stat_name: total})
    return pd.DataFrame(rows).sort_values("Year")
