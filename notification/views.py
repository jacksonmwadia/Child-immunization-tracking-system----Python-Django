from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import *
from accounts.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from decouple import config
from django.core.mail import send_mail
import datetime

from core.africanstalking_configs import sms
# Create your views here.


@login_required
def doctor_send_notification(request, *args, **kwargs):
    parents = Parent.objects.all()
    if request.user.is_doctor:
        doctor = Doctor.objects.get(user=request.user)
    
        parents_phone_numbers = []
        

        if request.method == 'POST':
            for parent in parents:
                if parent.user.phone_no is not None:
                    parents_phone_numbers.append('+254'+str(parent.user.phone_no[-9:]))
            print(parents_phone_numbers)
            message = request.POST.get('message')
            response = sms.send(message, parents_phone_numbers)
            print(response)
            # save response to media folder in a file called sms_response.txt
          
            messages.success(request, 'Notification sent successfully')
            return HttpResponseRedirect(reverse('core:doctor-dashboard'))
        context = {
            'doctor': doctor,
        }
        return render(request, 'doctor_send_notification.html', context)
    messages.error(request, 'You are not authorized to perform this action')
    return HttpResponseRedirect(reverse('core:index'))



@login_required
def send_vaccine_notifications(request, *args, **kwargs):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        child_id = request.POST.get('child_id')
        child = Child.objects.get(id=child_id)
        sms_content = f"This is to reminde you of your next immunization appointment for {child.first_name} is scheduled at (hospital name) on (due_date)We look forward to seeing you then"
        response = sms.send(f"+{child.parent.phone_no}", sms_content)
        print(response)
        messages.success(request, 'Notification sent successfully')
        return HttpResponseRedirect(reverse('core:doctor-dashboard'))
    context = {
        'doctor': doctor,
    }
    return render(request, 'send_vaccine_notifications.html', context)

def send_sms_reminder(request, uuid, *args, **kwargs):  
    try:
        child_immunization = ChildImmunization.objects.get(uuid=uuid)
    except ChildImmunization.DoesNotExist:
        pass

    appointment_time = child_immunization.immunization_date
    message = f"This is to remind you of your next immunization appointment for {child_immunization.child.first_name} is scheduled at (hospital name) on {appointment_time}We look forward to seeing you then"
    response = sms.send(f"{message}", [f'+{child_immunization.child.parent.phone_no}'])