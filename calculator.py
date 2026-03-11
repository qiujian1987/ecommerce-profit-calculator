# 跨境电商利润计算器

"""
跨境电商利润计算器
支持多平台费率计算，帮助卖家快速分析利润
"""

import json
from typing import Dict, List, Optional

# 平台费率配置
PLATFORM_RATES = {
    'amazon': {
        'referral_fee': 0.15,  # 15% 佣金
        'fba_fulfillment': {'base': 3.22, 'per_kg': 0.45},
        'storage_fee': {'monthly': 0.87, 'per_cu_ft': 0.53},
        'closing_fee': 1.80
    },
    'shopify': {
        'payment_fee': 0.029,  # 2.9% 支付费
        'monthly_fee': 29,
        'transaction_fee': 0.30
    },
    'tiktok': {
        'commission_fee': 0.05,  # 5% 佣金
        'payment_fee': 0.029,
        'shipping_fee': 3.0
    },
    'temu': {
        'commission_fee': 0.15,  # 15% 佣金
        'payment_fee': 0.025
    }
}

def calculate_profit(
    platform: str,
    cost_price: float,
    selling_price: float,
    weight: float = 0,
    shipping_cost: float = 0,
    quantity: int = 1
) -> Dict:
    """
    计算利润

    Args:
        platform: 平台名称 (amazon, shopify, tiktok, temu)
        cost_price: 成本价
        selling_price: 售价
        weight: 商品重量(kg)
        shipping_cost: 物流成本
        quantity: 数量

    Returns:
        利润详情字典
    """
    platform = platform.lower()
    rates = PLATFORM_RATES.get(platform, PLATFORM_RATES['temu'])

    total_revenue = selling_price * quantity
    total_cost = cost_price * quantity

    # 计算平台费用
    fees = {}

    if platform == 'amazon':
        # Amazon FBA 费用
        fees['referral_fee'] = total_revenue * rates['referral_fee']
        fees['fulfillment_fee'] = (rates['fba_fulfillment']['base'] +
                                   rates['fba_fulfillment']['per_kg'] * weight) * quantity
        fees['closing_fee'] = rates['closing_fee'] * quantity

    elif platform == 'shopify':
        fees['payment_fee'] = total_revenue * rates['payment_fee'] + rates['transaction_fee']
        fees['monthly_fee'] = rates['monthly_fee'] / 30  # 按天分摊

    elif platform == 'tiktok':
        fees['commission_fee'] = total_revenue * rates['commission_fee']
        fees['payment_fee'] = total_revenue * rates['payment_fee']
        fees['shipping_fee'] = rates['shipping_fee'] * quantity

    else:  # temus 和其他平台
        fees['commission_fee'] = total_revenue * rates['commission_fee']
        fees['payment_fee'] = total_revenue * rates['payment_fee']

    # 总费用
    total_fees = sum(fees.values())
    total_expenses = total_cost + shipping_cost + total_fees

    # 利润计算
    profit = total_revenue - total_expenses
    profit_margin = (profit / total_revenue) * 100 if total_revenue > 0 else 0

    # 盈亏平衡点
    break_even_price = (total_cost + total_fees) / quantity if quantity > 0 else 0

    return {
        'platform': platform,
        'revenue': round(total_revenue, 2),
        'cost': round(total_cost, 2),
        'shipping': round(shipping_cost, 2),
        'fees': {k: round(v, 2) for k, v in fees.items()},
        'total_fees': round(total_fees, 2),
        'total_expenses': round(total_expenses, 2),
        'profit': round(profit, 2),
        'profit_margin': round(profit_margin, 2),
        'break_even_price': round(break_even_price, 2)
    }


def batch_calculate(items: List[Dict]) -> List[Dict]:
    """
    批量计算多个商品的利润
    """
    results = []
    for item in items:
        result = calculate_profit(
            platform=item.get('platform', 'temu'),
            cost_price=item.get('cost_price', 0),
            selling_price=item.get('selling_price', 0),
            weight=item.get('weight', 0),
            shipping_cost=item.get('shipping_cost', 0),
            quantity=item.get('quantity', 1)
        )
        result['product_name'] = item.get('name', 'Unknown')
        results.append(result)
    return results


def compare_platforms(
    cost_price: float,
    selling_price: float,
    weight: float = 0,
    shipping_cost: float = 0
) -> Dict:
    """
    对比不同平台的利润
    """
    comparison = {}
    for platform in PLATFORM_RATES.keys():
        result = calculate_profit(
            platform=platform,
            cost_price=cost_price,
            selling_price=selling_price,
            weight=weight,
            shipping_cost=shipping_cost
        )
        comparison[platform] = {
            'profit': result['profit'],
            'profit_margin': result['profit_margin'],
            'total_fees': result['total_fees']
        }

    # 找出利润最高的平台
    best_platform = max(comparison.items(), key=lambda x: x[1]['profit'])

    return {
        'comparison': comparison,
        'best_platform': best_platform[0],
        'best_profit': best_platform[1]['profit']
    }


def main():
    """命令行交互界面"""
    print("=" * 50)
    print("跨境电商利润计算器")
    print("=" * 50)

    # 示例计算
    print("\n示例：Amazon 平台利润计算")
    result = calculate_profit(
        platform='amazon',
        cost_price=30,
        selling_price=59.99,
        weight=0.3,
        shipping_cost=5
    )

    print(f"\n收入: ${result['revenue']}")
    print(f"成本: ${result['cost']}")
    print(f"平台费用:")
    for fee, amount in result['fees'].items():
        print(f"  - {fee}: ${amount}")
    print(f"总费用: ${result['total_fees']}")
    print(f"\n净利润: ${result['profit']}")
    print(f"利润率: {result['profit_margin']}%")
    print(f"盈亏平衡价: ${result['break_even_price']}")

    # 平台对比
    print("\n" + "=" * 50)
    print("平台利润对比")
    print("=" * 50)
    comparison = compare_platforms(
        cost_price=30,
        selling_price=59.99,
        weight=0.3,
        shipping_cost=5
    )

    for platform, data in comparison['comparison'].items():
        print(f"\n{platform.upper()}:")
        print(f"  利润: ${data['profit']}")
        print(f"  利润率: {data['profit_margin']}%")
        print(f"  总费用: ${data['total_fees']}")

    print(f"\n推荐平台: {comparison['best_platform'].upper()}")


if __name__ == '__main__':
    main()
