# Generated by Django 5.1.4 on 2024-12-19 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
