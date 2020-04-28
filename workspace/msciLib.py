import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


"""MSCI Helper Library (msciLib)

This module includes helper functions that can be utilized in the notebooks to
improve readability of code as well as streamline development.

Example:
    import msciLib
    
    v_index = msciLib.variable_to_index("Close")

Attributes:
    VARIABLE_MAP (np.array (string)): an array of variables in the order as 
        they appear in the dataset. This allows for a mapping between variable
        and its index and vice versa.
Todo:
    * Look into Symmetric MAPE for calculate MAPE to resolve divide by zero.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

# Global variables
VARIABLE_MAP = np.array(["open", "high", "low", "close", "volume"]) # constant

def select_ticker(tickers, df, chosen_tickers_dict):
    ticker = np.random.choice(tickers)
    num_entries = df.query('Name == "{}"'.format(ticker)).shape[0]
    
    while ((num_entries < 2500 or num_entries > 4000) or ticker in chosen_tickers_dict):
        
        ticker = np.random.choice(tickers)
        num_entries = df.query('Name == "{}"'.format(ticker)).shape[0]
        
    return ticker

def select_random_ticker(tickers, df, chosen_tickers):
    ticker = np.random.choice(tickers)
    while (df.query('Name == "{}"'.format(ticker)).shape[0] < 2500 or ticker in chosen_tickers):
        
        ticker = np.random.choice(tickers)
        
    chosen_tickers.append(ticker)
        
    return ticker, chosen_tickers

# TODO(melissa): clean up import.
def import_3201_stock(_file_list, verbose=False, date_as_index=True):
    """
    Function to import .txt file contents into a dictionary of Pandas dataframes.

    :param _file_list: List of stock data file paths.
    :param verbose: Bool to print errors or not.
    :return: dictionary of dataframes keyed by ticker.
    """
    _dfDict = pd.DataFrame()
    for i in range(len(_file_list)):
    # for i in range(200):
        
        _file = _file_list[i]
        
        _file_name = os.path.splitext(os.path.basename(_file))[0]
        try:
            _dfn = pd.read_csv(_file, engine='c')  # Read in CSV
            _objName = _file_name.split('.', 1)[0]  # Retrieve the stock name
            _dfn['Name'] = _objName  # Add column with stock name
            _dfn.index.name = _file_name
            _dfn['Date'] = pd.to_datetime(_dfn['Date'])  # Convert Date field to correct data type.
            if date_as_index:
                _dfn.set_index(['Date'], inplace=True, verify_integrity=True)  # Set date as index if specified
                
            my_data = np.genfromtxt(_file, dtype=[('Date','U10'),('Open','f8'),
                                                       ('High','f8'),('Low','f8'),('Close','f8'),
                                                      ('Volume','f8'),('OpenInt','f8')],delimiter=',', skip_header = True)
            if (my_data.size == 3201):
                #_dfDict[_objName] = my_data  # Add DF to dictionary
                _dfDict = _dfDict.append(_dfn)   
            #_dfDict[_objName] = _dfn  # Add DF to dictionary
            # print("Imported " + file_name)
        except Exception as e:
            if verbose:  # Print exception
                print(str(e) + ": '" + _file_name + ".txt' File may be blank.")
    return _dfDict  # Return a dictionary of dataframes keyed by ticker.


def calculate_mape(actual_values, forcasted_values):
    """Calculates the Mean Absolute Percentage Error (MAPE) of two arrays.
    
    Note: there is no divide by zero error, a small value is added to
          zeros that are present. 
        
    TODO(mewilson): look further into symmetric MAPE.

    Args:
        actual_values (numpy.array): The actual values
        forcasted_values (numpy.array): The predicted values

    Returns:
        float: he calculated Mean Absolute Percentage Error, see 
            MSCI\ MAPE\ Calculate.ipynb for details
        
    Raises:
        IndexError: Raises this when input arrays are unequal lengths, or empty

    """

    if (len(actual_values) < 1):
        raise IndexError("0 values in input array.")
        
    if (len(actual_values) != len(forcasted_values)):
        raise IndexError("actual_values and forcasted_values are different lengths.")
        
    if np.isin(0, actual_values):
        actual_values[np.where(actual_values == 0)] += 0.000001
    
    return np.sum(np.absolute((actual_values - forcasted_values) / actual_values)) / len(actual_values) * 100


def calculate_basecase_mape(matrix, ticker_index, variable):
    
    variable_index = variable_to_index(variable)
    
    actual_values = matrix[1:, ticker_index * 5 + variable_index]
    forcasted_values = matrix[0:-1, ticker_index * 5 + variable_index]
    
    return calculate_mape(actual_values, forcasted_values)


def index_to_variable(index):
    """Maps a index to its variable value in the matrix. Inverse of 
        variable_to_index function.
    
    0, 1, 2, 3, 4 are mapped to Open, High, Low, Close, Volume respectively.

    Args:
        index (int): the index of the variable

    Returns:
        string: the variable
        
    Raises:
        ValueError: if the specified index does not exist in dataset.

    """
    
    if index < 0 or index > 4:
        raise ValueError("index specified does not exist.")
        
    return VARIABLE_MAP[index]


def variable_to_index(variable):
    """Maps a variable to its index value in the matrix.
    
    Open, High, Low, Close, Volume are mapped to 0, 1, 2, 3, 4 respectively.

    Args:
        variable (string): the variable

    Returns:
        int: the index of the variable
        
    Raises:
        ValueError: if the specified variable does not exist in dataset.

    """
    
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
        raise ValueError("variable specified does not exist.")
        
    return variable_index


def variable_to_index(variable):
    """Maps a variable to its index value in the matrix.
    
    Open, High, Low, Close, Volume are mapped to 0, 1, 2, 3, 4 respectively.

    Args:
        variable (string): The variable

    Returns:
        int: the index of the variable
        
    Raises:
        ValueError: if the specified variable does not exist in dataset.

    """
    
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
        raise ValueError("variable specified does not exist.")
        
    return variable_index

def plot_ticker(matrix, tickers, ticker_index, variable):

    """Plots the value of a ticker's variable over time.

    This function requires a matrix in the form that is constructed in
    MSCI Data Exploration.ipynb

    Args:
        matrix (numpy.array): a numpy matrix of training data
        tickers (numpy.array): an array of tickers included in the matrix
        ticker_index (int): specific index in tickers to plot
        variable (str): the stock variable to plot

    """
    
    variable_index = variable_to_index(variable)


    plt.plot(matrix[:,ticker_index * 5 + variable_index])
    
    plt.title("Variable: {}, Ticker: {}, Ticker Index: {}".format(
        variable, tickers[ticker_index], ticker_index))
    
    plt.show()
    
    
def construct_train_test_indicies(number_of_examples, split = 0.5, seed = 42):
    """Constructs randomized indicies for train and test sets. 

    Args:
        number_of_examples (int): number of examples in the dataset to split.
        split (float): percentage of data to be alloted in the training set.
        seed (int): the seed for randomization.

    Returns:
        (numpy.array (int), numpy.array (int)): the training and testing
            indicies respectively.
            
    """
    
    # Shuffle indicies for dataset.
    shuffled_indicies = np.linspace(0, number_of_examples - 1, number_of_examples, dtype=int)
    np.random.seed(seed)
    np.random.shuffle(shuffled_indicies)
    
    # Train and test indicies
    train_indicies = shuffled_indicies[:int(shuffled_indicies.size * split)]
    test_indicies = shuffled_indicies[int(shuffled_indicies.size * split):]
    
    return train_indicies, test_indicies
    
    
def construct_train_test_sets(matrix, ticker_index, target_variable, split = 0.5, seed = 42):
    """Constructs train and test sets for a matrix where features are columns
        and examples are rows.

    Args:
        matrix (numpy.array): a 2D matrix of examples.
        ticker_index (int): the index of the ticker to be predicted.
        target_variable (string): the variable to be predicted.
        split (float): percentage of data to be alloted in the training set.
        seed (int): the seed for randomization.

    Returns:
        (numpy.array (float), numpy.array (float), numpy.array (float), 
        numpy.array (float)): the training and testing sets and targets.
            
    """
    
    number_of_examples = matrix.shape[0]
    
    train_indicies, test_indicies = construct_train_test_indicies(
        number_of_examples)
    
    variable_index = variable_to_index(target_variable)

    train_set = np.delete(matrix[train_indicies], ticker_index * 5 + variable_index, 1)
    train_target = matrix[train_indicies][:, ticker_index * 5 + variable_index]
    test_set = np.delete(matrix[test_indicies], ticker_index * 5 + variable_index, 1)
    test_target = matrix[test_indicies][:, ticker_index * 5 + variable_index]
    
    return train_set, train_target, test_set, test_target

def import_numpy_dict(_file_list, _expected_length, numStart, verbose=False):
    """
    Function to import .npy file contents into a dictionary of numpy arrays

    :param _file_list: List of feature importance file paths.
    :param verbose: Bool to print errors or not.
    :return: dictionary of numpy arrays keyed by ticker.
    """
    _feat_imp_dict = {}
    for _file in _file_list:
        _file_name = os.path.splitext(os.path.basename(_file))[0]
        
        
        _np_array = np.load(_file)
        
        if (len(_np_array) != _expected_length):

            if (verbose):
                print("ERROR {}".format(len(_np_array)))
                print(_file)
                print("")
        
        else:
            _company_num = _file_name[numStart:]
            _feat_imp_dict[int(_company_num)] = _np_array
            
    return _feat_imp_dict  # Return a dictionary of dataframes keyed by ticker.