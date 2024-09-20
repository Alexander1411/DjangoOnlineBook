from django.urls import path
from .views import BookListView, BookDetailView
from . import views

urlpatterns = [
    path('search/', views.search_books, name='search_books'), #home search function 
    path('<int:pk>/', BookDetailView.as_view(), name='book_details'), # home page
    path('', BookListView.as_view(), name='book_list'), # all books 
    path('wishlist/', views.WishlistView.as_view(), name='wishlist_view'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),



    # cart view
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:book_id>/', views.update_cart_quantity, name='update_cart_quantity'),

] 

