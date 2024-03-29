# Generated by Django 3.1.4 on 2021-01-03 13:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20210103_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boundingbox',
            name='sid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='sid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
