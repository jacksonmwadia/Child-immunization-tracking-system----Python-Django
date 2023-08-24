# Generated by Django 4.0.4 on 2022-06-18 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0002_hospital_hospital_id_hospital_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='county',
            options={'ordering': ['county_no'], 'verbose_name_plural': 'Counties'},
        ),
        migrations.AddField(
            model_name='county',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]