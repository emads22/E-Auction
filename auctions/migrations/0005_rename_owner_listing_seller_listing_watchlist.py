# Generated by Django 4.1.7 on 2023-07-17 06:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_alter_listing_date_added"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="owner",
            new_name="seller",
        ),
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]