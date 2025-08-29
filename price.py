import csv
from aiven import get_rows,get_broker,get_stock,get_stock_partial
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
 with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        # Read all rows into a list for easy lookup
        rows = list(reader)
        return rows
