from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        db_table = 'categories'


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


    class Meta:

        db_table = 'brands'


class Product(models.Model):
    PRODUCT_TYPES = (
        ('batareyka', 'Batareyka'),
        ('zaryadka', 'Zaryadka'),
    )

    title = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    watt = models.CharField(max_length=20, blank=True, help_text="Quvvat (masalan: 20W, 65W)")
    voltage = models.CharField(max_length=20, blank=True, help_text="Kuchlanish (masalan: 3.7V, 12V)")
    capacity = models.CharField(max_length=50, blank=True, help_text="Sig'im (masalan: 5000mAh)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        ordering = ['-created_at']
        db_table = 'products'

