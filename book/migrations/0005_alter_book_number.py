# Generated by Django 5.1.4 on 2024-12-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_book_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='number',
            field=models.IntegerField(),
        ),
    ]
