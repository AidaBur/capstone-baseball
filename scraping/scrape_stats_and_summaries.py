from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# Set up Selenium WebDriver with custom user-agent to mimic a real browser
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/2025.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Directory to save output files
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Loop through a range of years to scrape each year's data
for year in range(1880, 2026):  # You can adjust the range
    print(f"Processing year {year}")
    url = f"https://www.baseball-almanac.com/yearly/yr{year}n.shtml"
    driver.get(url)
    time.sleep(1.5)  # Let the page load

    # 1. Extract league summary text sections
    try:
        summary_sections = []
        headers = driver.find_elements(By.TAG_NAME, "b")
        for header in headers:
            text = header.text.strip()
            if text in ["In the American League…", "In the National League…", "Around the League…"]:
                # Get the full parent element text and remove the header
                parent = header.find_element(By.XPATH, "./parent::*")
                paragraph = parent.text.replace(text, "").strip()
                summary_sections.append({"Section": text, "Content": paragraph})

        # Save to CSV if any summary was found
        if summary_sections:
            summary_df = pd.DataFrame(summary_sections)
            summary_df.to_csv(f"{output_dir}/league_summary_{year}.csv", index=False)
            print(f"Saved: league_summary_{year}.csv")
        else:
            print("No league summary found.")
    except Exception as e:
        print(f"Error saving summary for {year}: {e}")

    # 2. Extract player statistics table
    try:
        player_table = driver.find_element(By.XPATH, f"//b[contains(text(),'{year}') and contains(text(),'Player Review')]/ancestor::table[1]")
        player_rows = player_table.find_elements(By.XPATH, ".//tr")[1:]  # Skip header row
        player_data = []

        for row in player_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 4:
                stat, name, team, value = [c.text.strip() for c in cols]
                player_data.append({
                    "Year": year,
                    "Statistic": stat,
                    "Name": name,
                    "Team": team,
                    "#": value
                })

        if player_data:
            pd.DataFrame(player_data).to_csv(f"{output_dir}/player_stats_{year}.csv", index=False)
            print(f"Saved: player_stats_{year}.csv")
        else:
            print("No player stats found.")
    except Exception:
        print("No player stats found.")

    # 3. Extract pitcher statistics table
    try:
        pitcher_table = driver.find_element(By.XPATH, f"//b[contains(text(),'{year}') and contains(text(),'Pitcher Review')]/ancestor::table[1]")
        pitcher_rows = pitcher_table.find_elements(By.XPATH, ".//tr")[1:]  # Skip header row
        pitcher_data = []

        for row in pitcher_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 4:
                stat, name, team, value = [c.text.strip() for c in cols]
                pitcher_data.append({
                    "Year": year,
                    "Statistic": stat,
                    "Name": name,
                    "Team": team,
                    "#": value
                })

        if pitcher_data:
            pd.DataFrame(pitcher_data).to_csv(f"{output_dir}/pitcher_stats_{year}.csv", index=False)
            print(f"Saved: pitcher_stats_{year}.csv")
        else:
            print("No pitcher stats found.")
    except Exception:
        print("No pitcher stats found.")

# Close the browser
driver.quit()
