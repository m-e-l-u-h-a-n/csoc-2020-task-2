# Generated by Django 2.2.1 on 2020-05-03 10:27

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200502_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating_u',
            field=jsonfield.fields.JSONField(default=None),
        ),
    ]
