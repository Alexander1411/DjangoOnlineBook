from books.models import  Catalog
from orders.models import Order, OrderItem

def test_order_model(self):
    order = Order.objects.create(user=self.user, total_price=20.00)
    self.assertEqual(str(order), f'Order #{order.id} - {self.user.username}')

def test_order_item_model(self):
    order = Order.objects.create(user=self.user, total_price=20.00)
    book = Catalog.objects.create(title="Test Book", price=10.00)
    order_item = OrderItem.objects.create(order=order, book=book, quantity=2, price=20.00)
    self.assertEqual(str(order_item), '2 of Test Book')
