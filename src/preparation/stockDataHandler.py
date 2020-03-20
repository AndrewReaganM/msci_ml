"""
Library for using a Pandas dataframe to import stock/etf data from Kaggle.

"""

import os
import pandas as pd


def import_stock_csv(_file_list, verbose=False, date_as_index=True, impute_vals=True):
    """
    Function to import .txt file contents into a dictionary of Pandas dataframes.

    :param date_as_index: indexes the dataframes by date.
    :param impute_vals: imputes additional data values
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
<<<<<<< Updated upstream:testEnv/stockDataHandler.py
            _dfn.drop(columns="OpenInt", axis=1, inplace=True) # Drop column with no data.
=======
            _dfn.drop(columns="OpenInt", axis=1, inplace=True)  # Drop column with no data.
            if impute_vals:
                # Insert imputed values that could help the model.
                _dfn['Close_to_Open'] = (_dfn.Open - _dfn.Close.shift(fill_value=0.0)) / _dfn.Close.shift(
                    fill_value=0.0)
                _dfn['Close_to_High'] = (_dfn.High - _dfn.Close.shift(fill_value=0.0)) / _dfn.Close.shift(
                    fill_value=0.0)
                _dfn['Close_to_Low'] = (_dfn.Low - _dfn.Close.shift(fill_value=0.0)) / _dfn.Close.shift(fill_value=0.0)
                _dfn['Close_to_Close'] = (_dfn.Close - _dfn.Close.shift(fill_value=0.0)) / _dfn.Close.shift(
                    fill_value=0.0)
                _dfn['Volume_Change'] = (_dfn.Volume - _dfn.Volume.shift(fill_value=0.0)) / _dfn.Volume.shift(
                    fill_value=0.0)
                # Remove the first value for the ticker (invalid imputed value, usually -inf)
                _dfn.drop([0], inplace=True)

            # Add dataframe to dictionary by key
>>>>>>> Stashed changes:src/preparation/stockDataHandler.py
            _dfDict[_objName] = _dfn  # Add DF to dictionary
            # print("Imported " + file_name)
        except Exception as e:
            if verbose:  # Print exception
                print(str(e) + ": '" + _file_name + "' File may be blank.")
    return _dfDict  # Return a dictionary of dataframes keyed by ticker.


def stock_dataframe(_file_list, verify_integrity=True, print_sample=0,
                    print_dtypes=False, verbose=False, sort_index=False, impute_vals=True):
    """
    Function to import Stock/ETF data in specific format.

    :param impute_vals: imputes additional data values
    :param sort_index: Boolean that sorts by multi-index if true
    :rtype: pandas df
    :param _file_list: List of files to be imported.
    :param verify_integrity: bool: whether pandas should verify index integrity or not.
    :param print_sample: int: print a sample of the data (head).
    :param print_dtypes: bool: print dtypes of imported data.
    :param verbose: bool: more verbose printing to console.
    :return: complete pandas dataframe.
    """
    # date_as_index is false as that needs to be set up in the master dataframe concatenated below.
    _df_list = import_stock_csv(_file_list, verbose=verbose, date_as_index=False, impute_vals=impute_vals)

    if verbose:
        print("Concatenating " + str(len(_df_list)) + " dataframes.")

    _dataframe = pd.concat(_df_list, axis=0, ignore_index=True)  # Concatenate dataframes from dictionary/list
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

    # Prints a sampling of data, if requested
    if print_sample != 0:
        print(_dataframe.head(print_sample))

    if verbose:
        print("Import complete\nLines: " + str(len(_dataframe.index)))

    if print_dtypes:  # Optionally print datatypes for verification.
        print("Data Types:")
        print(_dataframe.dtypes)

    del _df_list

    return _dataframe  # Return individual dataframe.


def import_supp_data(_comp_data, verify_integrity=True):
    """
    Function to import supplemental data from a csv into a dataframe that can then be queried.
    :param _comp_data: supplemental data file path
    :param verify_integrity: boolean True verifies index integrity
    :return: dataframe indexed by ticker that contains supplemental data.
    """
    _comp_df = pd.read_csv(_comp_data)  # Read CSV
    _comp_df['ticker'] = _comp_df['ticker'].str.lower()  # Make ticker lowercase for easier access.
    _comp_df.set_index(['ticker'], inplace=True, verify_integrity=verify_integrity)  # Set ticker as index.
    _comp_df.columns = [_c.replace(' ', '_') for _c in _comp_df.columns]  # Replace spaces with underscores.
    return _comp_df  # Return individual dataframe.
