from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from scrape_year_events import extract_events_for_year  # Import function
import time

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Launch Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the year menu page
url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)
time.sleep(2)  # Let the page load fully

# Extract links to individual years
year_links = driver.find_elements(By.XPATH, '//ul/li/a')

# Filter and process only numeric year links
for link in year_links:
    text = link.text.strip()
    href = link.get_attribute("href")
    if text.isdigit():
        year = int(text)
        print(f"Processing year {year}: {href}")
        try:
            extract_events_for_year(href, year, driver=driver)
        except Exception as e:
            print(f"Error for year {year}: {e}")

# Close the browser
driver.quit()
