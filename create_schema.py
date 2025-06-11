import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KESGK1z1meyj",
)
cursor = connection.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS baseball")
cursor.execute("USE baseball")

# Create player_stats table
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    statistic VARCHAR(255),
    name VARCHAR(255),
    team VARCHAR(100),
    value VARCHAR(50)
)
""")

# Create pitcher_stats table
cursor.execute("""
CREATE TABLE IF NOT EXISTS pitcher_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    statistic VARCHAR(255),
    name VARCHAR(255),
    team VARCHAR(100),
    value VARCHAR(50)
)
""")

# Create league_summary table
cursor.execute("""
CREATE TABLE IF NOT EXISTS league_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section VARCHAR(255),
    content TEXT,
    year INT
)
""")

# Create events table
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(100),
    description TEXT,
    year INT
)
""")

print("✔ Tables created successfully.")
cursor.close()
connection.close()
