import flask
from app import app
from flask import render_template, redirect, url_for, request, send_from_directory
import os
from app.models.product import Product
from app.services.ProductsService import ProductsService

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        if product_id != '':
            try:    
                product = Product(product_id)
                product.extract_product().process_stats().draw_charts()
                product.save_stats()
                product.save_opinions()
                return redirect(url_for("product", product_id=product_id))

            except Exception as e:
                print('ERROR', e)
                return render_template("extract.html.jinja", error='Produkt nie istnieje w Ceneo')

    return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = ProductsService().get_products()
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id): 

    product = Product(product_id)
    product.load_product()
    opinions = product.opinions_to_df()
    stats = product.stats_to_dict()
    stats_labels = product.stats_labels()
    return render_template("product.html.jinja", stats=stats, product_id=product_id, opinions=opinions, stats_labels=stats_labels)


@app.route('/open/<product_id>', methods=['GET'])
def open(product_id): 
    # from pathlib import Path
    # root = Path('.')
    # folder_path = Path.cwd() / '/app/opinions'
    # print('folder_path', folder_path)
    # TODO get full path 
    folder_path = '/Users/kamilakapinos/dev/CeneoWebScraper/app/opinions'
    return send_from_directory(folder_path, product_id + '.json', as_attachment=True) 

