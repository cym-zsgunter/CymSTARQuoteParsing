import undetected_chromedriver as uc
import time
import random
from datetime import datetime
import base64
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def accept_cookies(driver):
    try:
        print("Looking for cookie consent button...")
        # Try different approaches to find the consent button
        cookie_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
        cookie_button.click()
        print("Cookies accepted.")
        time.sleep(2)  # Let the page refresh after accepting
    except NoSuchElementException:
        print("No cookie consent button found. Proceeding without action.")
    except Exception as e:
        print(f"Error while trying to accept cookies: {e}")

def save_webpage_as_pdf(url, save_path):
    # Initialize undetected chromedriver with options
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")  # Open browser in maximized mode
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass automation detection
    options.add_argument("--disable-infobars")  # Disable "Chrome is being controlled by automated test software"
    options.add_argument("--enable-javascript")  # Ensure JavaScript is enabled
    options.add_argument("--enable-cookies")  # Ensure cookies are enabled
    options.add_argument("--no-sandbox")  # Disable sandboxing (may help with some sites)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5745.96 Safari/537.36")


    driver = uc.Chrome(options=options)

    try:
        print("Opening URL...")
        driver.get(url)

        # Random delay to simulate human-like browsing
        time.sleep(random.uniform(3, 5))

        # Accept cookies if present
        accept_cookies(driver)

        # Additional random delay to mimic human behavior
        time.sleep(random.uniform(5, 10))

        print("Wait completed, capturing page to PDF...")

        # Set up PDF printing preferences with a timestamp in the footer
        chrome_print_options = {
            'landscape': False,
            'displayHeaderFooter': True,
            'printBackground': True,
            'headerTemplate': '',
            'footerTemplate': f'<span class="date">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>',
            'margin': {
                'top': '0.4in',
                'bottom': '0.4in',
                'left': '0.4in',
                'right': '0.4in'
            }
        }

        # Save the page as PDF
        pdf = driver.execute_cdp_cmd("Page.printToPDF", chrome_print_options)

        # Decode base64-encoded PDF and save
        pdf_data = base64.b64decode(pdf['data'])

        with open(save_path, 'wb') as f:
            f.write(pdf_data)

        print(f"PDF saved as: {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error during driver quit: {e}")

if __name__ == "__main__":
    url = "https://www.digikey.com/en/products/detail/adafruit-industries-llc/4210/10230021"
    save_path = "C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/Screenshots/Screenshot.pdf"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    save_webpage_as_pdf(url, save_path)
