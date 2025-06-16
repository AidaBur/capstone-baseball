import pandas as pd
import sqlite3

conn = sqlite3.connect("baseball.db")

try:
    player_df = pd.read_csv("dashboard/statistics_cleaned.csv")
    print("player_df loaded:", player_df.shape)
    player_df.to_sql("player_stats", conn, if_exists="replace", index=False)
except Exception as e:
    print("Error loading player_df:", e)

try:
    pitcher_df = pd.read_csv("dashboard/pitcher_stats_cleaned.csv")
    print("pitcher_df loaded:", pitcher_df.shape)
    pitcher_df.to_sql("pitcher_stats", conn, if_exists="replace", index=False)
except Exception as e:
    print("Error loading pitcher_df:", e)

try:
    events_df = pd.read_csv("dashboard/events_cleaned.csv")
    print("events_df loaded:", events_df.shape)
    events_df.to_sql("events", conn, if_exists="replace", index=False)
except Exception as e:
    print("Error loading events_df:", e)

print("\n📋 Current tables in baseball.db:")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(" -", table[0])

conn.close()
