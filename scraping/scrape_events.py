from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Launch Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the year menu page
url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)

# Extract links to individual years
year_links = driver.find_elements(By.XPATH, '//ul/li/a')

# Filter and print only numeric year links
for link in year_links:
    text = link.text.strip()
    href = link.get_attribute("href")
    if text.isdigit():
        print(f"{text}: {href}")

# Close the browser
driver.quit()
