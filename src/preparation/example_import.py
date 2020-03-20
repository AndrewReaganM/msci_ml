import stockDataHandler as sdh
import glob
import os


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

sdf = sdh.stock_dataframe(filenames, verbose=True, print_sample=10)

supp_data = sdh.import_supp_data(comp_data)
print("Data import complete")

