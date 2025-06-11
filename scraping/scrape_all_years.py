import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
)

# Launch Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("Loading year menu page")
url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)

# Find all links
all_links = driver.find_elements(By.TAG_NAME, "a")

# Filter numeric years only
year_links = []
for link in all_links:
    text = link.text.strip()
    href = link.get_attribute("href")
    if text.isdigit() and href:
        year_links.append((text, href))

print(f"Total valid year links collected: {len(year_links)}")

# Save to CSV
with open("data/year_links.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Year", "URL"])
    for year, href in year_links:
        writer.writerow([year, href])

driver.quit()
