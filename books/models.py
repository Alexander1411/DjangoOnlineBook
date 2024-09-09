from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Catalog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    is_top = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_related_books(self):
        return Catalog.objects.filter(category=self.category).exclude(id=self.id)[:5]

    def __str__(self):
        return self.title

class Price(models.Model):
    book = models.OneToOneField(Catalog, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} - ${self.amount}"

class Stock(models.Model):
    book = models.OneToOneField(Catalog, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='wishlist_items')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.book.title}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
