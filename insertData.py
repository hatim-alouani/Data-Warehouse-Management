from threading import Thread
from cassandra.cluster import Cluster
import pandas as pd

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace('retail_data')

months = [
    ('january', 'hdfs://localhost:9000/processed_datasets/data_Sales_January_2019.csv'),
    ('february', 'hdfs://localhost:9000/processed_datasets/data_Sales_February_2019.csv'),
    ('march', 'hdfs://localhost:9000/processed_datasets/data_Sales_March_2019.csv'),
    ('april', 'hdfs://localhost:9000/processed_datasets/data_Sales_April_2019.csv'),
    ('may', 'hdfs://localhost:9000/processed_datasets/data_Sales_May_2019.csv'),
    ('june', 'hdfs://localhost:9000/processed_datasets/data_Sales_June_2019.csv'),
    ('july', 'hdfs://localhost:9000/processed_datasets/data_Sales_July_2019.csv'),
    ('august', 'hdfs://localhost:9000/processed_datasets/data_Sales_August_2019.csv'),
    ('september', 'hdfs://localhost:9000/processed_datasets/data_Sales_September_2019.csv'),
    ('october', 'hdfs://localhost:9000/processed_datasets/data_Sales_October_2019.csv'),
    ('november', 'hdfs://localhost:9000/processed_datasets/data_Sales_November_2019.csv'),
    ('december', 'hdfs://localhost:9000/processed_datasets/data_Sales_December_2019.csv')
]

def clean_months_data(data):
    data = data.dropna().drop_duplicates()
    data = data.dropna(subset=['Price Each'])
    data['Order ID'] = pd.to_numeric(data['Order ID'], errors='coerce', downcast='float')\
        .dropna().astype(float)
    data['Quantity Ordered'] = pd.to_numeric(data['Quantity Ordered'], errors='coerce')\
        .dropna().astype(int)
    data['Price Each'] = pd.to_numeric(data['Price Each'], errors='coerce', downcast='float')\
        .dropna().astype(float)
    data['Total Prices'] = data['Quantity Ordered'] * data['Price Each']
    return data

def insert_monthly_sales_data(month, file_path):
    print(f"Processing data for {month.capitalize()}...")
    monthly_data = pd.read_csv(file_path)
    monthly_data = clean_months_data(monthly_data)
    table_name = month
    for index, row in monthly_data.iterrows():
        query = f"""
        INSERT INTO {table_name} ("Order ID", "Order Date", "Price Each", "Product", "Purchase Address",
            "Quantity Ordered", "Total Prices")
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        session.execute(query, (row['Order ID'], row['Order Date'], row['Price Each'], row['Product'],
                                row['Purchase Address'], row['Quantity Ordered'], row['Total Prices']))
    print(f"Data for {month.capitalize()} inserted successfully.")

monthly_threads = []
for month, file_path in months:
    thread = Thread(target=insert_monthly_sales_data, args=(month, file_path))
    monthly_threads.append(thread)

for thread in monthly_threads:
    thread.start()

for thread in monthly_threads:
    thread.join()

session.shutdown()
cluster.shutdown()
print("Data insertion complete.")
