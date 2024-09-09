from django.test import TestCase
from django.urls import reverse
from books.models import Catalog, Price, Category
from django.contrib.auth.models import User
from decimal import Decimal


class BookViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction") # Creating a category first, foreign key relationship is satisfied when new catalog object is created : https://docs.djangoproject.com/en/5.1/topics/db/models/#foreignkey
        self.book = Catalog.objects.create( ##Creating Catalog (book) object without the price field
            title="1984",
            author="George Orwell",
            category=self.category  # Link to the category
        )
        
        Price.objects.create( # creating Price object linked to the book
            book=self.book,
            amount=Decimal('10.99') 
        )
        
        self.user = User.objects.create_user(
            username='AmazingReader', 
            password='amazingPassword10'
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_details', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_details.html')
        self.assertContains(response, self.book.title)
