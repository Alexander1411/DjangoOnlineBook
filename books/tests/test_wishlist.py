from django.test import TestCase
from django.urls import reverse
from books.models import Catalog, Wishlist, Price, Category
from django.contrib.auth.models import User
from decimal import Decimal

class WishlistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='QuickRead', password='QuickPassword0')
        self.category = Category.objects.create(name="Fiction")
        self.book = Catalog.objects.create(title="1984", author="George Orwell", category=self.category) # creating a test book (catalog) and associate it with created category
        Price.objects.create(book=self.book, amount=Decimal('10.99')) ## creating a associated price for book

    def test_add_wishlist(self):
        self.client.login(username='QuickRead', password='QuickPassword0')
        response = self.client.post(reverse('add_to_wishlist', args=[self.book.id])) # Adding book to the wishlist
        self.assertRedirects(response, reverse('wishlist_view')) ## making sure that the user is redirected to the wishlist view
        self.assertTrue(Wishlist.objects.filter(user=self.user, book=self.book).exists()) # Checking if the book is in users wishlist

    def test_remove_wishlist(self):
        self.client.login(username='QuickRead', password='QuickPassword0')
        Wishlist.objects.create(user=self.user, book=self.book) # adding book to the wishlist initially
        response = self.client.post(reverse('remove_from_wishlist', args=[self.book.id])) # Remove book 
        self.assertRedirects(response, reverse('wishlist_view')) # Verifing that user is redirected to wishlist
        self.assertFalse(Wishlist.objects.filter(user=self.user, book=self.book).exists()) # Checking if  book is removed
