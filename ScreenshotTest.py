import os
import time
import pdfkit
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_webpage_as_pdf(url, save_path):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-infobars')  # Disable info bars
    chrome_options.add_argument('--window-size=1280,800')  # Set window size

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the specified URL
        driver.get(url)

        # Wait for the page to load fully (adjust as needed)
        time.sleep(5)  # Adjust this wait time based on your internet speed

        # Get the page source
        page_source = driver.page_source

        # Create a temporary HTML file with the timestamp
        temp_html_path = os.path.join(os.path.dirname(save_path), "temp.html")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html_content = f"""
        <html>
            <head>
                <title>Webpage PDF</title>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .timestamp {{ position: fixed; top: 10px; right: 10px; font-size: 12px; color: gray; }}
                </style>
            </head>
            <body>
                <div class="timestamp">Captured on: {timestamp}</div>
                {page_source}
            </body>
        </html>
        """

        # Write the HTML content to the temporary file
        with open(temp_html_path, "w", encoding='utf-8') as f:
            f.write(html_content)

        # Convert the HTML file to PDF using pdfkit
        config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
        pdfkit.from_file(temp_html_path, save_path, configuration=config)

        print(f"PDF saved as: {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up: delete the temporary HTML file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    url = "https://www.digikey.com/en/products/detail/5749266-1/5749266-1-ND/1122005?curr=usd&utm_campaign=buynow&utm_medium=aggregator&utm_source=octopart"
    save_path = "C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/Screenshots/Screenshot.pdf"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save the webpage as PDF
    save_webpage_as_pdf(url, save_path)
