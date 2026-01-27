from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time

# 1. Setup Chrome Options for Linux/Chromebook
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without a visible window
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 2. Initialize the Driver (Specifying Chromium for Linux)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
    options=chrome_options
)

try:
    print("Connecting to Patna Metro Project page...")
    driver.get("https://www.delhimetrorail.com/pages/en/project-update-patna")
    
    # Wait for the page to load
    time.sleep(3)
    
    print(f"Success! Page Title is: {driver.title}")

except Exception as e:
    print(f"Oops, something went wrong: {e}")

finally:
    driver.quit()