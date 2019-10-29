import os
import pandas as pd


def import_stock_csv(_file_list, verbose=False):
    _dfList = []
    for file in _file_list:
        _file_name = os.path.splitext(os.path.basename(file))[0]
        try:
            _dfn = pd.read_csv(file)
            _objName = _file_name.split('.', 1)[0]
            _dfn['Name'] = _objName
            _dfn.index.name = _file_name
            # Convert Date field to correct format.
            _dfn['Date'] = pd.to_datetime(_dfn['Date'])
            _dfList.append(_dfn)
            # print("Imported " + file_name)
        except Exception as e:
            if verbose:
                print(str(e) + ": '" + _file_name + ".txt' File may be blank.")
    return _dfList


def stock_dataframe(_file_list, verify_integrity=True, print_sample=0, print_dtypes=False, verbose=False):
    """
    Function to import Stock/ETF data in specific format.

    :param _file_list: List of files to be imported.
    :param verify_integrity: bool: whether pandas should verify index integrity or not.
    :param print_sample: int: print a sample of the data (head).
    :param print_dtypes: bool: print dtypes of imported data.
    :param verbose: bool: more verbose printing to console.
    :return: complate pandas dataframe.
    """
    dflist = import_stock_csv(_file_list, verbose=verbose)

    if verbose:
        print("Concatenating " + str(len(dflist)) + " dataframes.")

    _dataframe = pd.concat(dflist, axis=0, ignore_index=True)
    if verbose:
        print("Setting up index and verifying index integrity...")

    # Reindexes dataframe using name and date
    _dataframe.set_index(['Name', 'Date'], inplace=True, verify_integrity=verify_integrity)

    # Prints a sampling of data
    if print_sample != 0:
        print("Post-indexing sample:")
        print(_dataframe.head(5))

    if verbose:
        print("Import complete\nLines: " + str(len(_dataframe.index)))

    if print_dtypes:
        print("Data Types:")
        print(_dataframe.dtypes)

    return _dataframe
