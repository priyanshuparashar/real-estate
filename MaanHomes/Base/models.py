from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Define Property Types
PROPERTY_TYPES = [
    ('pg', 'PG'),
    ('house', 'House'),
    ('bungalow', 'Bungalow'),
    ('flat', 'Flat'),
    ('shop', 'Shop'),
    ('showroom', 'Showroom'),
    ('commercial', 'Commercial Property'),
    ('plot', 'Plot'),
]

# Define Status for Listings
LISTING_STATUS = [
    ('available', 'Available'),
    ('sold', 'Sold'),
    ('rented', 'Rented'),
]

# Define Transaction Types
TRANSACTION_TYPES = [
    ('buy', 'Buy'),
    ('rent', 'Rent'),
    ('sell', 'Sell'),
    ('lease', 'Lease'),
]


class Profile(models.Model):
    """User profile for property owners, agents, and buyers."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_agent = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Property(models.Model):
    """Model to store property details."""
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    area_sq_ft = models.FloatField(help_text='Enter area in square feet')
    number_of_rooms = models.IntegerField(default=0)
    # e.g., "Pool, Gym, Parking"
    amenities = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=LISTING_STATUS, default='available')
    listed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"


class PropertyImage(models.Model):
    """Model to store images for properties."""
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"


class Inquiry(models.Model):
    """Model to store inquiries for properties."""
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    contact_info = models.CharField(max_length=255)
    inquiry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} for {self.property.title}"


class FavoriteProperty(models.Model):
    """Model to store favorite properties for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.property.title}"


class SubscriptionPlan(models.Model):
    """Model to store subscription plans for featured listings or agent subscriptions."""
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    features = models.TextField(
        help_text='List of features provided by the subscription plan')

    def __str__(self):
        return self.name


class FeaturedListing(models.Model):
    """Model to store featured property listings."""
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Featured: {self.property.title}"


class Review(models.Model):
    """Model for property reviews."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.property.title}"


class Transaction(models.Model):
    """Model to store payment transactions for subscriptions or featured listings."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Transaction by {self.user.username} - {self.transaction_type}"
