# Generated by Django 4.1.7 on 2023-07-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0023_alter_listing_current_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="total_bids",
            field=models.IntegerField(default=0),
        ),
    ]