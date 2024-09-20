from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model): # I using Profile model for additional user info, so its not User model
    user = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneField
    phone_number = models.CharField(max_length=15, unique=True, db_index=True, blank=True, null=True) # Indexing helps speed up queries that frequently involve the phone_number field, especially if the field is marked as unique=True. By adding an index, the database can quickly locate rows based on the phone_number without scanning the entire table.
    city = models.CharField(max_length=100, blank=True)  
    birth_date = models.DateField(blank=True, null=True) # Null allowed for DateField

    def __str__(self):
        return self.user.username
