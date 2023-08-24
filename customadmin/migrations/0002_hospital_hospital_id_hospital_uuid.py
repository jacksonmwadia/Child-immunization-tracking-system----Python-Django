# Generated by Django 4.0.4 on 2022-06-18 12:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='hospital_id',
            field=models.CharField(blank=True, max_length=5, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
