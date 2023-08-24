from distutils.command.upload import upload
from email.policy import default
from secrets import choice
from tabnanny import verbose
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from customadmin.models import Hospital

COUNTY_CHOICES = (
    ('NAIROBI COUNTY', 'NAIROBI COUNTY'),
    ('KISUMU COUNTY', 'KISUMU COUNTY'),
    ('NYANDARUA COUNTY', 'NYANDARUA COUNTY'),
    ('NAKURU COUNTY', 'NAKURU COUNTY'),
    ('KERICHO COUNTY', 'KERICHO COUNTY'),
    ('BARINGO COUNTY', 'BARINGO COUNTY'),
    ('LAIKIPIA COUNTY', 'LAIKIPIA COUNTY'),
    ('MAKUENI COUNTY', 'MAKUENI COUNTY'),
    ('BOMET COUNTY', 'BOMET COUNTY'),
    ('BUSIA COUNTY', 'BUSIA COUNTY'),
    ('EMBU COUNTY', 'EMBU COUNTY'),
    ('ISIOLO COUNTY', 'ISIOLO COUNTY'),
    ('NANDI COUNTY', 'NANDI COUNTY'),
    ('NAROK COUNTY', 'NAROK COUNTY'),
    ('NYERI COUNTY', 'NYERI COUNTY'),
    ('KAKAMEGA COUNTY', 'KAKAMEGA COUNTY'),
    ('KERICHO COUNTY', 'KERICHO COUNTY'),
    ('BARINGO COUNTY', 'BARINGO COUNTY'),
)


User = settings.AUTH_USER_MODEL
# Create your models here.

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female','Female'),
    ('Other', 'Other')
)

DR_SALUTATIONS = (
    ('Dr', 'Dr'),
    ('RN', 'RN')
)




class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=True)
    is_ministry = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    ver_code = models.CharField(blank=True, null=True, max_length=10)
    profile_picture = models.ImageField(upload_to='images/doctors_profile/%Y/%m', 
                                        default='images/default-avatar.jpg',
                                        blank=True, null=True)
    profile_picture_thumbnail = ImageSpecField(source='profile_picture',
                                            processors=[ResizeToFill(100, 100)],
                                            format='JPEG',
                                            options={'quality': 60}
                                                )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name_plural = 'Users'
        db_table = 'users'
        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salutation = models.CharField(choices=DR_SALUTATIONS, max_length=20)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=True, null=True)
    license_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    speciality = models.CharField(max_length=254, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    profile_picture = models.ImageField(upload_to='images/doctors_profile/%Y/%m', 
                                        default='images/default-avatar.jpg',
                                        blank=True, null=True)
    profile_picture_thumbnail = ImageSpecField(source='profile_picture',
                                            processors=[ResizeToFill(100, 100)],
                                            format='JPEG',
                                            options={'quality': 60}
                                                )
    about = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    doctor_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Doctors'
        db_table = 'doctors'

    def save(self, *args, **kwargs):
        get_id_previous_doctor = Doctor.objects.last().id
        if not self.doctor_id:
            if self.id is None:
                if get_id_previous_doctor is None:
                    self.doctor_id = "D0001"
                else:
                    get_id_previous_doctor = get_id_previous_doctor + 1
                    self.doctor_id = "D" + str(get_id_previous_doctor).zfill(4)
            else:
                self.doctor_id = "D" + str(self.id).zfill(4)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.user.username

class Parent(models.Model):
    parent_id = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/parents_profile/%Y/%m',
                                                    default='images/default-avatar.jpg',
                                                    blank=True, null=True)
    profile_picture_thumbnail = ImageSpecField(source='profile_picture',
                                            processors=[ResizeToFill(100, 100)],
                                            format='JPEG',
                                            options={'quality': 60}
                                                )

    class Meta:
        verbose_name_plural = 'Parents'
        db_table = 'parents'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            get_id_previous_parent = Parent.objects.last().id
        except Parent.DoesNotExist:
            get_id_previous_parent = 0
        if not self.parent_id:
            if self.id is None:
                if get_id_previous_parent is None:
                    self.parent_id = "P0001"
                get_id_previous_parent = get_id_previous_parent + 1
                self.parent_id = "P" + str(get_id_previous_parent).zfill(4)
            self.parent_id = "P" + str(self.id).zfill(4)
        super().save(*args, **kwargs)
        

class MOH(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'MOH'
        db_table = 'moh'

    def __str__(self):
        return self.user.username