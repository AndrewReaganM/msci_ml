import matplotlib.pyplot as plt
import numpy as np

def calculate_mape(actual_values, forcasted_values):

    if (len(actual_values) < 1):
        raise IndexError("0 values in input array.")
        
    if (len(actual_values) != len(forcasted_values)):
        raise IndexError("actual_values and forcasted_values are different lengths.")
        
    if np.isin(0, actual_values):
        actual_values[np.where(actual_values == 0)] += 0.000001
    
    return np.sum(np.absolute((actual_values - forcasted_values) / actual_values)) / len(actual_values) * 100

def variable_to_index(variable):
    
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
        raise ValueError("ERROR: variable specified does not exist.")
        
    return variable_index

def plot_ticker(matrix, tickers, ticker_index, variable):

    """Plots the value of a ticker's variable over time.

    This function requires a matrix in the form that is constructed in
    MSCI Data Exploration.ipynb

    Args:
        matrix (numpy.array) a numpy matrix of training data
        tickers (numpy.array) an array of tickers included in the matrix
        ticker_index (int) specific index in tickers to plot
        variable (str) the stock variable to plot

    """
    
    variable_index = variable_to_index(variable)


    plt.plot(matrix[:,ticker_index * 5 + variable_index])
    plt.title("Variable: {}, Ticker: {}".format(variable, tickers[ticker_index]))
    plt.show()
    
    
def construct_train_test_indicies(number_of_examples, split = 0.5, seed = 42):
    
    # Shuffle indicies for dataset.
    shuffled_indicies = np.linspace(0, number_of_examples - 1, number_of_examples, dtype=int)
    np.random.seed(seed)
    np.random.shuffle(shuffled_indicies)
    
    # Train and test indicies
    train_indicies = shuffled_indicies[:int(shuffled_indicies.size * split)]
    test_indicies = shuffled_indicies[int(shuffled_indicies.size * split):]
    
    return train_indicies, test_indicies
    
def construct_train_test_sets(matrix, ticker_index, target_variable, split = 0.5, seed = 42):
    
    number_of_examples = matrix.shape[0]
    
    train_indicies, test_indicies = construct_train_test_indicies(
        number_of_examples)
    
    variable_index = variable_to_index(target_variable)

    train_set = np.delete(matrix[train_indicies], ticker_index * 5 + variable_index, 1)
    train_target = matrix[train_indicies][:, ticker_index * 5 + variable_index]
    test_set = np.delete(matrix[test_indicies], ticker_index * 5 + variable_index, 1)
    test_target = matrix[test_indicies][:, ticker_index * 5 + variable_index]
    
    return train_set, train_target, test_set, test_target

