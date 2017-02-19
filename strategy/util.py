import os
import csv

from os import listdir
from os.path import isfile


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
