import pandas as pd

print("Hello world")

apple = pd.read_csv("/Users/andrewmassey/Documents/2019 - Fall/SoftwareEng/MSCI/price-volume-data-for-all-us-stocks"
                    "-etfs/Stocks/aapl.us.txt")
print(apple.head(5))