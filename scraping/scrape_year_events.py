import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Define months
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def extract_events_for_year(url, year, driver=None):
    # Use passed driver or create a new one
    own_driver = False
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        )
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        own_driver = True

    driver.get(url)
    time.sleep(3)

    body = driver.find_element(By.TAG_NAME, "body")
    lines = body.text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    data = []
    for line in lines:
        for month in months:
            if month in line and any(char.isdigit() for char in line):
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

    df = pd.DataFrame(data)
    df.to_csv(f"data/events_{year}.csv", index=False)

    if own_driver:
        driver.quit()
