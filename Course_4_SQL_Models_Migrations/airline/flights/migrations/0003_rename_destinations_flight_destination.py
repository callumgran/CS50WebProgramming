# Generated by Django 4.0 on 2021-12-31 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_airport_remove_flight_destination_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='destinations',
            new_name='destination',
        ),
    ]