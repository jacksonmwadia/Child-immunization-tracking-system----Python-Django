# Generated by Django 4.0 on 2022-05-30 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_parent_profile_picture_alter_doctor_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]