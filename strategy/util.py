import os
import csv

from os import listdir
from os.path import isfile

from pandas import np


def list_all_symbols(include_etf=False):
    """
    :return: sorted array of SYMBOL in data folder
    """
    data_path = os.path.join(os.getcwd(),'data')
    allsymbols = [f[0:-4] for f in listdir(data_path) if isfile(os.path.join(data_path, f)) and f.endswith('.csv')]

    if not include_etf:
        etfs = set()
        with open('./downloader/etf_etn.csv', 'r') as csvfile:
            etfreader = csv.reader(csvfile)
            next(etfreader)  # skip header
            for row in etfreader:
                etfs.add(row[0].strip())
        allsymbols = list(set(allsymbols) - etfs)
    allsymbols.sort()
    return allsymbols


def historical_volatility(df, days):
    "Return the annualized stddev of daily log returns of `sym`."
    quotes = df[-days:]
    logreturns = np.log(quotes / quotes.shift(1))
    return np.sqrt(252*logreturns.var())  # sqrt(252) * std deviation. same thing?

#
# from pandas import np
# from pandas.io.data import DataReader
#
#
# def historical_volatility(sym, days):
#     "Return the annualized stddev of daily log returns of `sym`."
#     try:
#         quotes = DataReader(sym, 'yahoo')['Close'][-days:]
#     except Exception, e:
#         print "Error getting data for symbol '{}'.\n".format(sym), e
#         return None, None
#     logreturns = np.log(quotes / quotes.shift(1))
#     return np.sqrt(252*logreturns.var())  # sqrt(252) * std deviation. same thing?
#
# if __name__ == "__main__":
#     print historical_volatility('GOOG', 30)
