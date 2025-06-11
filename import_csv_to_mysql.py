import os
import csv
import mysql.connector

# DB config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "KESGK1z1meyj",
    "database": "baseball"
}

# Connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

data_dir = "data"
files = os.listdir(data_dir)

for filename in sorted(files):
    filepath = os.path.join(data_dir, filename)

    if not filename.endswith(".csv"):
        continue

    print(f"Importing {filename}...")

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        try:
            header = next(reader)
        except StopIteration:
            print("⚠ File is empty, skipping.")
            continue

        inserted_rows = 0

        for row in reader:
            try:
                if filename.startswith("player_stats"):
                    cursor.execute("""
                        INSERT INTO player_stats (year, statistic, name, team, value)
                        VALUES (%s, %s, %s, %s, %s)
                    """, row)
                elif filename.startswith("pitcher_stats"):
                    cursor.execute("""
                        INSERT INTO pitcher_stats (year, statistic, name, team, value)
                        VALUES (%s, %s, %s, %s, %s)
                    """, row)
                elif filename.startswith("league_summary"):
                    cursor.execute("""
                        INSERT INTO league_summary (section, content, year)
                        VALUES (%s, %s, %s)
                    """, row)
                elif filename.startswith("events"):
                    cursor.execute("""
                        INSERT INTO events (date, description, year)
                        VALUES (%s, %s, %s)
                    """, row)
                inserted_rows += 1
            except Exception as e:
                print(f"Failed to insert row: {row} — {e}")

        connection.commit()
        print(f"{inserted_rows} rows inserted from {filename}.")

cursor.close()
connection.close()
