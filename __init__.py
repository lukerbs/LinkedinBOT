import tkinter as tk
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


# Assign custom user agent 
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")

# Instantiate chrome web driver
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
# Open the website
url = 'https://www.linkedin.com'
driver.get(url)


main_window = tk.Tk()
main_window.withdraw()