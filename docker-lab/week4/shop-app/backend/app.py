from flask import Flask, jsonify
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)

# Подключение к Redis ПО ИМЕНИ
r = redis.Redis(host="redis", port=6379, decode_responses=True)

PRODUCTS = [
  {"id": 1, "name": "Docker T-Shirt", "price": 25},
  {"id": 2, "name": "Kubernetes Mug", "price": 15},
  {"id": 3, "name": "DevOps Book", "price": 40}
]

@app.route("/products")
def products():
    return jsonify(PRODUCTS)

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        r.lpush("cart", json.dumps(product))
    return jsonify({"success": True})

@app.route("/cart")
def get_cart():
    items = [json.loads(x) for x in r.lrange("cart", 0, -1)]
    total = sum(item["price"] for item in items)
    return jsonify({"count": len(items), "total": total, "items": items})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
