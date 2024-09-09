from .models import Stock

def check_low_stock():
    low_stock_items = Stock.objects.filter(quantity__lte=Stock.LOW_STOCK_THRESHOLD)
    return low_stock_items