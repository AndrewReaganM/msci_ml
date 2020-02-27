import matplotlib.pyplot as plt
import numpy as np

def plot_ticker(matrix, tickers, ticker_index, variable):

    variable_index = -1

    if (variable.lower() == "open"):
        variable_index = 0
    elif (variable.lower() == "high"):
        variable_index = 1
    elif (variable.lower() == "low"):
        variable_index = 2
    elif (variable.lower() == "close"):
        variable_index = 3
    elif (variable.lower() == "volume"):
        variable_index = 4
    else:
        print("ERROR: variable specified does not exist.")

    plt.plot(matrix[:,ticker_index * 5 + variable_index])
    plt.title("Variable: {}, Ticker: {}".format(variable, tickers[ticker_index]))
    plt.show()


#matrix = np.load("matrix_3201.npy")
#tickers = np.load("tickers_3201.npy")
#
#plot_ticker(matrix, tickers, 2, "close")

#def create_numpy()
#    a = np.array([])
