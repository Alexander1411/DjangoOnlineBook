from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Catalog, Category, Wishlist, Cart, Price
from django.contrib.messages import get_messages
from books.forms import CheckoutForm
from decimal import Decimal


class WishlistViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bookMclover', password='W1234D')
        self.client.login(username='bookMclover', password='W1234D')

        self.category = Category.objects.create(name="Fiction")
        self.book = Catalog.objects.create(
            title="1984",
            slug="1984",
            author="George Orwell",
            category=self.category,
            description="Dystopian novel, blah, blah"
        )
        Wishlist.objects.create(user=self.user, book=self.book)

    def test_wishlist_view(self):
        # Access the wishlist view
        response = self.client.get(reverse('wishlist_view'))
        self.assertEqual(response.status_code, 200)  # Ensure the page loads
        self.assertTemplateUsed(response, 'books/wishlist.html')  # Check template
        self.assertContains(response, "1984")  # Ensure the book is in the wishlist
        
class SearchBookViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='SomeDude', password="DudesPassword")
        self.client.login(username='SomeDude', password='DudesPassword')

        self.category = Category.objects.create(name='Fiction')
        self.moby_dick = Catalog.objects.create(
            title='Moby Dick',
            slug='moby-dick',
            author='Herman Melville',
            category=self.category
        )

    def test_search_books(self):
        Wishlist.objects.create(user=self.user, book=self.moby_dick) # Adding book to the users wishlist first

        response = self.client.get(reverse('search_books'), {'q': 'Moby Dick'}) # Search for "Moby Dick"
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moby Dick")
        self.assertNotContains(response, "1984")

        books = response.context['books']
        self.assertTrue(hasattr(books[0], 'in_wishlist'), "in_wishlist annotation missing")
        self.assertTrue(books[0].in_wishlist)  # Check if the book is actually in the wishlist

def test_search_books(self):
    Wishlist.objects.create(user=self.user, book=self.moby_dick)
    
    response = self.client.get(reverse('search_books'), {'q': 'Moby Dick'})
    print(response.context['books'][0].in_wishlist)  

class BookListViewTest(TestCase):
    def setUp(self):
        # Setting up test data
        self.user = User.objects.create_user(username='AlexanderBook', password='AlexanderBook34')
        self.category = Category.objects.create(name='Fiction')
        self.book1 = Catalog.objects.create(
            title='1984', author='George Orwell', category=self.category)
        self.book2 = Catalog.objects.create(
            title='War and Peace', author='Leo Tolstoy', category=self.category)

        # Create a wishlist for the user
        self.wishlist_item = Wishlist.objects.create(user=self.user, book=self.book1)

    def test_book_list_view_without_login(self):
        # Test the view without the user being authenticated
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1984')
        self.assertContains(response, 'War and Peace')
        # Check that 'in_wishlist' is not in the context since the user is not authenticated
        books = response.context['books']
        self.assertFalse(hasattr(books[0], 'in_wishlist'))

    def test_book_list_view_with_login(self):
        # Login as the user
        self.client.login(username='AlexanderBook', password='AlexanderBook34')

        # Test the view with the user logged in
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1984')
        self.assertContains(response, 'War and Peace')

        # Check the 'in_wishlist' annotation in the context
        books = response.context['books']
        self.assertTrue(hasattr(books[0], 'in_wishlist'))

        # Test if the correct book is marked as in the wishlist
        for book in books:
            if book.pk == self.book1.pk:
                self.assertTrue(book.in_wishlist)  # 1984 is in the wishlist
            else:
                self.assertFalse(book.in_wishlist)  # War and Peace is not in the wishlist

class BookDetailViewTest(TestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(username='MyBooks', password='OnlyMyBook55')
        self.category = Category.objects.create(name='Psychological Fiction')
        self.book = Catalog.objects.create(
            title='Crime and Punishment', author='Fyodor Dostoevsky', category=self.category)

    def test_book_details_view_without_login(self):
        # Test the view without the user being authenticated
        response = self.client.get(reverse('book_details', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crime and Punishment')
        self.assertContains(response, 'Fyodor Dostoevsky')
        # Check that 'in_wishlist' is not in the context since the user is not authenticated
        self.assertNotIn('in_wishlist', response.context)

    def test_book_details_view_with_login_not_in_wishlist(self):
        # Login as the user
        self.client.login(username='MyBooks', password='OnlyMyBook55')

        # Test the view with the user logged in but without the book in the wishlist
        response = self.client.get(reverse('book_details', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crime and Punishment')
        self.assertContains(response, 'Fyodor Dostoevsky')

        # Check that 'in_wishlist' is False since the book is not in the user's wishlist
        self.assertIn('in_wishlist', response.context)
        self.assertFalse(response.context['in_wishlist'])

    def test_book_details_view_with_login_in_wishlist(self):
        # Add the book to the user's wishlist
        Wishlist.objects.create(user=self.user, book=self.book)

        # Login as the user
        self.client.login(username='MyBooks', password='OnlyMyBook55')

        # Test the view with the user logged in and the book in the wishlist
        response = self.client.get(reverse('book_details', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crime and Punishment')
        self.assertContains(response, 'Fyodor Dostoevsky')

        # Check that 'in_wishlist' is True since the book is in the user's wishlist
        self.assertIn('in_wishlist', response.context)
        self.assertTrue(response.context['in_wishlist'])

class AddToWishlistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='QuickestReader',password='QuickestReader76')
        self.category = Category.objects.create(name='Gothic Fiction')
        self.book = Catalog.objects.create(title='Wuthering Heights', author='Emily Bronte', category=self.category)

    def test_add_to_wishlist_without_login(self):
        response = self.client.post(reverse('add_to_wishlist',args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/books/wishlist/add/{self.book.id}/')

    def test_add_to_wishlist_with_login(self):
        self.client.login(username='QuickestReader', password='QuickestReader76')
        response = self.client.post(reverse('add_to_wishlist', args=[self.book.id]))   # Add the book to the wishlist
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wishlist_view'))

        self.assertTrue(Wishlist.objects.filter(user=self.user, book=self.book).exists()) # Check if the book was added to the wishlist

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),'Wuthering Heights has been added to your wishlist.')

    def test_add_to_wishlist_already_exists(self):
        Wishlist.objects.create(user=self.user, book=self.book)
        self.client.login(username='QuickestReader', password='QuickestReader76')
        response = self.client.post(reverse('add_to_wishlist', args=[self.book.id])) # # Try to add the same book again
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wishlist_view'))

        self.assertEqual(Wishlist.objects.filter(user=self.user, book=self.book).count(), 1) # Ensuring that book was not added multiple times to the wishlist

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wuthering Heights has been added to your wishlist.')

class CheckoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='QuickestReader', password='QuickestReader76')
        self.category = Category.objects.create(name='Gothic Fiction')

        self.book = Catalog.objects.create(title='Wuthering Heights', author='Emily Bronte', category=self.category) # Setting book with a price
        self.book_price = Price.objects.create(book=self.book, amount=Decimal('10.99'))
        
        self.cart_item = Cart.objects.create(user=self.user, book=self.book, quantity=2) # Adding book to the cart

    def test_checkout_view_without_login(self): # Testin access to checkout without login
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/books/checkout/')

    def test_checkout_view_with_login(self): # Login as user
        self.client.login(username='QuickestReader', password='QuickestReader76')

        response = self.client.get(reverse('checkout')) # Accessing checkout page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/checkout.html')

        self.assertIsInstance(response.context['form'], CheckoutForm) # Ensuring  form is in the context

        # Use Decimal for comparison
        total_price = Decimal('10.99') * 2
        self.assertEqual(response.context['total_price'], total_price)

#    def test_checkout_process(self):
#        # Login as the user
#        self.client.login(username='QuickestReader', password='QuickestReader76')

        # Post valid data to the checkout form
#        response = self.client.post(reverse('checkout'), {

#            'address': 'Great Address',
#            'city': 'Fake City',
#            'zip_code': '123',
#            'payment_method': 'stripe'
#        })

        # Print form errors for debugging
#        if 'form' in response.context:
#            print(response.context['form'].errors)

        # Check that the form was valid, and the cart was emptied
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'books/checkout_success.html')

        # Check if the cart was emptied
#        self.assertEqual(Cart.objects.filter(user=self.user).count(), 0)

        # Check if the total price was passed to the template
#        total_price = Decimal('10.99') * 2
#        self.assertContains(response, f'Total: {total_price}')