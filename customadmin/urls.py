from django.urls import path

from customadmin.views import *

app_name = 'custom-admin'

urlpatterns = [
    path('', IndexView, name='index'),
    path('doctors/', DoctorList, name='doctors'),
    path('doctors/<int:pk>/', DoctorDetail, name='doctor-detail'),
    path('doctors/<int:pk>/suspend/', suspendDoctor, name='suspend-doctor'),
    path('doctors/<int:pk>/delete/', DoctorDelete, name='doctor-delete'),
    path('doctors/create/', DoctorCreate, name='doctor-create'),
    path('parents/', ParentList, name='parents'),
    path('parents/<int:pk>/', ParentDetail, name='parent-detail'),
    path('parents/<int:pk>/delete/', ParentDelete, name='parent-delete'),
    path('parents/create/', ParentCreate, name='parent-create'),
    path('children/', ChildList, name='children'),
    path('children/<int:pk>/', ChildDetail, name='child-detail'),
    path('children/<int:pk>/delete/', ChildDelete, name='child-delete'),
    path('children/create/', ChildCreate, name='child-create'),
    path('vaccines/', VaccinesList, name='vaccines'),
    path('vaccines/<int:pk>/', VaccinesDetail, name='vaccines-detail'),
    path('vaccines/<int:pk>/delete/', VaccinesDelete, name='vaccines-delete'),
    path('vaccines/create/', VaccinesCreate, name='vaccines-create'),
    path('counties/', CountiesList, name='counties'),
    path('counties/<slug>/', CountiesDetail, name='counties-detail'),
    path('hospitals/', HospitalList, name='hospitals'),
    path('hospitals/<uuid>/', HospitalDetail, name='hospital-detail'),
    path('hospitals/<uuid>/delete/', HospitalDelete, name='hospital-delete'),
    

    
]
