import uuid, datetime
from django.db import models
from accounts.models import Parent, Doctor
from django.urls import reverse
from django.conf import settings


from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import redis
from .africanstalking_configs import sms

# Create your models here.

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

#vaccines given to kids
VACCINE_CHOICES = (
    ('BCG', 'BCG'),
    ('OPV', 'OPV'),
    ('DPT', 'DPT'),
    ('HPB', 'HEPATITIS B'),
    ('HPA', 'HEPATITIS A'),
    ('MEA', 'MEASLES')
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


class Child(models.Model):
    child_id = models.CharField(max_length=5, unique=True, blank=True, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    birth_no = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=13)
    mothers_name = models.CharField(max_length=254, blank=True, null=True)
    fathers_name = models.CharField(max_length=254, blank=True, null=True)
    date_of_registration = models.DateTimeField()
    date_of_birth = models.DateTimeField()
    birth_facility = models.CharField(max_length=254, blank=True, null=True)
    birth_county = models.CharField(max_length=254, choices=COUNTY_CHOICES)
    resident_county = models.CharField(choices=COUNTY_CHOICES, max_length=50, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/children/%Y/%m/%d',
                                        blank=True, null=True, 
                                        default='images/default-avatar.jpg')
    profile_picture_thumbnail = ImageSpecField(source='profile_picture',
                                            processors=[ResizeToFill(100, 100)],
                                            format='JPEG',
                                            options={'quality': 60}
                                            )
    is_defaulter = models.BooleanField(default=False)   



    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('core:child-profile', kwargs={'uuid': self.uuid})

    def get_child_age(self):
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month:
            age -= 1
        elif today.month == self.date_of_birth.month:
            if today.day < self.date_of_birth.day:
                age -= 1
        return age * 12 + (today.month - self.date_of_birth.month)


    def save(self, *args, **kwargs):
        try:
            get_id_last_child = Child.objects.last().id
        except:
            get_id_last_child = 0
        if not self.child_id:
            if self.id is None:
                if get_id_last_child is None:
                    self.child_id = 'C0001'
                else:
                    new_id = get_id_last_child + 1
                    self.child_id = 'C' + str(new_id).zfill(4)
            else:
                self.child_id = 'C' + str(self.id).zfill(4)
        super().save(*args, **kwargs)


    
    class Meta:
        verbose_name_plural = 'Children'
        db_table = 'child'



class Vaccines(models.Model):
    # vaccine_id with 4 digits start with V
    vaccine_id = models.CharField(max_length=5, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=254, blank=True, null=True)
    time_given = models.CharField(max_length=254, blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    duration_given = models.DurationField(blank=True, null=True, default=None)
    picture = models.ImageField(upload_to='vaccines/%Y/%m/%d',
                                blank=True, null=True)
    picture_thumbnail = ImageSpecField(source='picture',
                                        processors=[ResizeToFill(100, 100)],
                                        format='JPEG',
                                        options={'quality': 60}
                                        )
    days_to_vaccine = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vaccine'
        verbose_name_plural = 'Vaccines'
        db_table = 'vaccines'

    def get_absolute_url(self):
        return reverse('core:vaccine-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        try:
            get_id_previous_vaccine = Vaccines.objects.last().id
        except:
            get_id_previous_vaccine = 0
        if not self.vaccine_id:
            if self.id is None:
                if get_id_previous_vaccine is None:
                    self.vaccine_id = "V0001"
                else:
                    get_id_previous_vaccine = get_id_previous_vaccine + 1
                    self.vaccine_id = "V" + str(get_id_previous_vaccine).zfill(4)
            else:
                self.vaccine_id = "V" + str(self.id).zfill(4)
        super().save(*args, **kwargs)



class ChildImmunization(models.Model):
    child_immunization_id = models.CharField(max_length=5, unique=True, blank=True, null=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccines, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    comment = models.TextField(max_length=254, blank=True, null=True)
    immunization_date = models.DateTimeField(blank=True, null=True)
    date_given = models.DateTimeField(blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    is_vaccinated = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'Child Immunization'
        verbose_name_plural = 'Child Immunizations'
        db_table = 'child_immunization'

    def get_absolute_url(self):
        return reverse("core:child-immunization-detail", kwargs={"uuid": self.uuid})

    def __str__(self):
        return f"{self.child.first_name} {self.child.last_name} {self.vaccine.name}"

    def save(self, *args, **kwargs):
        try:
            get_id_of_previous_record = ChildImmunization.objects.last().id
        except:
            get_id_of_previous_record = 0
        if not self.child_immunization_id:
            if self.id is None:
                if get_id_of_previous_record:
                    new_id = get_id_of_previous_record + 1
                    self.child_immunization_id = 'I' + str(new_id).zfill(4)
                else:
                    self.child_immunization_id = 'I' + str(1).zfill(4)
            else:
                self.child_immunization_id = 'I' + str(self.id).zfill(4)
        super().save(*args, **kwargs)

    def schedule_reminder(self):
        appointment_time = self.immunization_date
        reminder_time = appointment_time - datetime.timedelta(days=2)
        now = datetime.datetime.now()
        milli_to_wait = int(
            (reminder_time - now).total_seconds()) * 1000

        # schedule the reminder
        from .views import send_sms_reminder
        response = send_sms_reminder.send_with_options(
            args = [self.uuid],
            delay = milli_to_wait,
        )
        return response.options['redis_message_id']

    def cancel_task(self):
        redis_client = redis.Redis(host=settings.REDIS_LOCAL, port=6379, db=0)
        redis_client.hdel("dramatiq:default.DQ.msgs", self.task_id)

    