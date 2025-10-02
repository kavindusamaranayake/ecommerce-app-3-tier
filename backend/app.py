# backend/app.py - Updated to include DELETE endpoint and handle MongoDB ObjectId

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongo:27017/ecommerce'))
db = client.ecommerce
products = db.products

@app.route('/health')
def health():
    return jsonify(status='healthy'), 200

@app.route('/ready')
def ready():
    try:
        products.find_one()  # Test DB connection
        return jsonify(status='ready'), 200
    except:
        return jsonify(status='not ready'), 503

@app.route('/products', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'GET':
        product_list = []
        for product in products.find({}):
            product['_id'] = str(product['_id'])
            product_list.append(product)
        return jsonify(product_list)
    elif request.method == 'POST':
        product = request.json
        result = products.insert_one(product)
        product['_id'] = str(result.inserted_id)
        return jsonify(message='Product added', product=product), 201

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        result = products.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify(message='Product deleted'), 200
        else:
            return jsonify(error='Product not found'), 404
    except:
        return jsonify(error='Invalid ID'), 400

# Metrics endpoint (placeholder)
@app.route('/metrics')
def metrics():
    return jsonify(uptime=42), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
