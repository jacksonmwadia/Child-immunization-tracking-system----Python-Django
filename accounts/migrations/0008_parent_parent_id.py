# Generated by Django 4.0 on 2022-06-01 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_doctor_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='parent_id',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
