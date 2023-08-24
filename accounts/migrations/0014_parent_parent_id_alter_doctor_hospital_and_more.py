# Generated by Django 4.0.4 on 2022-06-18 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0004_hospital_phone_no'),
        ('accounts', '0013_doctor_doctor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='parent_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customadmin.hospital'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.DeleteModel(
            name='Hospital',
        ),
    ]
