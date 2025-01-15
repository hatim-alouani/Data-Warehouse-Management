from flask import Flask, render_template, request, redirect, url_for
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster()
session = cluster.connect('retail_data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        query = "SELECT * FROM product_info WHERE product = %s"
        existing_product = session.execute(query, (product_name,)).one()

        if existing_product:
            return render_template('add_product.html', message="Product already exists.")

        query = "INSERT INTO product_info (product, price, quantity) VALUES (%s, %s, %s)"
        session.execute(query, (product_name, price, quantity))
        return redirect(url_for('index'))

    return render_template('add_product.html')


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        product_name = request.form['product']

        query = "SELECT * FROM product_info WHERE product = %s"
        existing_product = session.execute(query, (product_name,)).one()

        if not existing_product:
            return render_template('delete_product.html', message="Product does not exist.")

        query = "DELETE FROM product_info WHERE product = %s"
        session.execute(query, (product_name,))
        return redirect(url_for('index'))

    return render_template('delete_product.html')


@app.route('/update_quantity', methods=['GET', 'POST'])
def update_quantity():
    if request.method == 'POST':
        product_name = request.form['product']
        quantity = int(request.form['quantity'])

        query_check = "SELECT * FROM product_info WHERE product = %s"
        result = session.execute(query_check, (product_name,))
        
        if not result:
            message = "Product not found!"
            return render_template('update_quantity.html', message=message)

        query_update = "UPDATE product_info SET quantity = %s WHERE product = %s"
        session.execute(query_update, (quantity, product_name))

        message = "Quantity updated successfully!"
        return render_template('update_quantity.html', message=message)

    return render_template('update_quantity.html')


@app.route('/update_price', methods=['GET', 'POST'])
def update_price():
    if request.method == 'POST':
        product_name = request.form['product']
        price = float(request.form['price'])

        query_check = "SELECT * FROM product_info WHERE product = %s"
        product = session.execute(query_check, (product_name,)).one()

        if not product:
            message = "Product not found!"
            return render_template('update_price.html', message=message)

        query = "UPDATE product_info SET price = %s WHERE product = %s"
        session.execute(query, (price, product_name))

        message = "Price updated successfully!"
        return render_template('update_price.html', message=message)

    return render_template('update_price.html')



@app.route('/show_products')
def show_products():
    query = "SELECT product, price, quantity FROM product_info"
    rows = session.execute(query)

    products = [{"product": row.product, "price": row.price, "quantity": row.quantity} for row in rows]
    
    return render_template('show_products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
