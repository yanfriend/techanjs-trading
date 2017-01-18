import datetime
import csv
from pandas_datareader import data as web
import os

start_date = datetime.datetime(1980, 10, 1)
end_date = datetime.datetime.now()
source = 'yahoo'

try_time = 5

folder = '../data'

# for file in ['IBM.csv']:
for file in os.listdir(folder):
    if file.endswith(".csv"):
        with open(os.path.join(folder, file)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pass
            # now row is the last line.
            start_date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d') + datetime.timedelta(days=1)

            try:
                symbol_data = web.DataReader(file[0:-4], source, start=start_date, end=end_date, retry_count=try_time)
            except:
                print '{} times in downloading:{}'.format(try_time, file[0:-4])
                continue

        with open(os.path.join(folder, file), 'a') as f:
            symbol_data.to_csv(f, header=False)
