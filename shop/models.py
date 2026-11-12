from django.core.validators import MinValueValidator
from django.db import models


class OrderEnquiry(models.Model):
    CUSTOMER_TYPES = [
        ('Hotel', 'Hotel'),
        ('Restaurant', 'Restaurant'),
        ('Household', 'Household'),
        ('Other', 'Other'),
    ]

    PRODUCTS = [
        ('Red Snapper', 'Red Snapper'),
        ('Kingfish', 'Kingfish'),
        ('Tilapia', 'Tilapia'),
        ('Jumbo Prawns', 'Jumbo Prawns'),
        ('Medium Prawns', 'Medium Prawns'),
        ('Mud Crab', 'Mud Crab'),
        ('Fresh Squid', 'Fresh Squid'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    product = models.CharField(max_length=50, choices=PRODUCTS)
    quantity_kg = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    delivery_location = models.CharField(max_length=150)
    preferred_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.product} ({self.quantity_kg} kg)"