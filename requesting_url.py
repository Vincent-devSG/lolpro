import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import chromedriver_autoinstaller


def get_html(url: str, params: dict | None = None)-> str:
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
    
    Returns:
        html (str):
            The HTML of the page, as text.
    """

    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

    # passing the optional parameters argument to the get function
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #options.add_argument('--disable-gpu')  # Add this line to disable GPU acceleration, which might help with headless mode

    browser = webdriver.Chrome(executable_path='/opt/homebrew/bin/chromedriver', options=options)
    
    try:
        browser.get(url)

        # Enable full screen
        browser.maximize_window()

        # Wait for the page to load
        time.sleep(1)

        # Click on the accept cookies button
        browser.find_element_by_xpath('//*[@class="fc-button fc-cta-consent fc-primary-button"]').click()

        # Click on the screen
        browser.find_element_by_class_name("headings").click()
        time.sleep(1)

        # Prepare to scroll
        elem = browser.find_element(By.TAG_NAME, "html")

        for i in range(10):
            elem.send_keys(Keys.END)

            print(f"Scrolling {i}")
            time.sleep(1)

        html_str = browser.page_source

    except TimeoutException:
        print("I give up...")

    finally:
        browser.quit()
    
    return html_str
