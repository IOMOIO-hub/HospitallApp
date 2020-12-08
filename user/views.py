from datetime import datetime
from time import strptime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from login.models import Appointment, HospitalUser, Doctor


def userPage(request, username):
    user = User.objects.filter(username=username)[0]

    if request.user == user:
        hospital_user = HospitalUser.objects.filter(name=user)[0]
        appointments = Appointment.objects.filter(client_name=hospital_user)

        if request.method == 'POST':
            specialist = request.POST['specialist']
            date = request.POST['date']
            time = request.POST['time']

            if not(validTime(time)) or not(validDate(date)):
                return render(request, 'user/index.html', {'appointments': appointments})

            appointment = Appointment.objects.create(
                doctor=Doctor.objects.all()[1],
                client_name=hospital_user,
                appointment_time=time,
                appointment_date=date,
                client_appeal='Заболел'
            )
            appointment.save()
            appointments.append(appointment)

        return render(request, 'user/index.html', {'appointments': appointments})
    return redirect('/login/')


def validDate(date):
    date = list(map(int, date.split('-')))
    day, month, year = date[2], date[1], date[0]
    datetime(year, month, day)
    try:
        datetime(year, month, day)
    except ValueError:
        return False
    return True


def validTime(time):
    try:
        strptime(time, '%H:%M')
    except ValueError:
        return False
    return True

    # doctors = Doctor.objects.filter(profession='Кардиолог')
    # que = []
    # for doctor in doctors:
    #     que.append(Appointment.objects.filter(doctor=doctor))
    #
    # print(que[0][0].appointment_time)