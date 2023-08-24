from django.shortcuts import render
from accounts.models import Doctor, Parent
from core.models import *
from .forms import VaccineForm, HospitalForm
from django.http import HttpResponseRedirect
from .models import Hospital, County
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def IndexView(request):
    doctors = Doctor.objects.filter(is_verified=True)
    parents = Parent.objects.all()
    children = Child.objects.all()
    registered_hospitals = Hospital.objects.all()
    vaccines = Vaccines.objects.all()
    vaccine_defaulters = Child.objects.filter(is_defaulter=True)

    context = {
        'doctors':doctors,
        'parents':parents,
        'children':children,
        'registered_hospitals':registered_hospitals,
        'vaccines':vaccines,
        'vaccine_defaulters':vaccine_defaulters
    }
    return render(request, 'admin-dash/index.html', context)

def DoctorList(request, *args, **kwargs):
    doctors = Doctor.objects.all()

    context = {
        'doctors':doctors
    }
    return render(request, 'admin-dash/doctors.html', context)

def DoctorDetail(request, pk):
    doctor = Doctor.objects.get(pk=pk)

    context = {
        'doctor':doctor
    }
    return render(request, 'admin-dash/doctor_profile.html', context)

def suspendDoctor(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    doctor.is_active = False
    doctor.is_verified = False
    doctor.save()

    return HttpResponseRedirect(reverse('custom-admin:doctors'))

def DoctorDelete(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    doctor.delete()

    return render(request, 'admin-dash/index.html')

def DoctorCreate(request, *args, **kwargs):
    return render(request, 'admin-dash/doctor-create.html')


def ParentList(request, *args, **kwargs):
    parents = Parent.objects.all()

    context = {
        'parents':parents
    }
    return render(request, 'admin-dash/parents.html', context)

def ParentDetail(request, pk):
    parent = Parent.objects.get(pk=pk)

    parent_children = parent.child_set.all()

    context = {
        'parent':parent,
        'parent_children':parent_children
    }
    return render(request, 'admin-dash/parent-detail.html', context)

def ParentDelete(request, pk):
    parent = Parent.objects.get(pk=pk)
    parent.delete()

    return render(request, 'admin-dash/index.html')

def ParentCreate(request, *args, **kwargs):
    return render(request, 'admin-dash/parent-create.html')

def ChildList(request, *args, **kwargs):
    children = Child.objects.all()

    context = {
        'children':children
    }
    return render(request, 'admin-dash/children.html', context)

def ChildDetail(request, pk):
    child = Child.objects.get(pk=pk)

    context = {
        'child':child
    }
    return render(request, 'admin-dash/child-detail.html', context)

def ChildDelete(request, pk):
    child = Child.objects.get(pk=pk)
    child.delete()

    return render(request, 'admin-dash/index.html')

def ChildCreate(request, *args, **kwargs):
    return render(request, 'admin-dash/child-create.html')

def VaccinesList(request, *args, **kwargs):
    vaccines = Vaccines.objects.all()
    form = VaccineForm()
    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('custom-admin:vaccines'))

    context = {
        'vaccines':vaccines,
        'form':form
    }
    return render(request, 'admin-dash/vaccines.html', context)

def VaccinesDetail(request, pk):
    vaccine = Vaccines.objects.get(pk=pk)
    form = VaccineForm(instance=vaccine)

    if request.method == 'POST':
        form = VaccineForm(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('custom-admin:vaccines-detail', kwargs={'pk':pk}))

    context = {
        'vaccine':vaccine,
        'form':form
    }
    return render(request, 'admin-dash/vaccine_detail.html', context)

def VaccinesDelete(request, pk):
    vaccine = Vaccines.objects.get(pk=pk)
    vaccine.delete()

    return HttpResponseRedirect(reverse('custom-admin:vaccines'))

def VaccinesCreate(request, *args, **kwargs):
    return render(request, 'admin-dash/vaccines-create.html')

def CountiesList(request, *args, **kwargs):
    counties = County.objects.all()

    context = {
        'counties':counties
    }
    return render(request, 'admin-dash/counties.html', context)

def CountiesDetail(request, slug):
    county = County.objects.get(slug=slug)

    context = {
        'county':county
    }
    return render(request, 'admin-dash/county-detail.html', context)



def HospitalList(request, *args, **kwargs):
    form = HospitalForm()
    hospitals = Hospital.objects.all()

    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect(reverse('custom-admin:hospitals'))
        print(form.errors)
    context = {
        'hospitals':hospitals,
        'form':form
    }
    return render(request, 'admin-dash/hospitals.html', context)


def HospitalDetail(request, uuid):
    hospital = Hospital.objects.get(uuid=uuid)

    context = {
        'hospital':hospital
    }
    return render(request, 'admin-dash/hospital-detail.html', context)

@login_required
def HospitalDelete(request, uuid):
    hospital = Hospital.objects.get(uuid=uuid)
    hospital.delete()

    return HttpResponseRedirect(reverse('custom-admin:hospitals'))

