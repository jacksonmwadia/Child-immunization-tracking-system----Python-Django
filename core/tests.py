from django.test import TestCase
from django.urls import reverse
from .models import Child, ChildImmunization, Vaccines
import datetime

# Create your tests here.

class ChildTestCase(TestCase):
    # create test child
    def setUp(self):
        self.child = Child.objects.create(
            name='Test Child', birth_no='123456789', first_name='Test', last_name='Child',
            mothers_name='Test Mother', fathers_name='Test Father',
            date_of_registration=datetime.date.today(), date_of_birth=datetime.date.today(),
            birth_county='NAIROBI COUNTY', resident_county='NAIROBI COUNTY',
            birth_facility='Test Facility', height=1, weight=1, doctor=1,
        )

    # test child creation
    def test_child_creation(self):
        self.assertTrue(isinstance(self.child, Child))
        self.assertEqual(self.child.__str__(), self.child.name)

    # test child update
    def test_child_update(self):
        self.child.name = 'Updated Child'
        self.child.save()
        self.assertEqual(self.child.name, 'Updated Child')

    # test child delete
    def test_child_delete(self):
        self.child.delete()
        self.assertTrue(Child.objects.count() == 0)


class ChildImmunizationTestCase(TestCase):
    # create test child immunization
    def setUp(self):
        self.child_immunization = ChildImmunization.objects.create(
            child=1, vaccine=1, date_given=datetime.date.today(),
        )

    # test child immunization creation
    def test_child_immunization_creation(self):
        self.assertTrue(isinstance(self.child_immunization, ChildImmunization))
        self.assertEqual(self.child_immunization.__str__(), self.child_immunization.child.name)

    # test child immunization update
    def test_child_immunization_update(self):
        self.child_immunization.child = 2
        self.child_immunization.save()
        self.assertEqual(self.child_immunization.child.id, 2)

    # test child immunization delete
    def test_child_immunization_delete(self):
        self.child_immunization.delete()
        self.assertTrue(ChildImmunization.objects.count() == 0)


class VaccineTestCase(TestCase):
    # create test vaccine
    def setUp(self):
        self.vaccine = Vaccines.objects.create(
            name='Test Vaccine',
            description='Test Description',
            manufacturer='Test Manufacturer',
            lot_no='Test Lot No',
            expiry_date=datetime.date.today(),
            price=1,
            quantity=1,
        )

    # test vaccine creation
    def test_vaccine_creation(self):
        self.assertTrue(isinstance(self.vaccine, Vaccines))
        self.assertEqual(self.vaccine.__str__(), self.vaccine.name)

    # test vaccine update
    def test_vaccine_update(self):
        self.vaccine.name = 'Updated Vaccine'
        self.vaccine.save()
        self.assertEqual(self.vaccine.name, 'Updated Vaccine')

    # test vaccine delete
    def test_vaccine_delete(self):
        self.vaccine.delete()
        self.assertTrue(Vaccines.objects.count() == 0)

