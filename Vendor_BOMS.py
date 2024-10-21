import os
import pandas as pd
import csv

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


# Function to process the CSV and create individual CSVs for each vendor, and a master CSV
def process_csv(input_csv, master_output_csv):
    df = pd.read_csv(input_csv, header=None)  # Load without headers since we need specific rows

    # Extract MPN from Row 1, Column 4 (index 3)
    mpn_col_index = 3
    quantity_col_index = 1  # Quantities are in column 2 (index 1)

    # Extract vendor names from Row 2, Columns 34-43 for pricing (indices 33-42)
    vendor_names = df.iloc[1, 33:43].tolist()  # Vendor names for prices

    output_data_master = []  # To store data for the master CSV

    choice = input("Do you want to see the 3 Lowest, Median, or Highest prices? (Type 'Low', 'Med', or 'High'): ").capitalize()

    for index in range(2, len(df)):
        row = df.iloc[index]
        prices = row.iloc[33:43].tolist()  # Price columns (adjust indices as needed)
        quantity = df.iloc[index, quantity_col_index]  # Extract quantity from column 2

        prices_with_vendors = []
        for vendor, price in zip(vendor_names, prices):
            if pd.notna(price):  # Check if the price is not NaN
                prices_with_vendors.append((price, vendor))

        selected_prices = get_price_data(prices_with_vendors, choice)

        # Prepare output row for master CSV
        current_mpn = df.iloc[index, mpn_col_index]  # MPN from the current row
        output_row_master = [current_mpn, quantity]

        # Add selected prices to output row, ensuring there are three entries
        for i in range(3):
            if i < len(selected_prices):
                output_row_master.append(f"{selected_prices[i][1]}: {selected_prices[i][0]}")  # Vendor: Price
            else:
                output_row_master.append("")  # Leave blank if no price is available

        output_data_master.append(output_row_master)

    # Save the master output CSV
    with open(master_output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['MPN', 'Quantity', 'Vendor_Price1', 'Vendor_Price2', 'Vendor_Price3'])  # Adjust headers as needed
        writer.writerows(output_data_master)
    print(f"Master CSV saved as {master_output_csv}.")

    # Now generate individual CSV files for each vendor
    for vendor_idx, vendor_name in enumerate(vendor_names):
        if pd.isna(vendor_name):
            continue  # Skip if the vendor name is NaN
        
        output_data_vendor = []

        for index in range(2, len(df)):
            row = df.iloc[index]
            price = row.iloc[33 + vendor_idx]  # Price for the current vendor
            quantity = df.iloc[index, quantity_col_index]  # Extract quantity from column 2

            if pd.notna(price):
                selected_prices = [(float(price), vendor_name)]  # Single price for this vendor
                current_mpn = df.iloc[index, mpn_col_index]  # MPN from the current row
                
                # Prepare output row for vendor CSV
                output_row_vendor = [current_mpn, quantity, f"{vendor_name}: {selected_prices[0][0]}"]
                output_data_vendor.append(output_row_vendor)

        # Save the output CSV for each vendor
        output_vendor_csv = f'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/{vendor_name}_BOM.csv'
        with open(output_vendor_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['MPN', 'Quantity', 'Vendor_Price'])  # Adjust headers as needed
            writer.writerows(output_data_vendor)
        print(f"{vendor_name}_BOM.csv saved.")


# Main script logic
input_csv = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/TestQuote.csv'
master_output_csv = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/OutputQuotes.csv'
screenshot_dir = 'C:/Users/Zach.Gunter/Documents/GitHub/CymSTARQuoteParsing/Screenshots'

# Create the screenshots directory if it doesn't exist

process_csv(input_csv, master_output_csv)
