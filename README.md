Django Online Bookstore 

This project is a fully functional Django-based online bookstore. Users can browse books, add them to their wishlist and shopping cart, proceed to checkout, and make purchases. The admin has the ability to manage books in the inventory. The application is designed with a focus on separation of concerns and user-friendly interaction, including features such as user registration, login, and profile management.



Features
User Registration and Authentication: Users can sign up, log in, and reset their passwords.
Profile Management: Users can view and edit their profile information, including personal details and preferences.
Wishlist: Users can add books to their wishlist for future reference.
Shopping Cart: Users can add items to their cart, update quantities, and remove items.
Checkout and Payment: Integration with Stripe allows users to securely make payments for their purchases.
Order History: Users can view their order history to track past purchases.
Admin Panel: The admin can manage books in the inventory, including adding new books and editing existing ones.

Setup
Prerequisites
Python 3.x
Django 5.0.7
PostgreSQL (or any supported database)
Stripe API keys for payment integration
Git (for version control)
Heroku (for deployment)

Installation
Clone the repository
Set up a virtual environment
Install the project dependencies (pip install -r requirements.txt)
Set up the database (settings.py)
Run the migrations (python manage.py migrate)
Create a superuser for accessing the admin panel (python manage.py createsuperuser)
Run the development server (python manage.py runserver)


Stripe Integration
STRIPE_PUBLIC_KEY = 'your-public-key'
STRIPE_SECRET_KEY = 'your-secret-key'


Deployment (Heroku)
Install the Heroku CLI and log
Create a Procfile in the root directory
Push the project to Heroku
Set up the PostgreSQL addon on Heroku (heroku addons:create heroku-postgresql:hobby-dev)
Apply the migrations on Heroku (heroku run python manage.py migrate)


Testing
python manage.py test




"# DjangoOnlineBook" 
