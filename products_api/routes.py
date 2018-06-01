from flask import Flask, jsonify, render_template, flash, redirect, url_for, request
import pytest

from products_api import app
from products_api.db import (
    all_products,
    find_product,
    is_valid_price,
    auto_incremented_id,
    write_products_to_file
)

#
# HOME
#

@app.route('/')
def index():
    app.logger.info("INDEX")
    return render_template('index.html')

@app.route('/hello')
def hello(name=None):
    app.logger.info("HELLO")
    if "name" in request.args:
        name = request.args["name"]
    return render_template('hello.html', name=name)

#
# PRODUCTS
#

# GET /products
@app.route('/products')
@app.route('/products.json')
def list_products():
    app.logger.info("LIST PRODUCTS")
    products = all_products()
    return jsonify(products)

# GET /products/:id
@app.route('/products/<int:id>')
@app.route('/products/<int:id>.json')
def show_product(id):
    app.logger.info(f"SHOW PRODUCT {id}")
    product = find_product(id)
    if product == None:
        flash( f"Oops, couldn't find a product with an identifier of {id}. Please try again.", "error")
        return redirect(url_for('index'))
    else:
        return jsonify(product)

# POST /products
@app.route('/products', methods=["POST"])
@app.route('/products.json', methods=["POST"])
def create_product():
    app.logger.info("CREATE PRODUCT")
    #app.logger.info("HEADERS")
    #app.logger.info(request.headers)
    #app.logger.info("FORM")
    #app.logger.info(request.form)
    #app.logger.info("JSON DATA")
    #json_data = request.get_json(force=True)
    #app.logger.info(json_data)

    ##pytest.set_trace()

    #new_product = {
    #    "name": request.form.get("name"),
    #    "aisle": request.form.get("aisle"),
    #    "department": request.form.get("department"),
    #    "price": request.form.get("price")
    #}
    new_product = request.get_json()
    app.logger.info("NEW PRODUCT")
    app.logger.info(new_product)

    if is_valid_price(new_product["price"]) == False:
        flash( f"OOPS. That product price ({new_product['price']}) is not valid. Expecting a price like 4.99 or 0.77. Please try again.", "error")
        return redirect(url_for('index'))
    else:
        products = all_products()
        new_product["id"] = auto_incremented_id(products)
        products.append(new_product)
        write_products_to_file(products=products)
        return jsonify(new_product)
