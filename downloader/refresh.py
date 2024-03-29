import datetime
import csv
from pandas_datareader import data as web


start_date = datetime.datetime(1980, 10, 1)
end_date = datetime.datetime.now()
source = 'yahoo'

try_time = 5

# symbol_files = ['amex.csv', 'nasdaq.csv', 'nyse.csv', 'additional.csv']
#
# for one_file in symbol_files:
#     with open(one_file) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             symbol = row['Symbol']
#
#             for i in xrange(try_time):
#                 try:
#                     sp500 = web.DataReader(symbol, source, start=start_date, end=end_date)
#                     sp500.to_csv('../data/'+symbol+'.csv')
#                     break
#                 except:
#                     print '{} times in downloading:{}'.format(i+1, symbol)
#             # print symbol


symbol_files = ['nasdaqlisted.txt','otherlisted.txt']
"""
NASDAQ makes this information available via FTP and they update it every night. Log into ftp.nasdaqtrader.com
anonymously. Look in the directory SymbolDirectory. You'll notice two files: nasdaqlisted.txt and otherlisted.txt.
These two files will give you the entire list of tradeable symbols, where they are listed, their name/description,
and an indicator as to whether they are an ETF.

Given this list, which you can pull each night, you can then query Yahoo to obtain the necessary data to calculate
your statistics.
"""

for one_file in symbol_files:
    with open(one_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            if one_file == 'nasdaqlisted.txt':
                symbol = row['Symbol']
            else:
                symbol = row['ACT Symbol']

            try:
                sp500 = web.DataReader(symbol, source, start=start_date, end=end_date, retry_count=try_time)
                sp500.to_csv('./data/'+symbol+'.csv')
            except:
                print '{} times in downloading:{}'.format(try_time, symbol)
            # print symbol
