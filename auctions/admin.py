from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment
   


class CategoryAdmin(admin.ModelAdmin):
    ordering = ["name"]


class ListingAdmin(admin.ModelAdmin):     
    ordering = ["id"]
    list_display = ("id", "title", "date_added", "active")
    filter_horizontal = ("watchlist",)


class BidAdmin(admin.ModelAdmin):
    ordering = ["bidder"]
    list_display = ("id", "bidder", "amount", "listing")

    # 'obj' represents an instance of the Bid model, and we use it to access and display related data in the custom admin interface for the Bid model.
    def listing(self, obj):
        return obj.listing.title 


class CommentAdmin(admin.ModelAdmin):
    ordering = ["date_posted"]
    list_display = ("id", "text", "date_posted", "relevant_listing", "author") 

    def relevant_listing(self, obj):
        return obj.listing.title



# Register your models here.
admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)