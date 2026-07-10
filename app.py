#!/usr/bin/env python3
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated in-memory database array with seed data
inventory_db = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "quantity": 50,
        "price": 3.99
    }
]
current_id = 1

@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    return jsonify(inventory_db), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route('/inventory', methods=['POST'])
def create_item():
    global current_id
    data = request.get_json() or {}
    if "product_name" not in data:
        return jsonify({"error": "Missing required field: product_name"}), 400
        
    current_id += 1
    new_item = {
        "id": current_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", "Unknown"),
        "ingredients_text": data.get("ingredients_text", "N/A"),
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0.0)
    }
    inventory_db.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json() or {}
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])
    if "price" in data:
        item["price"] = float(data["price"])
    if "product_name" in data:
        item["product_name"] = data["product_name"]
        
    return jsonify(item), 200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory_db
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    inventory_db = [i for i in inventory_db if i["id"] != item_id]
    return jsonify({"message": f"Successfully deleted item {item_id}"}), 200

@app.route('/api/external/fetch', methods=['GET'])
def fetch_external_product():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "Barcode parameter is required"}), 400
        
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            api_data = response.json()
            if api_data.get("status") == 1:
                prod = api_data.get("product", {})
                extracted = {
                    "product_name": prod.get("product_name", "Unknown External Item"),
                    "brands": prod.get("brands", "Unknown Brand"),
                    "ingredients_text": prod.get("ingredients_text", "No ingredients provided.")
                }
                return jsonify(extracted), 200
            return jsonify({"error": "Product not found in OpenFoodFacts database"}), 404
    except requests.exceptions.RequestException:
        return jsonify({"error": "External API service unavailable"}), 503
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
