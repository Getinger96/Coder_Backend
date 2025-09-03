from django.db import models
from auth_app.models import User




# Create your models here.

class Profile(models.Model):
    """
    Represents a user profile linked to a User instance.

    Fields:
        user: One-to-one relationship to the User.
        username: Optional username string.
        first_name: Optional first name.
        last_name: Optional last name.
        file: Optional profile picture or file upload.
        location: Optional location string.
        tel: Optional telephone number.
        description: Optional free-text description.
        working_hours: Optional working hours info.
        uploaded_at: Timestamp when profile was created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, default='') 
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    file = models.FileField(upload_to='profile_pics/', default='', blank=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=50, blank=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Offer(models.Model):
    """
    Represents an offer created by a business profile.

    Fields:
        title: Title of the offer.
        image: Optional image representing the offer.
        description: Detailed description of the offer.
        profile: ForeignKey to the business profile who created the offer.
        created_at: Timestamp when offer was created.
        updated_at: Timestamp when offer was last updated.
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    profile = models.ForeignKey(Profile, related_name='offers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """
    Detailed options or packages for a specific offer.

    Fields:
        offer: ForeignKey to the related Offer.
        title: Title of the detail/package.
        revisions: Number of allowed revisions.
        delivery_time_in_days: Estimated delivery time in days.
        price: Price for this offer detail.
        features: JSON field listing features (alternative to ManyToMany).
        offer_type: Type of offer (basic, standard, premium).
    """
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
    features = models.JSONField()  # Alternatively, a ManyToMany relation to a Feature model
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return self.title


class Order(models.Model):
    """
    Represents an order placed by a customer for an offer detail.

    Fields:
        offer_detail: The OfferDetail ordered.
        customer_user: Profile of the customer placing the order.
        business_user: Profile of the business receiving the order.
        status: Current order status.
        created_at: Timestamp when the order was created.
        updated_at: Timestamp when the order was last updated.
    """
    ORDER_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    offer_detail = models.ForeignKey(OfferDetail, related_name='orders', on_delete=models.CASCADE)
    customer_user = models.ForeignKey(Profile, related_name='orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(Profile, related_name='received_orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Zeigt z. B. den OfferDetail Titel + Status
        return f"Order #{self.id} - {self.offer_detail.title} ({self.status})"


class Review(models.Model):
    """
    Represents a review given by a customer to a business profile.

    Fields:
        business_user: Profile of the business being reviewed.
        reviewer: Profile of the customer who wrote the review.
        rating: Numeric rating given.
        description: Optional text describing the review.
        created_at: Timestamp when the review was created.
        updated_at: Timestamp when the review was last updated.
    """
    business_user = models.ForeignKey(Profile, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Profile, related_name='given_reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Zeigt z. B. Reviewer → Business + Bewertung
        return f"Review by {self.reviewer.user.username} for {self.business_user.user.username} "
