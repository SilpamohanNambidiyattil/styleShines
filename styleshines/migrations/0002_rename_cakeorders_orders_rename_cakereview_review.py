# Generated by Django 4.2 on 2023-12-29 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('styleshines', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CakeOrders',
            new_name='Orders',
        ),
        migrations.RenameModel(
            old_name='CakeReview',
            new_name='Review',
        ),
    ]
