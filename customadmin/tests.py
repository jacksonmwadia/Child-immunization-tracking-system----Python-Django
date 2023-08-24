from django.test import TestCase
from .models import Hospital, County

# Create your tests here.

class HospitalTestCase(TestCase):
    # create test hospital
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name='Test Hospital',
            license_no='123456789',
            county='NAIROBI COUNTY',
            phone_no='123456789',
            address='Test Address',
        )

    # test hospital creation
    def test_hospital_creation(self):
        self.assertTrue(isinstance(self.hospital, Hospital))
        self.assertEqual(self.hospital.__str__(), self.hospital.name)

    # test hospital update
    def test_hospital_update(self):
        self.hospital.name = 'Updated Hospital'
        self.hospital.save()
        self.assertEqual(self.hospital.name, 'Updated Hospital')

    # test hospital delete
    def test_hospital_delete(self):
        self.hospital.delete()
        self.assertTrue(Hospital.objects.count() == 0)

class CountyTestCase(TestCase):
    # create test county
    def setUp(self):
        self.county = County.objects.create(
            name='Test County',
            county_no=1,
        )

    # test county creation
    def test_county_creation(self):
        self.assertTrue(isinstance(self.county, County))
        self.assertEqual(self.county.__str__(), self.county.name)

    # test county update
    def test_county_update(self):
        self.county.name = 'Updated County'
        self.county.save()
        self.assertEqual(self.county.name, 'Updated County')

    # test county delete
    def test_county_delete(self):
        self.county.delete()
        self.assertTrue(County.objects.count() == 0)