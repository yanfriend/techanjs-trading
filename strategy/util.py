import os

from os import listdir
from os.path import isfile


def list_all_symbols():
    """
    :return: sorted array of SYMBOL in data folder
    """
    data_path = os.path.join(os.getcwd(),'data')
    allsymbols = [f[0:-4] for f in listdir(data_path) if isfile(os.path.join(data_path, f)) and f.endswith('.csv')]
    allsymbols.sort()
    return allsymbols
