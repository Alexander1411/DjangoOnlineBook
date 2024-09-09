from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.order_history, name='order_history'),
    path('management/', views.order_management, name='order_management'),
    path('<int:order_id>/', views.order_summary, name='order_summary'),
]
