import pandas as pd
from data_manager import load_records

def dataframe(): return pd.DataFrame(load_records(),columns=['date','location','category','quantity'])
def filter_records(search=''):
    rows=load_records(); s=search.lower()
    if not s: return rows
    return [r for r in rows if s in r['date'].lower() or s in r['location'].lower() or s in r['category'].lower()]
def get_summary():
    df=dataframe()
    if df.empty: return {'total':0,'average':0,'count':0}
    a=df['quantity'].to_numpy(); return {'total':a.sum(),'average':a.mean(),'count':len(a)}
def high_waste_areas():
    df=dataframe()
    if df.empty: return []
    return list(df.groupby('location')['quantity'].sum().sort_values(ascending=False).items())
def category_totals():
    df=dataframe(); return pd.Series(dtype=float) if df.empty else df.groupby('category')['quantity'].sum().sort_values(ascending=False)
def location_totals():
    df=dataframe(); return pd.Series(dtype=float) if df.empty else df.groupby('location')['quantity'].sum().sort_values(ascending=False)
