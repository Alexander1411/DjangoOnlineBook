from django.shortcuts import render, redirect
from .models import Order, OrderItem
from books.models import Cart 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request, purchased_books, total_price):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    order = Order.objects.create(user=request.user, total_price=total_price) # Creating  order

    for cart_item in cart_items: # Create order items from  cart items
        OrderItem.objects.create(
            order=order,
            book=cart_item.book,
            quantity=cart_item.quantity,
            price=cart_item.book.price.amount
        )
    cart_items.delete() # Clear the cart after order is placed

    return render(request, 'books/checkout_success.html', { # Render  checkout_success.html with the order details
        'purchased_books': purchased_books,
        'total_price': total_price,
        'order': order  # Pass  order to display order number
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at') # Fetch all orders for logged in user

    return render(request, 'orders/order_history.html', {'orders': orders}) # Pass  orders to the template