import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Define list of months to detect date-like patterns in the text
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def extract_events_for_year(url, year, driver=None):
    # Use passed driver if available, otherwise create a new one
    own_driver = False
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        )
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        own_driver = True

    # Load the page and wait for content to render
    driver.get(url)
    time.sleep(3)

    # Extract all text from the page body
    body = driver.find_element(By.TAG_NAME, "body")
    lines = body.text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    data = []

    # Loop through each line and attempt to extract date-based events
    for line in lines:
        for month in months:
            if month in line and any(char.isdigit() for char in line):
                # Main match: "April 3" or "April 3, 2020" with optional dash/colon
                match = re.match(r"(On )?(%s\s+\d{1,2})(,?\s+\d{4})?\s*[-–—:]?\s*(.*)" % month, line)
                if match:
                    date_text = match.group(2)
                    desc = match.group(4) if match.group(4) else line
                    data.append({
                        "Date": date_text.strip(),
                        "Description": desc.strip(),
                        "Year": year
                    })
                    break
                else:
                    # Alternative match: "April 3, 2020" anywhere in line
                    alt_match = re.search(r"(%s\s+\d{1,2},?\s+\d{4})" % month, line)
                    if alt_match:
                        data.append({
                            "Date": alt_match.group(1),
                            "Description": line.strip(),
                            "Year": year
                        })
                        break

    # If no date-based events were found, store the entire text as a single "event"
    if not data:
        full_text = "\n".join(lines)
        data.append({
            "Date": "",
            "Description": full_text.strip(),
            "Year": year
        })

    # Save the events to CSV
    df = pd.DataFrame(data)
    df.to_csv(f"data/events_{year}.csv", index=False)

    # Quit the driver if it was created inside this function
    if own_driver:
        driver.quit()
