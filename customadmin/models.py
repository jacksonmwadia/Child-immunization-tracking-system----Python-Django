import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.


class County(models.Model):
    name = models.CharField(max_length=100)
    county_no = models.PositiveSmallIntegerField(unique=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)+"-"+str(self.county_no)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Counties'
        ordering = ['county_no']
        db_table = 'counties'

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=254)
    image = models.ImageField(upload_to='hospital_images', blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(470, 313)], format='JPEG', options={'quality': 60})
    license_no = models.CharField(max_length=20, blank=True, null=True)
    county = models.ForeignKey(County, blank=True, null=True, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name_plural = 'Hospitals'
        ordering = ['name']
        db_table = 'hospitals'

    def __str__(self):
        return f'{self.name} -> { self.county }'

    def get_absolute_url(self):
        return reverse('custom-admin:hospital-detail', kwargs={'uuid': self.uuid})
