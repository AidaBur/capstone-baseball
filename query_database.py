import mysql.connector

# Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KESGK1z1meyj",
    database="baseball"
)
cursor = connection.cursor()

print("\n✔ Connected to database.\n")

while True:
    print("Welcome to the Baseball Database Query Tool!")
    print("1. View player stats with event data (JOIN)")
    print("2. Filter player stats by year")
    print("3. Exit\n")

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        year = input("Enter the year to JOIN (e.g. 2013): ")

        query = """
            SELECT ps.statistic, ps.name, ps.team, ps.value, e.date, e.description
            FROM player_stats ps
            LEFT JOIN events e ON ps.year = e.year
            WHERE ps.year = %s
        """

        try:
            cursor.execute(query, (year,))
            rows = cursor.fetchall()

            if not rows:
                print("\nNo data found for that year.\n")
            else:
                print(f"\nPlayer stats and events from {year}:\n")
                for row in rows:
                    stat, name, team, value, date, desc = row
                    print(f"Stat: {stat} | Name: {name} | Team: {team} | #: {value}")
                    if date and desc:
                        print(f"  → Event on {date}: {desc}")
                print()
        except mysql.connector.Error as err:
            print(f"Query error: {err}")

    elif choice == "2":
        year = input("Enter year to filter by (e.g. 2013): ")

        query = """
            SELECT statistic, name, team, value
            FROM player_stats
            WHERE year = %s
        """

        try:
            cursor.execute(query, (year,))
            rows = cursor.fetchall()

            if not rows:
                print("\nNo player stats found for that year.\n")
            else:
                print(f"\nTop player stats from {year}:\n")
                for row in rows:
                    stat, name, team, value = row
                    print(f"Stat: {stat} | Name: {name} | Team: {team} | #: {value}")
                print()
        except mysql.connector.Error as err:
            print(f"Query error: {err}")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please select 1, 2, or 3.\n")

cursor.close()
connection.close()
