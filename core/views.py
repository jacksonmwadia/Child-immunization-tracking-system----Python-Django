from urllib import response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
from .forms import ChildCreateForm, ChildImmunizationForm
from accounts.forms import DoctorRegistrationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from decouple import config
from django.core.mail import send_mail
import datetime

from .africanstalking_configs import sms

# Create your views here.
def IndexView(request, *args, **kwargs):
    vaccines = Vaccines.objects.all()
    context = {
        'vaccines': vaccines
    }
    return render(request, 'index.html', context)

@login_required
def ParentDashboard(request, *args, **kwargs):
    parent = Parent.objects.get(user=request.user)
    parent_children = Child.objects.filter(parent=parent)

    context = {
        'parent': parent,
        'parent_children': parent_children,
    }
    return render(request, 'parent_dashboard.html', context)

@login_required
def parent_profile_settings(request, *args, **kwargs):
    parent = Parent.objects.get(user=request.user)
    context = {
        'parent': parent,
    }
    return render(request, 'profile-settings.html', context)

@login_required
def dashboard_change_password(request, *args, **kwargs):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect(reverse('core:parent-dashboard'))
            messages.error(request, 'New password and confirm password does not match')     
    context = {

    }
    return render(request, 'dashboard_change_password.html', context)

@login_required
def doctor_dashboard(request, *args, **kwargs):
    doctor = Doctor.objects.get(user=request.user)
    doctor_children = Child.objects.filter(doctor=doctor)
    appointments = ChildImmunization.objects.filter(doctor=doctor).filter(is_vaccinated=False).order_by('immunization_date')

    # appointments in the next 30 days
    appointments_next_30_days = ChildImmunization.objects.filter(doctor=doctor).filter(is_vaccinated=False).filter(immunization_date__gte=datetime.date.today()).order_by('immunization_date')
    context = {
        'doctor': doctor,
        'doctor_children': doctor_children,
        'appointments': appointments[:20],
        'total_appointments': appointments_next_30_days,
        'today_appointments': ChildImmunization.objects.filter(doctor=doctor).filter(immunization_date=datetime.date.today()).order_by('immunization_date')
    }
    return render(request, 'doctor_dashboard.html', context)

@login_required
def doctor_children_assigned(request, *args, **kwargs):
    doctor = Doctor.objects.get(user=request.user)
    doctor_children = Child.objects.filter(doctor=doctor)

    context = {
        'doctor': doctor,
        'doctor_children': doctor_children,
    }
    return render(request, 'doctor_children_assigned.html', context)

@login_required
def doctor_appintments(request, *args, **kwargs):
    doctor = Doctor.objects.get(user=request.user)
    doctor_children = Child.objects.filter(doctor=doctor)
    appointments = ChildImmunization.objects.filter(doctor=doctor).filter(is_vaccinated=False).order_by('immunization_date')

    context = {
        'doctor': doctor,
        'doctor_children': doctor_children,
        'appointments': appointments,
    }
    return render(request, 'doctor_appointments.html', context)

@login_required
def doctor_profile_update(request, *args, **kwargs):
    doctor = Doctor.objects.get(user=request.user)
    form = DoctorRegistrationForm(request.POST or None, request.FILES or None, instance=doctor)
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(reverse('core:doctor-dashboard'))
        messages.error(request, 'Profile update failed')

    context = {
        'doctor': doctor,
        'form':form
    }
    return render(request, 'doctor_profile_update.html', context)

@login_required
def create_child(request, *args, **kwargs):
    doctor = Doctor.objects.get(user=request.user)
    form = ChildCreateForm()
    if request.method == 'POST':
        form = ChildCreateForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.doctor = doctor
            child.save()

            # send notification via sms to parent
            # sms_content = "Your child {} has been registered successfully, wait for notifications on vaccination".format(child.first_name)
            # response = sms_provider.send(child.parent.phone_no, sms_content)

            vaccines = Vaccines.objects.all()
            for vaccine in vaccines:
                ChildImmunization.objects.create(
                    child=child,
                    vaccine=vaccine,
                    doctor=doctor,
                    # add duration to today's date given that duration_given is a durationfield
                    immunization_date = datetime.date.today() + datetime.timedelta(days=vaccine.days_to_vaccine)
                    )
            
          
            messages.success(request, 'Child created successfully')
            return HttpResponseRedirect(reverse('core:doctor-dashboard'))
    context = {
        'form': form,
        'doctor':doctor
    }
    return render(request, 'child_form.html', context)

@login_required
def child_profile(request, uuid, *args, **kwargs):
    child = Child.objects.get(uuid=uuid)
    immunizations = ChildImmunization.objects.filter(child=child)
    context = {
        'child': child,
        'child_immunizations':immunizations
    }
    return render(request, 'child_profile.html', context)

@login_required
def child_immunization_detail(request, uuid, *args, **kwargs):
    immunization = get_object_or_404(ChildImmunization, uuid=uuid)
    child = immunization.child
    form = ChildImmunizationForm(request.POST or None, instance=immunization)
    if request.method == 'POST':
        form = ChildImmunizationForm(request.POST, instance=immunization)
        if form.is_valid():
            immunization_form = form.save(commit=False)
            # check if immunization is_vaccinated is True
            if immunization_form.is_vaccinated:
                print(child.parent.phone_no)
                # send notification via sms to parent
                # sms_content = f"Your child {child} has been vaccinated { immunization.vaccine.name } successfully"
                # response = sms.send(sms_content, [f'+{child.parent.phone_no}'])
                
                # print(response)
            immunization_form.save()
            messages.success(request, 'Immunization updated successfully')
            return HttpResponseRedirect(reverse('core:child-profile', kwargs={'uuid':child.uuid}))
        messages.error(request, 'Immunization update failed')

    context = {
        'immunization':immunization,
        'child':child,
        'doctor':immunization.doctor,
        'form':form
    }
    return render(request, 'child_immunization_detail.html', context)


@login_required
def child_profile_update(request, uuid, *args, **kwargs):
    child = Child.objects.get(uuid=uuid)
    if request.method == 'POST':
        form = ChildCreateForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, 'Child profile updated successfully')
            return HttpResponseRedirect(reverse('core:parent-dashboard'))
    else:
        form = ChildCreateForm(instance=child)
    context = {
        'form': form,
    }
    return render(request, 'child_profile_update.html', context)

@login_required
def delete_child(request, uuid, *args, **kwargs):
    child = Child.objects.get(uuid=uuid)
    child.delete()
    messages.success(request, 'Child deleted successfully')
    return HttpResponseRedirect(reverse('core:doctor-dashboard'))



def clients(request, *args, **kwargs):
    clients = Hospital.objects.all()

    context = {
        'clients': clients,
    }
    return render(request, 'hospitals.html', context)



def terms_and_conditions(request, *args, **kwargs):
    return render(request, 'terms_and_conditions.html')

def privacy_policy(request, *args, **kwargs):
    return render(request, 'privacy_policy.html')

def error_404(request, exception):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html')


from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string


# view to generate pdf
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        data = models.Employees.objects.all().order_by('first_name')
        open('templates/temp.html', "w").write(render_to_string('result.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')