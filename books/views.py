from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy # Import reverse_lazy for lazy URL resolution, typically used in class based views
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from orders.views import create_order
from .models import Catalog, Category, Stock, Price, Wishlist, Cart
from .utils import check_low_stock
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CheckoutForm


class BookListView(ListView):
    model = Catalog
    template_name = 'books/book_list.html'
    context_object_name = 'books'  # Using books as the context variable name
 #   paginate_by = 9  # Pagination

    def get_queryset(self): # my annotation for user to see what is added and what can be remove from cart
        queryset = super().get_queryset()

        category = self.request.GET.get('category', None) # Filter by category if provided
        if category:
            queryset = queryset.filter(category__id=category)

        if self.request.user.is_authenticated: # Checking if user is authenticated and annotate the wishlist information
            wishlist_subquery = Wishlist.objects.filter(user=self.request.user, book=OuterRef('pk'))
            queryset = queryset.annotate(in_wishlist=Exists(wishlist_subquery))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass all categories to the template
        context['selected_category'] = self.request.GET.get('category', None)  # Keep track of selected category
        return context

# View for searching books by a query string
def search_books(request): # Used this logic :  https://stackoverflow.com/questions/44817298/search-using-django-filter 
    query = request.GET.get('q') # Get the search query from the request : https://forum.djangoproject.com/t/having-trouble-fetching-search-results/7667
    results = Catalog.objects.filter(title__icontains=query) # Filter the Catalog objects whose title contains the search query : https://stackoverflow.com/questions/37396781/how-to-order-django-query-set-filtered-using-icontains-such-that-the-exactly
    
    if request.user.is_authenticated: # is user autheticated :https://forum.djangoproject.com/t/user-is-authenticated/5145/7
        wishlist_subquery = Wishlist.objects.filter(user=request.user, book=OuterRef('pk')) # filters the wishlist to see if the current user has a book on their wishlist. This video helped me:https://www.youtube.com/watch?v=QvaScsn6S6E
        results = results.annotate(in_wishlist=Exists(wishlist_subquery)) # annotate the results with a boolean indicating if each book is in the wishlist
    
    context = {
        'books': results,
    #    'query': query, # Pass the original query to the context
    }
    return render(request, 'books/book_list.html', context)

    
# Class  based view for displaying the details of a book, logic was taken from here: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
class BookDetailView(DetailView): # 
    model = Catalog # view will look up the details of a single instance of the Catalog model
    template_name = 'books/book_details.html' # The button "View Detail"
    context_object_name = 'book' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object  # The current book being viewed
        if self.request.user.is_authenticated:
            wishlist_exists = Wishlist.objects.filter(user=self.request.user, book=book).exists()
            context['in_wishlist'] = wishlist_exists
        return context


# Class based view to display the users wishlist
class WishlistView(LoginRequiredMixin,ListView):
    model = Wishlist
    template_name = 'books/wishlist.html'
    context_object_name = 'wishlist_items' # 'wishlist_items' as the context variable name

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user) 

# Function based view to add a book to the users whishlist.
@login_required #  the user is authenticated before allowing access to this view.
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Catalog, id=book_id)
    Wishlist.objects.get_or_create(user=request.user, book=book) # Add the book to the users wishlist, or do nothing if its already there.
    messages.success(request, f"{book.title} has been added to your wishlist.")
    return redirect('wishlist_view')


@login_required # making sure that the user is authenticated before allowing access to this view.
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Catalog, id=book_id) # Fetch the book by ID or return a 404 if not found.
    Wishlist.objects.filter(user=request.user, book=book).delete()
    messages.success(request, 'Book removed from your wishlist.') # Display a success message to the user.
    return redirect('wishlist_view')

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Catalog, id=book_id)
    
    # Get or create a cart item for the user and book
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1  # If it exists, increase the quantity
        cart_item.save()
        
    return redirect('cart_view')  # Redirect to the cart view after adding

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate the total price for each item and the cart total
    for item in cart_items:
        item.total_price = item.book.price.amount * item.quantity  # Calculate total for this item
    
    total_price = sum(item.total_price for item in cart_items)  # Total for the whole cart

    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, book_id):
    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    cart_item.delete()  # Remove the item from the cart
    return redirect('cart_view')  # Redirect to the cart page

#@login_required
#def update_cart_quantity(request, book_id):
#    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    
    # Get the new quantity from a POST request
#    new_quantity = int(request.POST.get('quantity', 1))
    
#    if new_quantity > 0:
#        cart_item.quantity = new_quantity
#        cart_item.save()
#    else:
#        cart_item.delete()  # If the new quantity is 0, remove the item from the cart
    
#    return redirect('cart_view')

@login_required
def update_cart_quantity(request, book_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
        
        # Get the new quantity from the POST request
        new_quantity = int(request.POST.get('quantity', 1))
        
        # Update the quantity and save the cart item
        cart_item.quantity = new_quantity
        cart_item.save()

        # Recalculate the total price
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.book.price.amount * item.quantity for item in cart_items)

        # Return a JSON response if the request is an AJAX call
        #if request.is_ajax(): old version 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Quantity updated successfully.',
                'new_quantity': cart_item.quantity,
                'total_price': total_price
            })
    
    # If not an AJAX request, redirect to the cart view
    return redirect('cart_view')


from django.conf import settings  # To get Stripe secret key from settings
from stripe.error import StripeError
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY  # Set your secret key here

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.book.price.amount * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            stripe_token = form.cleaned_data.get('stripeToken')
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']

            if not stripe_token:
                messages.error(request, "No Stripe token was provided.")
                return render(request, 'books/checkout.html', {
                    'form': form, 
                    'total_price': total_price,
                    'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
                })

            # Process payment with Stripe
            try:
                charge = stripe.Charge.create(
                    amount=int(total_price * 100),  # Stripe works with cents
                    currency='eur',
                    description=f"Order for {name}",
                    source=stripe_token,
                    receipt_email=email
                )
            except stripe.error.StripeError as e:
                # Handle payment errors
                messages.error(request, f"Payment error: {str(e)}")
                return render(request, 'books/checkout.html', {
                    'form': form, 
                    'total_price': total_price,
                    'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
                })

            # If payment is successful, create the order and reduce stock
            purchased_books = []
            for item in cart_items:
                book = item.book
                stock = Stock.objects.get(book=book)
                if stock.quantity >= item.quantity:
                    stock.quantity -= item.quantity
                    stock.save()
                    purchased_books.append(book)
                else:
                    messages.error(request, f"Sorry, '{book.title}' has insufficient stock.")
                    return redirect('cart_view')

            create_order(request, purchased_books, total_price)
            cart_items.delete()

            return render(request, 'books/checkout_success.html', {
                'purchased_books': purchased_books, 
                'total_price': total_price,
            })

        else:
            messages.error(request, "There was an error with your form.")
    else:
        form = CheckoutForm(initial={'email': request.user.email})

    return render(request, 'books/checkout.html', {
        'form': form, 
        'total_price': total_price,
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
    })