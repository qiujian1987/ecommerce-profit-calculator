from flask import Flask, request, jsonify
from flask_limiter import Limiter
from calculator import calculate_profit, batch_calculate, compare_platforms
import os

app = Flask(__name__)

# 限流：免费用户100次/天
limiter = Limiter(
    app=app,
    key_func=lambda: request.headers.get("X-API-Key", request.remote_addr),
    default_limits=["100 per day"]
)

@app.route('/')
def home():
    return {
        "name": "跨境电商利润计算器 API",
        "version": "1.0",
        "endpoints": {
            "/calculate": "计算单个商品利润",
            "/batch": "批量计算",
            "/compare": "多平台对比"
        },
        "pricing": {
            "free": "100次/天",
            "premium": "联系开通"
        }
    }

@app.route('/calculate', methods=['POST'])
@limiter.limit("100 per day")
def api_calculate():
    data = request.json
    result = calculate_profit(
        platform=data.get('platform', 'amazon'),
        cost_price=float(data.get('cost_price', 0)),
        selling_price=float(data.get('selling_price', 0)),
        weight=float(data.get('weight', 0)),
        shipping_cost=float(data.get('shipping_cost', 0))
    )
    return jsonify(result)

@app.route('/batch', methods=['POST'])
@limiter.limit("50 per day")
def api_batch():
    items = request.json.get('items', [])
    results = batch_calculate(items)
    return jsonify({"results": results})

@app.route('/compare', methods=['POST'])
@limiter.limit("100 per day")
def api_compare():
    data = request.json
    result = compare_platforms(
        cost_price=float(data.get('cost_price', 0)),
        selling_price=float(data.get('selling_price', 0)),
        weight=float(data.get('weight', 0)),
        shipping_cost=float(data.get('shipping_cost', 0))
    )
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
