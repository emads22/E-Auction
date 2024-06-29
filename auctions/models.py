from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    

class Listing(models.Model):
    title = models.CharField(max_length=50) 
    description = models.CharField(max_length=1000)
    image_url  = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    starting_bid = models.FloatField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)    # automatically populated with current date
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category_listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_listings")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist_listings")

    def __str__(self):
        return f'"{self.title}" -- (added on {self.date_added.strftime("%b. %d, %Y, %I:%M %p")})' 
    

class Bid(models.Model):
    amount = models.FloatField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bids")

    def __str__(self):
        return f'{self.bidder.username}: "${self.amount}"'
        

class Comment(models.Model):
    text = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)    # automatically populated with current date
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comments")

    def __str__(self):
        return f'{self.author.username}: "{self.text}" -- (listing: "{self.listing.title}")'