from django.contrib import admin
from .models import Catalog, Price, Category, Stock

admin.site.register(Catalog)
admin.site.register(Stock)
admin.site.register(Price)
admin.site.register(Category)
