from django.db import models
from auth_app.models import User




# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, default='') 
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    file = models.FileField(upload_to='profile_pics/',default='', blank=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=50, blank=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    

class Offer(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    profile = models.ForeignKey(Profile, related_name='offers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class OfferDetail(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()  # Alternativ: ein ManyToMany zu einem Feature-Modell
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return self.title
    

class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    offer_detail = models.ForeignKey(OfferDetail, related_name='orders', on_delete=models.CASCADE)
    customer_user = models.ForeignKey(Profile, related_name='orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(Profile, related_name='received_orders', on_delete=models.CASCADE)
    status=models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Review(models.Model):
    business_user = models.ForeignKey(Profile, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Profile, related_name='given_reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
