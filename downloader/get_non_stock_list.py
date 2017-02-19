import datetime
import csv
from pandas_datareader import data as web


symbol_files = ['./downloader/nasdaqlisted.txt','./downloader/otherlisted.txt']

with open('./downloader/etf_etn.csv', 'w') as fout:
    w = csv.DictWriter(fout, ['Symbol','ETF'])
    w.writeheader()

    for one_file in symbol_files:
        with open(one_file) as fin:
            reader = csv.DictReader(fin, delimiter='|')
            for row in reader:
                if one_file == './downloader/nasdaqlisted.txt':
                    symbol = row['Symbol']
                    security_name = row['Security Name']
                    is_etf = row['ETF']
                else:
                    symbol = row['ACT Symbol']
                    security_name = row['Security Name']
                    is_etf = row['ETF']

                # if etf or etn, write to file
                if is_etf == 'Y' or ' ETN' in security_name: # ETN is a key word
                    w.writerow({'Symbol': symbol, 'ETF': 'Y' if is_etf == 'Y' else 'N'})
