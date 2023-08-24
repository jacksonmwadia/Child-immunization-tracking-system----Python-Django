import email
from django.test import TestCase
from .models import User, Doctor, Parent, MOH
from customadmin.models import Hospital, County
# Create your tests here.


class UserTestCase(TestCase):
    # create test user
    def setUp(self):
        self.user = User.objects.create(
            first_name='Test',
            last_name='User',
            username='testuser',
            password = 'testpassword',
        )

    # test user creation
    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.__str__(), self.user.first_name)

    # test user update
    def test_user_update(self):
        self.user.first_name = 'Updated'
        self.user.save()
        self.assertEqual(self.user.first_name, 'Updated')
        
    # test user delete
    def test_user_delete(self):
        self.user.delete()
        self.assertTrue(User.objects.count() == 0)

class DoctorTestCase(TestCase):
    # create test doctor
    def setUp(self):
        self.doctor = Doctor.objects.create(
            user = User.objects.create(
                first_name='Test',
                last_name='Doctor',
                username='testdoctor',
                password = 'testpassword',
            ),
            salutation = 'Dr',
            hospital = Hospital.objects.create(
                name='Test Hospital',
                license_no='123456789',
                county='NAIROBI COUNTY',
                phone_no='123456789',
                address='Test Address',
            ),
            license_no = '123456789',
            email = 'testmail@gmail.com',
            phone_no = '123456789',
            address = 'Test Address',
            speciality = 'Test Speciality',
            is_verified = True,
        )

    # test doctor creation
    def test_doctor_creation(self):
        self.assertTrue(isinstance(self.doctor, Doctor))
        self.assertEqual(self.doctor.__str__(), self.doctor.user.first_name)

    # test doctor update
    def test_doctor_update(self):
        self.doctor.user.first_name = 'Updated'
        self.doctor.save()
        self.assertEqual(self.doctor.user.first_name, 'Updated')

    # test doctor delete
    def test_doctor_delete(self):
        self.doctor.delete()
        self.assertTrue(Doctor.objects.count() == 0)


class ParentTestCase(TestCase):
    # create test parent
    def setUp(self):
        self.parent = Parent.objects.create(
            user = User.objects.create(
                email = 'testmail@gmail.com',
                first_name='Test',
                last_name='Parent',
                username='testparent',
                password = 'testpassword',
            ),
            salutation = 'Mrs',
            email = 'testmail@gmail.com',
            phone_no = '123456789',
            address = 'Test Address',
        )

    # test parent creation
    def test_parent_creation(self):
        self.assertTrue(isinstance(self.parent, Parent))
        self.assertEqual(self.parent.__str__(), self.parent.user.first_name)

    # test parent update
    def test_parent_update(self):
        self.parent.user.first_name = 'Updated'
        self.parent.save()
        self.assertEqual(self.parent.user.first_name, 'Updated')

    # test parent delete
    def test_parent_delete(self):
        self.parent.delete()
        self.assertTrue(Parent.objects.count() == 0)


class MOHTestCase(TestCase):
    # create test MOH
    def setUp(self):
        self.moh = MOH.objects.create(
            user = User.objects.create(
                first_name='Test',
                last_name='MOH',
                username='testmoh',
                password = 'testpassword',
            ),
            salutation = 'Mr',
            email = 'testmail@gmail.com',
            phone_no = '123456789',
            address = 'Test Address',
        )

    # test MOH creation
    def test_moh_creation(self):
        self.assertTrue(isinstance(self.moh, MOH))
        self.assertEqual(self.moh.__str__(), self.moh.user.first_name)

    # test MOH update
    def test_moh_update(self):
        self.moh.user.first_name = 'Updated'
        self.moh.save()
        self.assertEqual(self.moh.user.first_name, 'Updated')

    # test MOH delete
    def test_moh_delete(self):
        self.moh.delete()
        self.assertTrue(MOH.objects.count() == 0)
        