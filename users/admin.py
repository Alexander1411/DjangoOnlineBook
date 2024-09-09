from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline): # ProfileInline allows me to edit Profile fields directly on the User admin page
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):  
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 
                    'get_phone_number', 'get_city', 'get_birth_date')

    def get_phone_number(self, instance): # retrieve data from the related Profile and display
        return instance.profile.phone_number
    get_phone_number.short_description = 'PHONE NUMBER'

    def get_city(self, instance): # retrieve data from the related Profile and display
        return instance.profile.city
    get_city.short_description = 'CITY'

    def get_birth_date(self, instance): # retrieve data from the related Profile and display
        return instance.profile.birth_date
    get_birth_date.short_description = 'BIRTH DATE'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
