import re
from datetime import datetime
from flask import render_template
from flask import Flask
import requests
import json
#from . import ngsiv2

app = Flask(__name__)


base_path = 'http://localhost:1026/v2'

def read_entity(entity_id):
 r = requests.get(base_path + '/entities/' + entity_id)
 return (r.status_code, json.loads(r.text))

def list_entities(type= None, options='count',attrs=None):
    r = requests.get(base_path + '/entities/',params={'options':options, 'type':type, 'attrs':attrs})
    return (r.status_code, json.loads(r.text))

def list_inventory_items_for_product(productid=None):
    r = requests.get(base_path + '/entities/',params={'options':'count', 'type':'InventoryItem', 'q':'refProduct=='+productid, 'attrs':'id'})
    return (json.loads(r.text))

def list_inventory_items_for_store(storeid=None):
    r = requests.get(base_path + '/entities/',params={'options':'count', 'type':'InventoryItem', 'q':'refStore=='+storeid, 'attrs':'id'})
    return (json.loads(r.text))



@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


@app.route("/products/")
def products():
    (status, data) = list_entities(type='Product')
    if status == 200:
        print("ok")
        return render_template("products.html", products = data, product_base_url = "/Product/")


@app.route('/Product/<product_id>')
def display_product(product_id):
    (status, data) = read_entity(product_id)
    inventory_items = list_inventory_items_for_product(product_id)
    if status == 200:
        return render_template('product.html', product = data,inventory_items=inventory_items) 



@app.route("/stores/")
def stores():
    (status, data) = list_entities(type='Store')
    if status == 200:
        return render_template("stores.html", stores = data, store_base_url = "/Store/")



@app.route('/Store/<store_id>')
def display_store(store_id):
    (status, data) = read_entity(store_id)
    inventory_items = list_inventory_items_for_store(store_id)
    if status == 200:
        return render_template('store.html', store= data,inventory_items=inventory_items)

