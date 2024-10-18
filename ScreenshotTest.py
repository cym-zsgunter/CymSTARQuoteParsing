import undetected_chromedriver as uc
import time
import random
from datetime import datetime
import base64
import os

def save_webpage_as_pdf(url, save_path):
    # Initialize undetected chromedriver
    driver = uc.Chrome()

    try:
        print("Opening URL...")
        driver.get(url)

        # Random delay to simulate human-like browsing
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
        driver.quit()

if __name__ == "__main__":
    url = "https://www.digikey.com/en/products/detail/5749266-1/5749266-1-ND/1122005?curr=usd&utm_campaign=buynow&utm_medium=aggregator&utm_source=octopart"
    save_path = "C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/Screenshots/Screenshot.pdf"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    save_webpage_as_pdf(url, save_path)
