"""
Example for how to use the stockDataHandler.
"""

import glob
import os
import pandas as pd
import stockDataHandler as sdh

# Path to Stock directory
pathStocks = "/Users/andrewmassey/Documents/2019 - Fall/SoftwareEng/MSCI/price-volume-data-for-all-us-stocks-etfs" \
             "/Stocks"
# Path to ETF directory
pathETFs = "/Users/andrewmassey/Documents/2019 - Fall/SoftwareEng/MSCI/price-volume-data-for-all-us-stocks-etfs/ETFs"

# Path to additional data.
comp_data = "/Users/andrewmassey/Documents/2019 - Fall/SoftwareEng/MSCI/supplementalData/all-us-stocks-tickers" \
            "-company-info-logos/companies.csv"

stock_file_ext = "*.txt"
# Create list of all filenames to be imported
filenames = glob.glob(os.path.join(pathStocks, stock_file_ext))  # Create list of Stock filenames.
filenames += glob.glob(os.path.join(pathETFs, stock_file_ext))  # Concatenate the list of ETF filenames

# Import stocks and ETFs
print("Importing Stocks and ETFs from .txt files...")
stock_df = sdh.stock_dataframe(filenames, print_sample=5, print_dtypes=False, verbose=False)

# Import supplemental data
print("Importing supplemental company metadata...")
comp_df = sdh.import_supp_data(comp_data)

print("Import complete.")

# Example queries
print(comp_df.query('ticker == "tsco"'))
print(stock_df.query('Name == "tsco"'))
