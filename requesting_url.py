import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


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
    # passing the optional parameters argument to the get function
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')  # Add this line to disable GPU acceleration, which might help with headless mode

    

    browser = webdriver.Chrome(executable_path='/opt/homebrew/bin/chromedriver', options=options)
    
    
    try:
        browser.get(url)

        # Enable full screen
        browser.maximize_window()

        # sometimes the cookies pop up coming up
        
        #WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="fc-footer-buttons"]')))
        #refuse_button = browser.find_element(By.XPATH, '//button[@class="fc-button fc-cta-do-not-consent fc-secondary-button"]')

        # Click the accept button
        #refuse_button.click()

        # Wait for the page to load
        time.sleep(2)

        # exit the input box by clicking on the body
        element_to_click_xpath = '//*[@id="app"]/main/div/div[3]/div/div/table/thead/tr/th[1]'
        element_to_click = browser.find_element(By.XPATH, element_to_click_xpath)
        element_to_click.click()
        
        div_xpath = '//*[@id="app"]/main/div'  
        div_element = browser.find_element(By.XPATH, div_xpath)


        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = browser.execute_script("return arguments[0].scrollHeight;", div_element)


        while True:
            # Get the current scroll position
            current_scroll_position = browser.execute_script("return window.scrollY;")
            
            # Print the current scroll position for debugging
            print(f"Current Scroll Position (Y): {current_scroll_position}")

            # Scroll down to the bottom of the page
            browser.execute_script("window.scrollBy(0, window.innerHeight);")

             # Get the current scroll position
            current_scroll_position = browser.execute_script("return window.scrollY;")
            
            # Print the current scroll position for debugging
            print(f"Current Scroll Position (Y): {current_scroll_position}")
            
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Get new scroll height after scrolling
            new_height = browser.execute_script("return arguments[0].scrollHeight;", div_element)

            # Print scroll heights for debugging
            print(f"Last Height: {last_height}, New Height: {new_height}")

            # Break the loop if the scroll height has not changed, indicating the end of the page
            if new_height == last_height:
                break

            # Update the scroll height for the next iteration
            last_height = new_height


        html_str = browser.page_source


    except TimeoutException:
        print("I give up...")

    finally:
        browser.quit()

    # Close the browser
    browser.quit()
    
    return html_str
