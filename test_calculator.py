# 测试用例
import pytest
from calculator import calculate_profit, batch_calculate, compare_platforms

def test_calculate_profit():
    result = calculate_profit(
        platform='amazon',
        cost_price=30,
        selling_price=59.99,
        weight=0.3,
        shipping_cost=5
    )

    assert result['revenue'] == 59.99
    assert result['cost'] == 30
    assert result['profit'] > 0
    assert 'profit_margin' in result
    assert 'fees' in result

def test_compare_platforms():
    result = compare_platforms(
        cost_price=30,
        selling_price=59.99,
        weight=0.3,
        shipping_cost=5
    )

    assert 'comparison' in result
    assert 'best_platform' in result
    assert len(result['comparison']) > 0

def test_batch_calculate():
    items = [
        {
            'name': 'Product A',
            'platform': 'amazon',
            'cost_price': 20,
            'selling_price': 45,
            'weight': 0.2
        },
        {
            'name': 'Product B',
            'platform': 'tiktok',
            'cost_price': 15,
            'selling_price': 35,
            'weight': 0.1
        }
    ]

    results = batch_calculate(items)
    assert len(results) == 2
    assert results[0]['product_name'] == 'Product A'
    assert results[1]['product_name'] == 'Product B'
