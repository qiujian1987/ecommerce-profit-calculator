# 🛒 跨境电商利润计算器

> 帮跨境卖家一键算清真实利润，不再亏本卖货！

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/qiujian1987/ecommerce-profit-calculator)](https://github.com/qiujian1987/ecommerce-profit-calculator/stargazers)

## 📌 为什么选择这个工具？

| 痛点 | 我们的解决方案 |
|------|---------------|
| 平台费用太复杂 | 8种费用自动计算 |
| 不知道哪个平台赚钱 | 一键对比4大平台 |
| 算错价格亏本 | 盈亏平衡自动分析 |

## ⚡ 快速开始

```python
from calculator import calculate_profit

result = calculate_profit(
    platform='amazon',
    cost_price=50,
    selling_price=99,
    weight=0.5
)

print(f"净利润: ${result['profit']}")
print(f"利润率: {result['profit_margin']}%")
```

## 🎯 核心功能

### ✅ 多平台支持
- Amazon FBA/FBM
- Shopify
- TikTok Shop
- Temu
- Shopee
- Lazada

### 📊 智能分析
- 佣金计算
- 物流费用
- 盈亏平衡点
- 多平台对比

### 🔄 批量处理
```python
from calculator import batch_calculate

items = [
    {'name': '商品A', 'platform': 'amazon', 'cost_price': 30, 'selling_price': 59.99},
    {'name': '商品B', 'platform': 'tiktok', 'cost_price': 25, 'selling_price': 49.99}
]

results = batch_calculate(items)
```

## 📈 示例输出

```
平台利润对比:
┌──────────┬─────────┬──────────┐
│ Platform │  Profit │   Margin │
├──────────┼─────────┼──────────┤
│ Amazon   │  $10.84 │  18.06%  │
│ Shopify  │  $21.98 │  36.65%  │ ⭐
│ TikTok   │  $17.25 │  28.76%  │
│ Temu     │  $14.49 │  24.16%  │
└──────────┴─────────┴──────────┘

推荐: Shopify (利润最高)
```

## 🛠️ 安装使用

### 在线使用 ⭐推荐
直接访问: https://qiujian1987.github.io/ecommerce-profit-calculator

### 本地运行

```bash
git clone https://github.com/qiujian1987/ecommerce-profit-calculator.git
cd ecommerce-profit-calculator

# Python版本
pip install -r requirements.txt
python calculator.py

# 或直接打开 index.html 使用网页版
```

## 🚀 API服务（新功能！）

无需安装，直接调用API：

```bash
# 计算利润
curl -X POST https://api.example.com/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "amazon",
    "cost_price": 30,
    "selling_price": 59.99,
    "weight": 0.3
  }'
```

**免费额度**: 100次/天  
**商业合作**: 联系开通高级API

### 本地运行API

```bash
pip install -r requirements.txt
python api_server.py

# 访问 http://localhost:5000
```

### 📈 价格监控与优化（新功能！）
```python
from price_monitor import PriceMonitor

monitor = PriceMonitor()

# 追踪价格变化
monitor.track_product('prod_001', 'amazon', 59.99)
trend = monitor.get_price_trend('prod_001')

# 智能定价建议
suggestion = monitor.suggest_optimal_price(
    cost_price=30,
    platform='amazon',
    competitor_prices=[55, 52, 58, 60]
)

print(f"建议售价: ¥{suggestion['optimal_price']}")
print(f"预期利润率: {suggestion['expected_margin']}%")
```

## 📄 License

MIT License

---

**觉得有用？点个 ⭐ 支持一下！**

[![Star](https://img.shields.io/badge/⭐-Star-blue)](https://github.com/qiujian1987/ecommerce-profit-calculator)
