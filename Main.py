import pandas as pd
import csv
import requests
from selenium import webdriver

# Function to handle price extraction based on user input
def get_price_data(prices_with_vendors, choice):
    # Filter and convert valid price values
    prices = []
    for price, vendor in prices_with_vendors:
        try:
            # Attempt to convert the price to float, ignoring non-numeric values
            prices.append(float(price))
        except ValueError:
            # Ignore any non-numeric values (like vendor names)
            continue

    # Sort the prices
    prices = sorted(prices)

    # Get the 3 lowest, median, or highest prices based on user input
    if choice == 'Low':
        return prices[:3]  # 3 lowest prices
    elif choice == 'Med':
        median_idx = len(prices) // 2
        return prices[median_idx-1:median_idx+2]  # 3 median prices
    elif choice == 'High':
        return prices[-3:]  # 3 highest prices

# Function to process the CSV
def process_csv(input_csv, output_csv):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv, header=None)  # Load without headers since we need specific rows

    # Extract MPN from Row 1, Column 4 (index 3)
    mpn_col_index = 3
    mpn = df.iloc[0, mpn_col_index]

    # Extract vendor names from Row 2, Columns 34-43 for pricing (indices 33-42)
    vendor_names = df.iloc[1, 33:43].tolist()  # Vendor names for prices

    # Extract URLs from Row 2, Columns 51-60 for URLs (indices 50-59)
    url_names = df.iloc[1, 50:60].tolist()  # Vendor names for URLs

    # Prepare an output CSV for the results
    output_data = []

    # Ask the user for their choice (Low, Med, High)
    choice = input("Do you want to see the 3 Lowest, Median, or Highest prices? (Type 'Low', 'Med', or 'High'): ")

    # Iterate through the rows starting from the 3rd row (index 2)
    for index in range(2, len(df)):
        row = df.iloc[index]

        # Assuming prices are in columns AH-AQ (indices 33-42) for this row
        prices = row.iloc[33:43].tolist()  # Price columns (adjust indices as needed)

        # Pair prices with their respective vendors
        prices_with_vendors = []
        for vendor, price in zip(vendor_names, prices):
            try:
                # Convert price to float and keep the vendor association
                prices_with_vendors.append((float(price), vendor))
            except ValueError:
                # Ignore non-numeric values (but still keep valid vendor-price pairs)
                continue

        # Get the relevant price data (with vendor names) based on the user's choice
        selected_prices = get_price_data(prices_with_vendors, choice)

        # Add the selected prices and vendor information to the output row
        output_row = [mpn] + [f"{vendor}: {price}" for price, vendor in prices_with_vendors if price in selected_prices]
        output_data.append(output_row)

        # Follow URLs and take screenshots (functionality to be implemented)
        for i, (price, vendor) in enumerate(prices_with_vendors[:3]):
            if i < len(url_names) and pd.notna(url_names[i]):  # Check if a URL exists for the vendor
                screenshot_filename = f"{mpn}_Quote_{vendor}_{choice.capitalize()}.jpg"
                # Screenshot logic placeholder
                print(f"Taking screenshot of {url_names[i]} and saving as {screenshot_filename}")
                # take_screenshot(url_names[i], screenshot_filename)  # Uncomment if screenshot logic is implemented

    # Save the output CSV with vendors and prices
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['MPN', 'Vendor_Price1', 'Vendor_Price2', 'Vendor_Price3'])  # Adjust headers as needed
        writer.writerows(output_data)

# Main script logic
input_csv = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/TestQuote.csv'
output_csv = 'path_to_output.csv'
process_csv(input_csv, output_csv)

#First Commit