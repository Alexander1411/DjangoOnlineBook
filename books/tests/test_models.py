from django.test import TestCase
from books.models import Category, Catalog, Price
from decimal import Decimal


class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create( # Creating a category first to for foreign key relationship is satisfied when new catalog object is created : https://docs.djangoproject.com/en/5.1/topics/db/models/#foreignkey
            name="Fiction"
        )

        self.book = Catalog.objects.create( # Creating Catalog entry. referencing category
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            category=self.category  # Using category object here
        )

        Price.objects.create( # Creating a price entry linked to the book
            book=self.book,
            amount=Decimal('14.99')
        )

    def test_model(self):
        self.assertEqual(self.book.title, "The Great Gatsby")
        self.assertEqual(self.book.author, "F. Scott Fitzgerald")

    def test_price_model(self):
        price = Price.objects.get(book=self.book)
        self.assertEqual(price.amount, Decimal('14.99'))  # not to self = Decimal values
