# Generated by Django 4.0 on 2022-06-05 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_rename_vac_id_vaccines_vaccine_id_child_child_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccines',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='vaccines/%Y/%m/%d'),
        ),
    ]
