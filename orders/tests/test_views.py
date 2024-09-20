from django.test import TestCase
from django.urls import reverse
from books.models import Cart, Catalog
from django.contrib.auth.models import User
from orders.models import Order, OrderItem

class CreateOrderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_order_with_empty_cart(self):
        # Adding the required purchased_books and total_price to the POST data
        response = self.client.post(reverse('create_order'), {
            'purchased_books': [],  # Empty cart scenario
            'total_price': 0  # Total price is 0
        })
        self.assertRedirects(response, reverse('cart_view'))
        self.assertEqual(response.wsgi_request._messages._queued_messages[0].message, "Your cart is empty.")

    def test_create_order_success(self):
        # Create cart items for the user
        book = Catalog.objects.create(title="Test Book", price=10.00)
        Cart.objects.create(user=self.user, book=book, quantity=1)

        # Adding the required purchased_books and total_price to the POST data
        response = self.client.post(reverse('create_order'), {
            'purchased_books': ['Test Book'],
            'total_price': 10.00
        })

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(Order.objects.first().total_price, 10.00)

    def test_order_history(self):
        # Create some orders
        Order.objects.create(user=self.user, total_price=20.00)
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order #')
