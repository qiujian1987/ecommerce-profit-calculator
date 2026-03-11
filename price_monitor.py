import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

class PriceMonitor:
    """跨境电商价格监控器"""
    
    def __init__(self):
        self.history = {}
    
    def track_product(self, product_id, platform, current_price):
        """记录产品价格"""
        if product_id not in self.history:
            self.history[product_id] = []
        
        self.history[product_id].append({
            'timestamp': datetime.now().isoformat(),
            'platform': platform,
            'price': current_price
        })
        
        return self.get_price_trend(product_id)
    
    def get_price_trend(self, product_id):
        """获取价格趋势"""
        if product_id not in self.history:
            return None
        
        history = self.history[product_id]
        if len(history) < 2:
            return {'trend': 'insufficient_data', 'change_percent': 0}
        
        prices = [h['price'] for h in history]
        avg_price = sum(prices) / len(prices)
        latest_price = prices[-1]
        first_price = prices[0]
        
        change_percent = ((latest_price - first_price) / first_price) * 100
        
        if change_percent > 5:
            trend = 'up'
        elif change_percent < -5:
            trend = 'down'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change_percent': round(change_percent, 2),
            'avg_price': round(avg_price, 2),
            'latest_price': latest_price,
            'first_price': first_price,
            'data_points': len(history)
        }
    
    def check_competitor_prices(self, products):
        """批量检查竞品价格（模拟）"""
        results = []
        for product in products:
            result = self.track_product(
                product['id'],
                product['platform'],
                product['price']
            )
            results.append({
                'product': product['name'],
                'trend': result
            })
        return results
    
    def suggest_optimal_price(self, cost_price, platform, competitor_prices=None):
        """建议最优售价"""
        from calculator import PLATFORM_RATES
        
        rates = PLATFORM_RATES.get(platform, PLATFORM_RATES['amazon'])
        
        # 基础利润率目标
        target_margin = 0.25  # 25%
        
        # 根据竞品价格调整
        if competitor_prices:
            avg_competitor = sum(competitor_prices) / len(competitor_prices)
            # 建议比竞品低5%或成本+目标利润率，取较高者
            suggested_from_competitor = avg_competitor * 0.95
        else:
            suggested_from_competitor = float('inf')
        
        # 从成本计算
        if platform == 'amazon':
            fee_rate = 0.15 + 0.05  # 佣金+其他费用估算
        elif platform == 'shopify':
            fee_rate = 0.029 + 0.02  # 支付费+估算
        elif platform == 'tiktok':
            fee_rate = 0.05 + 0.029
        else:  # temu
            fee_rate = 0.15 + 0.025
        
        # 目标售价 = 成本 / (1 - 目标利润率 - 费用率)
        suggested_from_cost = cost_price / (1 - target_margin - fee_rate)
        
        # 取较高者，但不超过竞品的1.1倍
        optimal_price = max(suggested_from_cost, suggested_from_competitor * 0.9)
        if competitor_prices:
            optimal_price = min(optimal_price, avg_competitor * 1.1)
        
        return {
            'optimal_price': round(optimal_price, 2),
            'expected_margin': round(target_margin * 100, 1),
            'based_on': 'competitor' if suggested_from_competitor != float('inf') else 'cost',
            'competitor_avg': round(sum(competitor_prices)/len(competitor_prices), 2) if competitor_prices else None
        }


if __name__ == '__main__':
    # 示例使用
    monitor = PriceMonitor()
    
    # 模拟历史价格数据
    monitor.track_product('prod_001', 'amazon', 59.99)
    time.sleep(0.1)
    monitor.track_product('prod_001', 'amazon', 54.99)
    time.sleep(0.1)
    monitor.track_product('prod_001', 'amazon', 49.99)
    
    trend = monitor.get_price_trend('prod_001')
    print(f"价格趋势: {trend}")
    
    # 建议最优售价
    suggestion = monitor.suggest_optimal_price(
        cost_price=30,
        platform='amazon',
        competitor_prices=[55, 52, 58, 60]
    )
    print(f"\n最优售价建议: {suggestion}")
