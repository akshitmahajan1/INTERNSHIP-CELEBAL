import pandas as pd

def load_data(path='data/online_retail_II.xlsx'):
    df = pd.read_excel(path, sheet_name='Year 2010-2011')
    df.dropna(subset=['Customer ID'], inplace=True)
    df = df[df['Quantity'] > 0]
    df['TotalPrice'] = df['Quantity'] * df['Price']
    return df

def get_rfm(df):
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'Invoice': 'nunique',
        'TotalPrice': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    return rfm