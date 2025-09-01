import csv
from aiven import get_rows,get_broker,get_stock,get_stock_partial
from download_bhav_copy import bhav_main
csv_file="/tmp/price.csv"
def get_price(data,rows):

    for var in data:
        found = False
        for row in rows:
            if len(row) > 3 and row[1] == var['NSEKEY']:
                var['price'] = row[3].strip()
                found = True
                break
        if not found:
            var['price'] = " " 


def load_price():
    bhav_main()
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Read all rows into a list
            return rows,"succes"
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' does not exist.")
        return [],"Failed"
    except Exception as e:
        print(f"Unexpected error while reading '{csv_file}': {e}")
        return [],"failed"

def get_date(rows):
    for i in rows:
        if len(i) != 0:
            return (i[1])

