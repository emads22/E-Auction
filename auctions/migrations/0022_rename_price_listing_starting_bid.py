# Generated by Django 4.1.7 on 2023-07-22 16:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0021_listing_current_bid_alter_listing_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="price",
            new_name="starting_bid",
        ),
    ]
