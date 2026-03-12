from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'


class Battery(models.Model):
    title = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    watt = models.CharField(max_length=20, blank=True, help_text="Quvvat (masalan: 20W)")
    voltage = models.CharField(max_length=20, blank=True, help_text="Kuchlanish (masalan: 3.7V)")
    capacity = models.CharField(max_length=50, blank=True, help_text="Sig'im (masalan: 5000mAh)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        verbose_name_plural = "Batteries"
        ordering = ['-created_at']
        db_table = 'batteries'


class Charger(models.Model):
    title = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    watt = models.CharField(max_length=20, blank=True, help_text="Quvvat (masalan: 65W)")
    voltage = models.CharField(max_length=20, blank=True, help_text="Kuchlanish (masalan: 12V)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        ordering = ['-created_at']
        db_table = 'chargers'


class Display(models.Model):
    title = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    hz = models.CharField(max_length=20, blank=True, help_text="Chastota (masalan: 60Hz, 144Hz)")
    pin = models.CharField(max_length=20, blank=True, help_text="Pin (masalan: 30pin, 40pin)")
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.count} dona)"

    class Meta:
        ordering = ['-created_at']
        db_table = 'displays'