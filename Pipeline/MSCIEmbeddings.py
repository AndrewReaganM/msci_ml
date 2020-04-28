import io
import pandas as pd
from gensim.models import Word2Vec
import numpy

class Embedding:
    _companies_fp = None
    _fundamentals_fp = None
    _training_df_fp = None
    _training_df = None
    _model = None
    _tickers = None

    def __init__(self, companies_fp=None, fundamentals_fp=None, training_df_fp=None):
        self._companies_fp = companies_fp
        self._fundamentals_fp = fundamentals_fp
        self._training_df_fp = training_df_fp

    def prepare_training_data(self, companies_fp=None, fundamentals_fp=None):
        if companies_fp is None:
            if self._companies_fp is None:
                raise Exception("Companies file was not provided. Pass companies_fp to the constructor or "
                                "prepare_training_data()")
        else:
            self._companies_fp = companies_fp

        if fundamentals_fp is None:
            if self._fundamentals_fp is None:
                raise Exception("Fundamentals file was not provided. Pass fundamentals fp to the constructor or "
                                "prepare_training_data()")
        else:
            self._fundamentals_fp = fundamentals_fp

        # Read in raw data files
        comp_df = pd.read_csv(self._companies_fp)
        fund_df = pd.read_csv(self._fundamentals_fp)

        # Remove unneeded company data
        comp_df = comp_df[['ticker','industry','sector','tag 1','tag 2','tag 3']]

        # Remove bad company data
        comp_df_clean_targets = comp_df[['ticker','industry','sector','tag 1']]
        comp_dfr = comp_df[comp_df_clean_targets.notna().all(axis=1)]

        # Removed unneeded fundamentals data
        fund_df = fund_df[['period','tickers','indicator','amount']]

        # Remove bad data
        # Many have 0 for the amount when it doesn't make sense (e.g. $0 final revenue)
        # Some 0 amounts may be legitimate, too many bad to sort through
        # Tossing all 0 amounts
        fund_df = fund_df[fund_df['amount'] != '0']

        fund_df_out = pd.DataFrame(columns=['period','ticker','data_name','data_val'])
        for row in fund_df.iterrows():
            row[1]['amount'] = "${}".format(row[1]['amount'])
        for row in fund_df[[',' in x for x in fund_df['tickers']]].iterrows():
            for ticker in row[1]['tickers'].split(', '):
                new_row_df = pd.DataFrame([
                    [row[1]['period'],ticker,row[1]['indicator'],row[1]['amount']]
                ], columns=['period','ticker','data_name','data_val'])
                fund_df_out = fund_df_out.append(new_row_df)
        fund_df_out = fund_df_out.append(fund_df[[',' not in x for x in fund_df['tickers']]].rename(columns={'tickers':'ticker','indicator':'data_name','amount':'data_val'}))

        shared = self.__shared_tickers(comp_df,fund_df_out)

        comp_df = self.__reduce(comp_df, shared)
        fund_df_out = self.__reduce(fund_df_out, shared)

        self._training_df = comp_df.append(fund_df_out)

    def train(self, size=50, workers=8, epochs=100):
        if self._training_df is None:
            raise Exception("No training data. Call prepare_training_data() or load_training_data().")

        training_data = self.__df_to_training_data()

        self._model = Word2Vec(training_data, size=size, min_count=0, workers=workers, sg=0, max_vocab_size=None,
                               max_final_vocab=None, iter=epochs)

    def save(self, fname):
        self._model.save(fname)

    def load(self, fname):
        self._model = Word2Vec.load(fname)

    def save_training_df(self, fname):
        self._training_df.to_csv(fname)

    def load_training_df(self, fname):
        if fname is None:
            if self._training_df_fp is None:
                raise Exception("No file provided. Include fname when calling load_training_df() or include "
                                "training_df_fp when calling the constructor.")
        else:
            self._training_df_fp = fname

        self._training_df = pd.read_csv(self._training_df_fp)

    def get_similar(self, ticker, count=10):

        similar = self._model.wv.most_similar(ticker, topn=count)
        similar = self.__remove_non_tickers(similar)
        return similar[:count]

        #return self._model.wv.most_similar(ticker, topn=count)

    def export_embeddings(self, fname):
        tickers = self._training_df.ticker.unique()
        tickers.sort()

        out = io.open(fname,'w',encoding='utf-8')
        for ticker in tickers:
            out.write(ticker + ',' + (','.join([str(x) for x in self._model.wv[ticker]]) + "\n"))
        out.close()

    def __remove_non_tickers(self, list):
        tickers = self._training_df.ticker.unique()

        list_out = []
        for t in list:
            if t[0] in tickers:
                list_out.append(t)

        return list_out

    def __shared_tickers(self, df1, df2):
        df1_tickers = pd.unique(df1['ticker'])
        df2_tickers = pd.unique(df2['ticker'])
        return df1_tickers[[ticker in df2_tickers for ticker in df1_tickers]]

    def __reduce(self, df, tickers):
        return df[[ticker in tickers for ticker in df['ticker']]]

    def __df_to_training_data(self):
        training_data = []
        for row in self._training_df.iterrows():
            list_row = []
            if type(row[1]['period']) is str:
                list_row.append(row[1]['period'])
            list_row.append(row[1]['ticker'])
            if type(row[1]['data_name']) is str:
                list_row.append(row[1]['data_name'])
            if type(row[1]['data_val']) is str:
                list_row.append(row[1]['data_val'])
            if type(row[1]['industry']) is str:
                list_row.append(row[1]['industry'])
            if type(row[1]['sector']) is str:
                list_row.append(row[1]['sector'])
            if type(row[1]['tag 1']) is str:
                list_row.append(row[1]['tag 1'])
            if type(row[1]['tag 2']) is str:
                list_row.append(row[1]['tag 2'])
            if type(row[1]['tag 3']) is str:
                list_row.append(row[1]['tag 3'])
            training_data.append(list_row)
        return training_data

