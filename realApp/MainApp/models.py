from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ('lost', 'Lost'),
    ('found', 'Found'),
    ('returned', 'Returned'),
]


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('accessories', 'Accessories'),
        ('documents', 'Documents'),
        ('keys', 'Keys'),
        ('bags', 'Bags'),
        ('others', 'Others'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    date_reported = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lost')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.status.capitalize()}"


class ClaimRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    contact_info = models.CharField(max_length=100)
    requested_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Claim by {self.claimant.username} for {self.item.title} - {self.status.capitalize()}"
