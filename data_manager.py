import csv, os
from datetime import datetime
DATA_FILE='waste_records.csv'
FIELDS=['date','location','category','quantity']

def ensure_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE,'w',newline='',encoding='utf-8') as f: csv.DictWriter(f,fieldnames=FIELDS).writeheader()

def load_records():
    ensure_file()
    with open(DATA_FILE,'r',newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    for r in rows: r['quantity']=float(r['quantity'])
    return rows

def validate(date,location,category,quantity):
    try: datetime.strptime(date,'%Y-%m-%d')
    except ValueError: raise ValueError('Date must be in YYYY-MM-DD format.')
    if not location: raise ValueError('Location cannot be empty.')
    if not category: raise ValueError('Category cannot be empty.')
    try: q=float(quantity)
    except ValueError: raise ValueError('Quantity must be a number.')
    if q<=0: raise ValueError('Quantity must be greater than 0.')
    return q

def add_record(date,location,category,quantity):
    q=validate(date,location,category,quantity); ensure_file()
    with open(DATA_FILE,'a',newline='',encoding='utf-8') as f:
        csv.DictWriter(f,fieldnames=FIELDS).writerow({'date':date,'location':location,'category':category,'quantity':q})
