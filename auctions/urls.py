from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("closed listings", views.closed_listings, name="closed_listings"),
    path("create listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.view_listing, name="listing"),
    path("categories", views.display_categories, name="categories"),
    path("category/<int:category_id>", views.display_category_listings, name="category_listings"),
    path("bids/listing/<int:listing_id>", views.place_bid, name="bid"),
    path("add comment/listing/<int:listing_id>", views.add_comment, name="comment"),
    path("delete comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("watchlist", views.open_watchlist, name="watchlist"),
    path("add to watchlist/listing/<int:listing_id>", views.add_to_watchlist, name="add_watchlist"),
    path("remove from watchlist/listing/<int:listing_id>", views.remove_from_watchlist, name="remove_watchlist"),
    path("close/listing/<int:listing_id>", views.close_auction, name="close_auction")
]
