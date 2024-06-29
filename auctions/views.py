from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from auctions.models import User, Category, Listing, Bid, Comment


INITIAL_CATEGORIES = ['Collectibles', 'Fashion', 'Furniture', 'Tools', 'Computers', 'Mobiles', 'Cameras', 'Toys', 'Jewelry']
NO_IMAGE_URL = "https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg"


# <==================================================< Forms >==================================================>
class ListingForm(forms.Form):
    title = forms.CharField(label='Title', 
                            max_length=50, 
                            widget=forms.TextInput(attrs={'class': 'form-control form-control-lg text-color', 
                                                          'placeholder': 'Enter a title'}))
    
    description = forms.CharField(label='Description', 
                                  max_length=1000, 
                                  widget=forms.Textarea(attrs={'class': 'form-control form-control-lg text-color', 
                                                               'rows': 4, 
                                                               'placeholder': 'Enter a description'}))
    
    image_url = forms.URLField(label='Image URL (Optional)', 
                               required=False,
                               widget=forms.URLInput(attrs={'class': 'form-control form-control-lg text-color', 
                                                            'placeholder': 'Enter an image URL'}))
    
    starting_bid = forms.FloatField(label='Starting Bid (USD)', 
                             widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg text-color', 
                                                             'step': 0.01, 
                                                             'min': 0, 
                                                             'placeholder': 'Enter a price'}))
    
    category = forms.ChoiceField(
        label='Category',
        # choices must be list of tuples (value, display_label), and added first choice as empty value. (categories are instances of table)
        choices=[('', 'Select a category')] + [(category.name, category.name) for category in Category.objects.all()],
        initial='',     # here empty value is selected at first
        widget=forms.Select(attrs={'class': 'form-select form-select-lg text-color'}))
    
    

class BidForm(forms.Form):
    bid = forms.FloatField(label='',
                           widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg',
                                                           'step': 0.01,
                                                           'min': 0,
                                                           'placeholder': 'Enter a bid'}))
    
           
class CommentForm(forms.Form):
    comment = forms.CharField(label='',  
                              widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                            'placeholder': 'Leave a comment'}))
    


# <==================================================<Helper Tools>==================================================>
def create_context(**kwargs):

    # create context template to avoid repeating the passing args in views everytime. use get() to set a default value 'None' if key not available
    context = {
        "category": kwargs.get("category", None),
        "categories": kwargs.get("categories", None),
        "listing": kwargs.get("listing", None),
        "listings": kwargs.get("listings", None),
        "listing_form": kwargs.get("listing_form", None),
        "create_listing_flash": kwargs.get("create_listing_flash", None),
        "n_watchlist_listings": kwargs.get("n_watchlist_listings", None),
        "is_listing_in_watchlist": kwargs.get("is_listing_in_watchlist", None),
        "watchlist_flash": kwargs.get("watchlist_flash", None),
        "current_bid": kwargs.get("current_bid", None),
        "total_bids": kwargs.get("total_bids", None),     
        "bid_form": kwargs.get("bid_form", None),
        "bid_flash": kwargs.get("bid_flash", None),
        "comments": kwargs.get("comments", None),
        "comment_form": kwargs.get("comment_form", None),
        "comment_flash": kwargs.get("comment_flash", None),
        "is_winner": kwargs.get("is_winner", None),
        "all_closed": kwargs.get("all_closed", None),       
        "auction_flash": kwargs.get("auction_flash", None),
        }

    return context



# <==================================================<Views Functions>==================================================>
def index(request):
    """ returns homepage that displays active listings """

    # check if the queryset is empty before proceeding (at the start no categories available), otherwise after added directly show them
    # also categories can be added through admin interface
    if not Category.objects.all():
        for category in INITIAL_CATEGORIES:
            Category.objects.create(name=category)

    current_user = request.user
    active_listings = Listing.objects.filter(active=True).all()

    context = create_context(
        # usually we would put 'active_listings' here but we want the current_bid to each one so we group the data
        listings=[],
        n_watchlist_listings=None if current_user.is_anonymous else current_user.watchlist_listings.all().count()
    )

    for listing in active_listings:
        # instead of a list of listings, we create a list of dicts where each dict contains 2 key-value pairs (listing , current_bid)
        grouped = {
            'listing': listing,
            # get the highest bid to every listing 
            'current_bid': listing.listing_bids.order_by("-amount").first()
            }
        # append it to context empty list 
        context['listings'].append(grouped)
    
    return render(request, "auctions/index.html", context)
  


def display_categories(request):
    """ returns a page that displays all the categories """

    current_user = request.user

    # create the context
    context = create_context(
        categories=Category.objects.all(),
        # current_user.is_anonymous means no user logged in, also in case 'category_listings' empty 'n_watchlist_listings' will be 0
        n_watchlist_listings=None if current_user.is_anonymous else current_user.watchlist_listings.all().count()
    )

    return render(request, "auctions/categories.html", context)



def display_category_listings(request, category_id):
    """ returns a page that displays all the listings under a specific category """

    this_category = Category.objects.get(pk=category_id)
    current_user = request.user
    # get all active listings under this category
    category_listings = Listing.objects.filter(category=this_category, active=True).all()

    # create the context
    context = create_context(
        # usually we would put 'category_listings' here but we want the current_bid to each one so we group the data
        listings=[],
        category=this_category.name,
        # current_user.is_anonymous means no user logged in, also in case 'category_listings' empty 'n_watchlist_listings' will be 0
        n_watchlist_listings=None if current_user.is_anonymous else current_user.watchlist_listings.all().count()
    )

    for listing in category_listings:
        # instead of a list of listings, we create a list of dicts where each dict contains 2 key-value pairs (listing , current_bid)
        grouped = {
            'listing': listing,
            # get the highest bid to every listing 
            'current_bid': listing.listing_bids.order_by("-amount").first()
            }
        # append it to context empty list 
        context['listings'].append(grouped)
    
    return render(request, "auctions/category_listings.html", context)



def closed_listings(request):
    """ returns the page that displays closed listings """
    
    current_user = request.user
    closed_listings = Listing.objects.filter(active=False).all()

    # create the context
    context = create_context(
        # usually we would put 'closed_listings' here but we want the current_bid to each one so we group the data
        listings=[],
        all_closed=True,
        # current_user.is_anonymous means no user logged in, also in case 'category_listings' empty 'n_watchlist_listings' will be 0
        n_watchlist_listings=None if current_user.is_anonymous else current_user.watchlist_listings.all().count()
    )

    for listing in closed_listings:
        # instead of a list of listings, we create a list of dicts where each dict contains 2 key-value pairs (listing , current_bid)
        grouped = {
            'listing': listing,
            # get the highest bid to every listing 
            'current_bid': listing.listing_bids.order_by("-amount").first()
            }
        # append it to context empty list 
        context['listings'].append(grouped)
    
    return render(request, "auctions/index.html", context)



@login_required
def open_watchlist(request):
    """ returns the page that displays the watchlist of the current user and all the listings that it includes """

    current_user = request.user
    watchlist_listings = current_user.watchlist_listings.all()
    
    # create the context
    context = create_context(
        # usually we would put 'watchlist_listings' here but we want the current_bid to each one so we group the data
        listings=[],
        # in case 'watchlist_listings' empty 'n_watchlist_listings' will be 0
        n_watchlist_listings=current_user.watchlist_listings.all().count()
    )

    for listing in watchlist_listings:
        # instead of a list of listings, we create a list of dicts where each dict contains 2 key-value pairs (listing , current_bid)
        grouped = {
            'listing': listing,
            # get the highest bid to every listing 
            'current_bid': listing.listing_bids.order_by("-amount").first()
            }
        # append it to context empty list 
        context['listings'].append(grouped)
    
    return render(request, "auctions/watchlist.html", context)



@login_required
def add_to_watchlist(request, listing_id):
    """ adds a listing to user's watchlist and stays on same page of the listing with a message displayed """

    this_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    # add this listing to this user watchlist
    current_user.watchlist_listings.add(this_listing)
    # alternatively adding this listing to current_user watchlist     
    # this_listing.watchlist.add(current_user)

    # create the context
    context = create_context(
        listing=this_listing,
        comment_form=CommentForm(),
        comments=Comment.objects.filter(listing=this_listing).all(),
        bid_form=BidForm(),
        current_bid=this_listing.listing_bids.order_by("-amount").first(),
        total_bids=this_listing.listing_bids.all().count()-1, 
        is_listing_in_watchlist=this_listing in current_user.watchlist_listings.all(),
        n_watchlist_listings=current_user.watchlist_listings.all().count(),
        watchlist_flash="Listing added to your watchlist successfully."
    )

    return render(request, "auctions/listing.html", context)



@login_required
def remove_from_watchlist(request, listing_id):
    """ removes a listing from user's watchlist and stays on same page of the listing with a message displayed """

    this_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    # remove this listing from this user watchlist
    current_user.watchlist_listings.remove(this_listing)
    # alternatively removing this listing from current_user watchlist     
    # this_listing.watchlist.remove(current_user)

    # create the context
    context = create_context(
        listing=this_listing,
        comment_form=CommentForm(),
        comments=Comment.objects.filter(listing=this_listing).all(),
        bid_form=BidForm(),
        current_bid=this_listing.listing_bids.order_by("-amount").first(),
        total_bids=this_listing.listing_bids.all().count()-1, 
        is_listing_in_watchlist=this_listing in current_user.watchlist_listings.all(),
        n_watchlist_listings=current_user.watchlist_listings.all().count(),
        watchlist_flash="Listing removed from your watchlist successfully."
    )

    return render(request, "auctions/listing.html", context)



@login_required
def create_listing(request):
    """ returns the page that displays 'create listing' form """

    current_user = request.user
    # create the default context
    context = create_context(
        n_watchlist_listings=current_user.watchlist_listings.all().count(),
        listing_form=ListingForm()
    )
    
    if request.method == "POST":
        listing_form = ListingForm(request.POST)
        # validate form to save it in database
        if listing_form.is_valid():   
            this_starting_bid = float(listing_form.cleaned_data["starting_bid"])
            # create new Listing instance
            new_listing = Listing(
                title = listing_form.cleaned_data["title"].title(),  
                description = listing_form.cleaned_data["description"],
                image_url = listing_form.cleaned_data["image_url"] if listing_form.cleaned_data["image_url"] != "" else NO_IMAGE_URL,
                starting_bid = this_starting_bid,              
                category = Category.objects.get(name=listing_form.cleaned_data["category"]),
                seller = current_user)
            # save this new instance
            new_listing.save()
            # create new Bid instance for this listing with the starting bid (with create() no need for save())
            Bid.objects.create(amount=this_starting_bid, bidder=current_user, listing=new_listing)
            # add the new values of the following variables (arguments that are keys in dict) in the context, the rest remain the same 
            context['create_listing_flash'] = "New listing created successfully."
            # redirect to same page with new empty form
            return render(request, "auctions/create_listing.html", context)
        # otherwise not validated
        else:
            # add the new values of the following variables (arguments that are keys in dict) in the context, the rest remain the same 
            context['listing_form'] = listing_form
            # redirect to same page with same form with inserted data
            return render(request, "auctions/create_listing.html", context)
    # if GET method visit page with empty form (default context)
    return render(request, "auctions/create_listing.html", context)



def view_listing(request, listing_id):
    """ returns the page that displays the listing and all its details including Bid and Comment forms """

    this_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    # get the max of all bids related to this listing ('-' in order_by() is for descendant order)
    current_bid = this_listing.listing_bids.order_by("-amount").first()
    # create the context
    context = create_context(
        listing=this_listing,
        bid_form=BidForm(),
        current_bid=current_bid,
        # get all bids number minus the starting bid (price)
        total_bids=this_listing.listing_bids.all().count()-1,
        comment_form=CommentForm(),
        comments=this_listing.listing_comments.all(),
        is_listing_in_watchlist=False if current_user.is_anonymous else this_listing in current_user.watchlist_listings.all(),
        # current_user.is_anonymous means no user logged in, also in case 'category_listings' empty 'n_watchlist_listings' will be 0
        n_watchlist_listings=None if current_user.is_anonymous else current_user.watchlist_listings.all().count(),
        is_winner=not this_listing.active and current_user == current_bid.bidder
    )

    return render(request, "auctions/listing.html", context)



@login_required
def place_bid(request, listing_id):
    """ adds a user bid to a specific listing and stays on same page of the listing with a message displayed if success or failure """

    this_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    current_bid = this_listing.listing_bids.order_by("-amount").first()

    # create the default context
    context = create_context(
        listing=this_listing,
        bid_form=BidForm(),
        comment_form=CommentForm(),
        comments=this_listing.listing_comments.all(),
        current_bid=current_bid,
        total_bids=this_listing.listing_bids.all().count()-1,
        is_listing_in_watchlist=this_listing in current_user.watchlist_listings.all(),
        n_watchlist_listings=current_user.watchlist_listings.all().count()
    )
        
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid(): 
            new_bid_amount = float(bid_form.cleaned_data["bid"])
            # current_bid_amount = current_bid.amount if current_bid else this_listing.price
            if new_bid_amount > current_bid.amount:   
                # create new Bid instance and add it to this listing bids directly
                this_listing.listing_bids.add(Bid.objects.create(amount=new_bid_amount, 
                                                                 bidder=current_user, 
                                                                 listing=this_listing))
                # save this listing update
                this_listing.save()                
                # set message value
                place_bid_message = "New bid placed successfully."
            # otherwise invalid new bid so just set message (error) and other params remain the same
            else:
                place_bid_message = f"Invalid amount. New bid must be higher than current bid (${current_bid.amount})."
            # add the new values of the following variables (arguments that are keys in dict) in the context, the rest remain the same 
            context['current_bid'] = this_listing.listing_bids.order_by("-amount").first()
            context['total_bids'] = this_listing.listing_bids.all().count()-1
            context['bid_flash'] = place_bid_message
            # in both cases redirect to same page with these params
            return render(request, "auctions/listing.html", context)
        # here we have one input only so need to check if form not validated cz simply nothing wld change. 
        # Usually several fields and if one empty makes the form invalid so we send back same inserted field values with redirect
        
    # if GET method use the default context
    else:
        return render(request, "auctions/listing.html", context)



@login_required
def add_comment(request, listing_id):
    """ adds a comment to a specific listing and stays on same page of the listing with a message displayed if success or failure """

    this_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user

    # create the default context
    context = create_context(
        listing=this_listing,
        comment_form=CommentForm(),
        comments=this_listing.listing_comments.all(),
        bid_form=BidForm(),
        current_bid=this_listing.listing_bids.order_by("-amount").first(),
        total_bids=this_listing.listing_bids.all().count()-1,
        is_listing_in_watchlist=this_listing in current_user.watchlist_listings.all(),
        n_watchlist_listings=current_user.watchlist_listings.all().count()
    )
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid(): 
            # create new Bid instance
            new_comment = Comment(
                text = comment_form.cleaned_data["comment"],
                author = request.user,
                listing = this_listing)
            # save this new instance
            new_comment.save()
            # add the new values of the following variables (arguments that are keys in dict) in the context, the rest remain the same 
            context['comments'] = this_listing.listing_comments.all()
            context['comment_flash'] = "New comment added successfully."
            # redirect to same page with new empty comment form
            return render(request, "auctions/listing.html", context)

    # if GET method and use the default context
    else:
        return render(request, "auctions/listing.html", context)
    


@login_required
def delete_comment(request, comment_id):
    """ deletes a comment from a specific listing and stays on same page of the listing with a message displayed if success or failure """

    this_comment = Comment.objects.get(pk=comment_id)
    current_user = request.user
    this_listing = this_comment.listing

    # only author of this comment can delete it
    if this_comment.author == request.user:
        this_comment.delete()

    # create the context
    context = create_context(
        listing=this_listing,
        comment_form=CommentForm(),
        comments=Comment.objects.filter(listing=this_listing).all(),
        bid_form=BidForm(),
        current_bid=this_listing.listing_bids.order_by("-amount").first(),
        total_bids=this_listing.listing_bids.all().count()-1,
        is_listing_in_watchlist=this_listing in current_user.watchlist_listings.all(),
        n_watchlist_listings=current_user.watchlist_listings.all().count(),
        comment_flash="Comment deleted successfully."
    )

    return render(request, "auctions/listing.html", context)



@login_required
def close_auction(request, listing_id):
    """ cloese the auction of a specific listing """

    current_user = request.user
    this_listing = Listing.objects.get(pk=listing_id)
    current_bid = this_listing.listing_bids.order_by("-amount").first()
    # close this auction by making the 'active' attribute False
    this_listing.active = False
    this_listing.save()
    
    # create the context
    context = create_context(
        listing=this_listing,
        bid_form=BidForm(),
        current_bid=current_bid,
        # get all bids number minus the starting bid (price)
        total_bids=this_listing.listing_bids.all().count()-1,
        comment_form=CommentForm(),
        comments=this_listing.listing_comments.all(),
        is_listing_in_watchlist=False if current_user.is_anonymous else this_listing in current_user.watchlist_listings.all(),
        # current_user.is_anonymous means no user logged in, also in case 'category_listings' empty 'n_watchlist_listings' will be 0
        n_watchlist_listings=None if current_user.is_anonymous else current_user.watchlist_listings.all().count(),
        is_winner=not this_listing.active and current_user == current_bid.bidder,
        auction_flash=f'"{this_listing.title.title()}" auction closed successfully.'
    )
    
    return render(request, "auctions/listing.html", context)



# <==================================================<Given Functions>==================================================>
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

