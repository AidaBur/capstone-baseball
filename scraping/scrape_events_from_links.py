import pandas as pd
from scrape_year_events import extract_events_for_year

# Load the year links CSV
df = pd.read_csv("data/year_links.csv")

# Loop through each year and scrape data
for index, row in df.iterrows():
    year = row["Year"]
    url = row["URL"]
    print(f"Processing year {year}")
    try:
        extract_events_for_year(url, year)
    except Exception as e:
        print(f"Error processing year {year}: {e}")
