from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    seo_title = models.CharField(max_length=60, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.seo_title:
            self.seo_title = f"Buy {self.name} | MyStore"
        if not self.seo_description:
            self.seo_description = f"Shop {self.name} at the best price. {self.description[:100]}..."
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

class ProductVariant(models.Model):
    VARIANT_TYPES = [
        ('size', 'Size'),
        ('color', 'Color'),
        ('material', 'Material'),
    ]
    
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_type = models.CharField(max_length=20, choices=VARIANT_TYPES)
    name = models.CharField(max_length=50)
    price_adjustment = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"