from django.db import models


class Battery(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, help_text="Brand (masalan: HP, Asus, Acer)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        verbose_name_plural = "Batteries"
        ordering = ['-created_at']
        db_table = 'batteries'


class Charger(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, help_text="Brand (masalan: HP, Asus, Acer)")
    watt = models.CharField(max_length=20, blank=True, help_text="Quvvat (masalan: 65W)")
    voltage = models.CharField(max_length=20, blank=True, help_text="Kuchlanish (masalan: 19V, 20V)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        ordering = ['-created_at']
        db_table = 'chargers'


class Display(models.Model):
    title = models.CharField(max_length=200)
    hz = models.CharField(max_length=20, blank=True, help_text="Chastota (masalan: 60Hz, 144Hz)")
    pin = models.CharField(max_length=20, blank=True, help_text="Pin (masalan: 30pin, 40pin)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        ordering = ['-created_at']
        db_table = 'displays'
