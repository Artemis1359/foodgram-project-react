# Generated by Django 4.2.6 on 2023-11-05 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_alter_favorite_recipe_alter_favorite_user_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="favorite",
            name="unique_favorite_fields",
        ),
        migrations.RemoveConstraint(
            model_name="shoppingcart",
            name="unique_shopping_cart_fields",
        ),
    ]
