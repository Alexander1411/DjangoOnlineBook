from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy # Import reverse_lazy for lazy URL resolution, typically used in class based views
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Catalog, Category, Stock, Price, Wishlist, Cart
from .utils import check_low_stock
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.contrib import messages
from .forms import CheckoutForm

# View for searching books by a query string
def search_books(request): # Used this logic :  https://stackoverflow.com/questions/44817298/search-using-django-filter 
    query = request.GET.get('q') # Get the search query from the request : https://forum.djangoproject.com/t/having-trouble-fetching-search-results/7667
    results = Catalog.objects.filter(title__icontains=query) # Filter the Catalog objects whose title contains the search query : https://stackoverflow.com/questions/37396781/how-to-order-django-query-set-filtered-using-icontains-such-that-the-exactly
    
    if request.user.is_authenticated: # is user autheticated :https://forum.djangoproject.com/t/user-is-authenticated/5145/7
        wishlist_subquery = Wishlist.objects.filter(user=request.user, book=OuterRef('pk')) # filters the wishlist to see if the current user has a book on their wishlist. This video helped me:https://www.youtube.com/watch?v=QvaScsn6S6E
        results = results.annotate(in_wishlist=Exists(wishlist_subquery)) # annotate the results with a boolean indicating if each book is in the wishlist
    
    context = {
        'books': results,
        'query': query, # Pass the original query to the context
    }
    return render(request, 'books/book_list.html', context)

# Class based view for listing books.
class BookListView(ListView):
    model = Catalog
    template_name = 'books/book_list.html'
    context_object_name = 'books' # Use book as the context variable name

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            wishlist_subquery = Wishlist.objects.filter(user=self.request.user, book=OuterRef('pk'))
            queryset = queryset.annotate(in_wishlist=Exists(wishlist_subquery))
        return queryset

# Class  based view for displaying the details of a book, logic was taken from here: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
class BookDetailView(DetailView): # display detailed info about a single object, in this case, a book from my Catalog model
    model = Catalog # view will look up the details of a single instance of the Catalog model
    template_name = 'books/book_details.html'
    context_object_name = 'book' # # use book as the context variable name for the object
    slug_url_kwarg = 'slug' # https://docs.djangoproject.com/en/5.1/ref/class-based-views/mixins-single-object/

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Get the default context data..
        context['related_books'] = self.object.get_related_books()
        try:
            context['stock'] = Stock.objects.get(book=self.object) #  # Try to get the stock information for the book..
        except Stock.DoesNotExist:
            context['stock'] = None # If no stock exists, set it to None.
        try:
            context['price'] = Price.objects.get(book=self.object)
        except Price.DoesNotExist:
            context['price'] = None
        return context

# Classbased view for updating an existing book entry
class BookUpdateView(UpdateView):
    model = Catalog
    fields = ['title', 'author', 'description', 'category']  # Add all relevant fields
    template_name = 'books/book_list.html'
    success_url = reverse_lazy('book_list')

# Class based view for deleting a book entry 
class BookDeleteView(DeleteView):
    model = Catalog
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

# Class based view to display the users wishlist
class WishlistView(ListView):
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

## Functionbased view to remove a book from the users wishlist
@login_required # make sure that the user is authenticated before allowing access to this view.
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Catalog, id=book_id) # Fetch the book by ID or return a 404 if not found.
    Wishlist.objects.filter(user=request.user, book=book).delete()
    messages.success(request, 'Book removed from your wishlist.') # Display a success message to the user.
    return redirect('wishlist_view')

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
    total_price = sum(item.book.price.amount * item.quantity for item in cart_items)
    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.book.price.amount * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the order
            # Empty the cart
            cart_items.delete()
            return render(request, 'books/checkout_success.html', {'total_price': total_price})
    else:
        form = CheckoutForm()
    
    return render(request, 'books/checkout.html', {'form': form, 'total_price': total_price})

@login_required
def remove_from_cart(request, book_id):
    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    cart_item.delete()  # Remove the item from the cart
    return redirect('cart_view')  # Redirect to the cart page

@login_required
def update_cart_quantity(request, book_id):
    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    
    # Get the new quantity from a POST request
    new_quantity = int(request.POST.get('quantity', 1))
    
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()  # If the new quantity is 0, remove the item from the cart
    
    return redirect('cart_view')

