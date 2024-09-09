from django.test import TestCase
from django.urls import reverse
from books.models import Catalog, Cart, Price, Category
from django.contrib.auth.models import User
from decimal import Decimal

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='AlexBooks', password='SimplePasswordTest')
        self.category = Category.objects.create(name="Fiction")
        self.book = Catalog.objects.create(title="1984", author="George Orwell", category=self.category) # Creating a test book (Catalog) and associate it with the created category
        Price.objects.create(book=self.book, amount=Decimal('10.99')) # Create an associated price for book

    def test_add_cart(self):
        self.client.login(username='AlexBooks', password='SimplePasswordTest')
        response = self.client.post(reverse('add_to_cart', args=[self.book.id])) # Add the book to cart
        self.assertRedirects(response, reverse('cart_view')) # Verify that the user is redirected to cart view
        self.assertTrue(Cart.objects.filter(user=self.user, book=self.book).exists()) # Check if the book is in users cart

    def test_remove_from_cart(self):
        self.client.login(username='AlexBooks', password='SimplePasswordTest')
        Cart.objects.create(user=self.user, book=self.book, quantity=1) #Add the book to cart initially
        response = self.client.post(reverse('remove_from_cart', args=[self.book.id])) # remove book
        self.assertRedirects(response, reverse('cart_view')) #  user is redirected to cart view
        self.assertFalse(Cart.objects.filter(user=self.user, book=self.book).exists()) # Checking if book is removed from users cart
