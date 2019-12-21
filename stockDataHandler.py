"""
Library for using a Pandas dataframe to import stock/etf data from Kaggle.

"""

import os
import pandas as pd


def import_stock_csv(_file_list, verbose=False, date_as_index=True):
    """
    Function to import .txt file contents into a dictionary of Pandas dataframes.

    :param _file_list: List of stock data file paths.
    :param verbose: Bool to print errors or not.
    :return: dictionary of dataframes keyed by ticker.
    """
    _dfDict = {}
    for _file in _file_list:
        _file_name = os.path.splitext(os.path.basename(_file))[0]
        try:
            _dfn = pd.read_csv(_file, engine='c')  # Read in CSV
            _objName = _file_name.split('.', 1)[0]  # Retrieve the stock name
            _dfn['Name'] = _objName  # Add column with stock name
            _dfn.index.name = _file_name
            _dfn['Date'] = pd.to_datetime(_dfn['Date'])  # Convert Date field to correct data type.
            if date_as_index:
                _dfn.set_index(['Date'], inplace=True, verify_integrity=True)  # Set date as index if specified
            _dfDict[_objName] = _dfn  # Add DF to dictionary
            # print("Imported " + file_name)
        except Exception as e:
            if verbose:  # Print exception
                print(str(e) + ": '" + _file_name + ".txt' File may be blank.")
    return _dfDict  # Return a dictionary of dataframes keyed by ticker.


def stock_dataframe(_file_list, verify_integrity=True, print_sample=0, print_dtypes=False, verbose=False, sort_index=False):
    """
    Function to import Stock/ETF data in specific format.

    :rtype: pandas df
    :param _file_list: List of files to be imported.
    :param verify_integrity: bool: whether pandas should verify index integrity or not.
    :param print_sample: int: print a sample of the data (head).
    :param print_dtypes: bool: print dtypes of imported data.
    :param verbose: bool: more verbose printing to console.
    :return: complete pandas dataframe.
    """
    _dflist = import_stock_csv(_file_list, verbose=verbose, date_as_index=False)

    if verbose:
        print("Concatenating " + str(len(_dflist)) + " dataframes.")

    _dataframe = pd.concat(_dflist, axis=0, ignore_index=True)  # Concatenate dataframes from dictionary/list
    if verbose:
        print("Setting up index and verifying index integrity...")

    # Reindex dataframe using name and date
    try:
        _dataframe.set_index(['Name', 'Date'], inplace=True, verify_integrity=verify_integrity)
    except KeyError as e:
        print("Indexing error" + str(e) + ". Make sure that this column was not an index in the external DF.")

    # Sorts dataframe by index
    if sort_index:
        if verbose:
            print("Sorting index...")
        _dataframe.sort_index()

        # Prints a sampling of data
        if print_sample != 0:
            print(_dataframe.head(print_sample))

    if verbose:
        print("Import complete\nLines: " + str(len(_dataframe.index)))

    if print_dtypes:  # Optionally print datatypes for verification.
        print("Data Types:")
        print(_dataframe.dtypes)

    return _dataframe  # Return individual dataframe.


def import_supp_data(_comp_data, verify_integrity=True):
    _comp_df = pd.read_csv(_comp_data)  # Read CSV
    _comp_df['ticker'] = _comp_df['ticker'].str.lower()  # Make ticker lowercase for easier access.
    _comp_df.set_index(['ticker'], inplace=True, verify_integrity=verify_integrity)  # Set ticker as index.
    _comp_df.columns = [_c.replace(' ', '_') for _c in _comp_df.columns]  # Replace spaces with underscores.
    return _comp_df  # Return individual dataframe.
