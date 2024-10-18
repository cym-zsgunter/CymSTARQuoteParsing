import os
import pandas as pd
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to handle price extraction based on user input
def get_price_data(row, choice):
    prices = []
    for price, vendor in row:
        if pd.notna(price):  # Check for NaN values
            try:
                prices.append((float(price), vendor))
            except ValueError:
                print(f"Invalid price '{price}' for vendor '{vendor}'")  # Handle non-numeric price values

    # Sort the prices
    prices = sorted(prices, key=lambda x: x[0])  # Sort by price

    # Get the 3 lowest, median, or highest prices based on user input
    if choice == 'Low':
        return prices[:3]  # 3 lowest prices
    elif choice == 'Med':
        median_idx = len(prices) // 2
        return prices[median_idx-1:median_idx+2]  # 3 median prices
    elif choice == 'High':
        return prices[-3:]  # 3 highest prices
    return []  # Return an empty list if choice is not recognized


# Function to take a screenshot
def take_screenshot(url, filename):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        driver.get(url)

        # Optional: Wait for the page to fully load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'body'))  # Wait for the body to be visible
        )
        
        # Take a screenshot of the entire page
        driver.save_screenshot(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Failed to take screenshot of {url}: {e}")
    finally:
        driver.quit()


# Function to process the CSV
def process_csv(input_csv, output_csv, screenshot_dir):
    df = pd.read_csv(input_csv, header=None)  # Load without headers since we need specific rows

    # Extract MPN from Row 1, Column 4 (index 3)
    mpn_col_index = 3
    mpn = df.iloc[0, mpn_col_index]

    # Extract vendor names from Row 2, Columns 34-43 for pricing (indices 33-42)
    vendor_names = df.iloc[1, 33:43].tolist()  # Vendor names for prices
    url_names = df.iloc[1, 50:60].tolist()  # Vendor names for URLs

    output_data = []

    choice = input("Do you want to see the 3 Lowest, Median, or Highest prices? (Type 'Low', 'Med', or 'High'): ")

    for index in range(2, len(df)):
        row = df.iloc[index]
        prices = row.iloc[33:43].tolist()  # Price columns (adjust indices as needed)

        prices_with_vendors = []
        for vendor, price in zip(vendor_names, prices):
            if pd.notna(price):  # Check if the price is not NaN
                prices_with_vendors.append((price, vendor))

        selected_prices = get_price_data(prices_with_vendors, choice)

        # Prepare output row
        current_mpn = df.iloc[index, mpn_col_index]  # MPN from the current row
        output_row = [current_mpn]

        # Add selected prices to output row, ensuring there are three entries
        for i in range(3):
            if i < len(selected_prices):
                output_row.append(f"{selected_prices[i][1]}: {selected_prices[i][0]}")  # Vendor: Price
            else:
                output_row.append("")  # Leave blank if no price is available

        output_data.append(output_row)

        # Take screenshots for the selected vendors' URLs
        for i, (price, vendor) in enumerate(selected_prices[:3]):
            if i < len(url_names) and pd.notna(url_names[i]):
                screenshot_filename = os.path.join(screenshot_dir, f"{current_mpn}_Quote_{vendor}_{choice.capitalize()}.png")
                take_screenshot(url_names[i], screenshot_filename)  # Save screenshot

    # Save the output CSV with vendors and prices
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['MPN', 'Vendor_Price1', 'Vendor_Price2', 'Vendor_Price3'])  # Adjust headers as needed
        writer.writerows(output_data)


# Main script logic
input_csv = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/TestQuote.csv'
output_csv = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/OutputQuotes.csv'
screenshot_dir = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/Screenshots'

# Create the screenshots directory if it doesn't exist
os.makedirs(screenshot_dir, exist_ok=True)

process_csv(input_csv, output_csv, screenshot_dir)
