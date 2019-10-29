# Sample for how to use the stockDataHandler

import glob
import os
import pandas as pd
import stockDataHandler as sdh


# Path to Stock directory
pathStocks = "/Users/andrewmassey/Documents/2019 - Fall/SoftwareEng/MSCI/price-volume-data-for-all-us-stocks-etfs" \
             "/Stocks"
# Path to ETF directory
pathETFs = "/Users/andrewmassey/Documents/2019 - Fall/SoftwareEng/MSCI/price-volume-data-for-all-us-stocks-etfs/ETFs"

# Create list of all filenames to be imported
filenames = glob.glob(os.path.join(pathStocks, "*.txt"))  # Create list of Stock filenames.
filenames += glob.glob(os.path.join(pathETFs, "*.txt"))  # Create list of ETF filenames

# Import stocks and ETFs
print("Importing Stocks and ETFs from .txt files....")
new_df = sdh.stock_dataframe(filenames, print_sample=20, print_dtypes=True, verbose=True)
