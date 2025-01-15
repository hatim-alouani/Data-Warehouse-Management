from cassandra.cluster import Cluster
from threading import Thread

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('retail_data')

create_table_query = """
CREATE TABLE IF NOT EXISTS product_info (
    product TEXT PRIMARY KEY,
    price DOUBLE,
    quantity INT
);
"""
session.execute(create_table_query)

months = [
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
    'october', 'november', 'december'
]

def product_exists(product_name):
    query = "SELECT COUNT(*) FROM product_info WHERE product = %s"
    result = session.execute(query, (product_name,))
    return result[0].count > 0

def insert_product(product_name, price_each):
    print(f"Inserting product {product_name} into product_info table...")
    query = """
    INSERT INTO product_info (product, price, quantity)
    VALUES (%s, %s, %s)
    """
    session.execute(query, (product_name, price_each, 100))

def process_month_data(month):
    query = f"""
    SELECT "Product", "Price Each"
    FROM {month}
    """
    result = session.execute(query)
    
    for row in result:
        product_name = row[0]
        price_each = row[1]

        if not product_exists(product_name):
            insert_product(product_name, price_each)
        else:
            print(f"Product {product_name} already exists in product_info table.")

threads = []

for month in months:
    thread = Thread(target=process_month_data, args=(month,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

query = "DELETE FROM product_info WHERE product = %s"
session.execute(query, ('Product',))

print("Data insertion complete.")
session.shutdown()
cluster.shutdown()
