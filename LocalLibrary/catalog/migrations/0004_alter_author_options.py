# Generated by Django 4.0.2 on 2022-06-28 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['name'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
