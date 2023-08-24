# Generated by Django 4.0 on 2022-05-26 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_create_at_child_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='birth_county',
            field=models.CharField(choices=[('NAIROBI COUNTY', 'NAIROBI COUNTY'), ('KISUMU COUNTY', 'KISUMU COUNTY'), ('NYANDARUA COUNTY', 'NYANDARUA COUNTY'), ('NAKURU COUNTY', 'NAKURU COUNTY'), ('KERICHO COUNTY', 'KERICHO COUNTY'), ('BARINGO COUNTY', 'BARINGO COUNTY'), ('LAIKIPIA COUNTY', 'LAIKIPIA COUNTY'), ('MAKUENI COUNTY', 'MAKUENI COUNTY'), ('BOMET COUNTY', 'BOMET COUNTY'), ('BUSIA COUNTY', 'BUSIA COUNTY'), ('EMBU COUNTY', 'EMBU COUNTY'), ('ISIOLO COUNTY', 'ISIOLO COUNTY'), ('NANDI COUNTY', 'NANDI COUNTY'), ('NAROK COUNTY', 'NAROK COUNTY'), ('NYERI COUNTY', 'NYERI COUNTY'), ('KAKAMEGA COUNTY', 'KAKAMEGA COUNTY'), ('KERICHO COUNTY', 'KERICHO COUNTY'), ('BARINGO COUNTY', 'BARINGO COUNTY')], max_length=254),
        ),
        migrations.AlterField(
            model_name='child',
            name='resident_county',
            field=models.CharField(blank=True, choices=[('NAIROBI COUNTY', 'NAIROBI COUNTY'), ('KISUMU COUNTY', 'KISUMU COUNTY'), ('NYANDARUA COUNTY', 'NYANDARUA COUNTY'), ('NAKURU COUNTY', 'NAKURU COUNTY'), ('KERICHO COUNTY', 'KERICHO COUNTY'), ('BARINGO COUNTY', 'BARINGO COUNTY'), ('LAIKIPIA COUNTY', 'LAIKIPIA COUNTY'), ('MAKUENI COUNTY', 'MAKUENI COUNTY'), ('BOMET COUNTY', 'BOMET COUNTY'), ('BUSIA COUNTY', 'BUSIA COUNTY'), ('EMBU COUNTY', 'EMBU COUNTY'), ('ISIOLO COUNTY', 'ISIOLO COUNTY'), ('NANDI COUNTY', 'NANDI COUNTY'), ('NAROK COUNTY', 'NAROK COUNTY'), ('NYERI COUNTY', 'NYERI COUNTY'), ('KAKAMEGA COUNTY', 'KAKAMEGA COUNTY'), ('KERICHO COUNTY', 'KERICHO COUNTY'), ('BARINGO COUNTY', 'BARINGO COUNTY')], max_length=50, null=True),
        ),
    ]
