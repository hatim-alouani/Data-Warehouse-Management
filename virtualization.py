import matplotlib.pyplot as plt
from cassandra.cluster import Cluster
import pandas as pd

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace('retail_data')

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="numpy")


def fetch_table_data(table_name):
    query = f"SELECT * FROM {table_name};"
    rows = session.execute(query)
    return pd.DataFrame(rows, columns=rows.column_names)

def plot_sales_by_product(sales_data):
    if 'Order Date' not in sales_data.columns:
        return
    try:
        sales_data['Order Date'] = pd.to_datetime(sales_data['Order Date'], format='%m/%d/%Y %H:%M', errors='coerce')
    except Exception as e:
        return
    invalid_dates = sales_data[sales_data['Order Date'].isna()]
    sales_data = sales_data.dropna(subset=['Order Date'])
    if 'Total Prices' not in sales_data.columns:
        print("Error: 'Total Prices' column not found.")
        return
    product_sales = sales_data.groupby('Product')['Total Prices'].sum().sort_values(ascending=False)
    if product_sales.empty:
        return
    plt.figure(figsize=(10, 6))
    product_sales.plot(kind='bar', color='skyblue')
    plt.title('Total Sales by Product')
    plt.xlabel('Product')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('virtualizations/total_sales_by_product.png')
    plt.close()

def plot_monthly_sales_comparison(monthly_sales_data):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December']
    total_sales = [data['Total Prices'].sum() for data in monthly_sales_data]
    plt.figure(figsize=(10, 6))
    plt.plot(months, total_sales, marker='o', color='b')
    plt.title('Total Sales by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('virtualizations/monthly_sales_comparison.png')
    plt.close()

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
        'august', 'september', 'october', 'november', 'december']
monthly_sales_data = [fetch_table_data(month) for month in months]

for month_data in monthly_sales_data:
    plot_sales_by_product(month_data)

plot_monthly_sales_comparison(monthly_sales_data)
