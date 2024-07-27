import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from vitaral_nutrition_app.models import competitors_info, competitors_payment_info, competition, initial_form_info, my_acc_info, timer_info, analytic_model, discount_code
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
import urllib.request
import json

# GOOGLE_RECAPTCHA_SECRET_KEY = '6Le0DPgUAAAAAIVCTrJ0pTmFedS-vb4gJ-sPwX-A'

def check_code(request):
    if request.method == 'POST':
        code = request.POST['discount']
        try:
            m = discount_code.objects.get(code=code)
            return HttpResponse(m.discount)
        except ObjectDoesNotExist:
            return HttpResponse("errorincode")

def index(request):
    a = analytic_model.objects.first()
    a.home_page = a.home_page+1
    a.save()
    return render(request, 'vitaral_nutrition_app/index.html')


def how_it_works(request):
    a = analytic_model.objects.first()
    a.how_it_work_page = a.how_it_work_page+1
    a.save()
    return render(request, 'vitaral_nutrition_app/how_it_works.html')


def timer(request):
    timer = timer_info.objects.first()
    context = {
        'month_name': timer.month_name,
        'days': timer.days,
        'year': timer.year
    }
    data = json.dumps(context, indent=4, sort_keys=True, default=str)
    return HttpResponse(data, content_type='application/json')


@login_required(function=None, login_url='user_form')
def questions_2(request):
    model = competition
    user = request.user.username
    m = competitors_info.objects.get(username=user)
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        correct_answer = request.POST['correct_answer']
        model.objects.create(i_id=m, question=question, answer=answer, correct_answer=correct_answer)
        return HttpResponse("Added")
    else:
        return HttpResponse("Failed")


def email_my_frnd(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']

        name = name + ' ' + surname

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "WIN WIN The 316Ti Executive Set"
        html = """
            <html>
              <head>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
              </head>
              <body>
                <h1>Hi %s</h1>
                <p>I have just entered this raffle competition and thought this would be great opportunity for you since you are a great cook, health conscious and love a beautiful kitchen.</p>
                <img class='text-center mx-auto' src='https://competition.vitaral.co.uk/static/email.png' style='width: 200px;'><br>
                <button class="btn btn-primary"><a href="competition.vitaral.co.uk">Click Here</a></button>
              </body>
            </html>
            """ % name
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.login('316ticompetition@gmail.com', 'tT#263478#')
        smtp_server.sendmail("316ticompetition@gmail.com", email, msg.as_string())
        smtp_server.close()
        return redirect('index')
    else:
        return HttpResponse("Try Again Later...")


def initial_form(request):
    if request.method == 'POST':
        fname = request.POST['id_fname']
        lname = request.POST['id_lname']
        email = request.POST['id_email']
        agree = request.POST['agree']
        set_name = request.POST['set_name']
        # recaptcha_response = request.POST['g-recaptcha-response']

        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # payload = {
        #     'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.parse.urlencode(payload).encode()
        # req = urllib.request.Request(url, data=data)
        # response = urllib.request.urlopen(req)
        # result = json.loads(response.read().decode())

        # if (not result['success']) or (not result['action'] == 'initial'):
        #     e = 'Invalid reCAPTCHA. Please try again.'
        #     return render(request, 'vitaral_nutrition_app/registration.html', {'e': e})



        other_set_name = request.POST['other_set_name']
        initial_form_info.objects.update_or_create(
             first_name=fname,
             last_name=lname,
             email=email,
             agree=agree,
             cookware_set=set_name,
             other_cook_set=other_set_name
        )
        return redirect('index')
    else:
        a = analytic_model.objects.first()
        a.initial_page = a.initial_page+1
        a.save()
        return render(request, 'vitaral_nutrition_app/initial_form.html')


@login_required(function=None, login_url='user_form')
def upload_my_picture(request):
    user = request.user.username
    u = User.objects.get(username=user)
    if request.method == 'POST':
        profile_picture = request.FILES['p_picture']
        try:
            m = my_acc_info.objects.get(i_id=u)
            m.profile_picture = profile_picture
            m.save()
        except ObjectDoesNotExist:
            my_acc_info.objects.update_or_create(i_id=u, bio='', profile_picture=profile_picture)
        return redirect('my_account')


def change_email(request):
    if request.method == 'POST':
        user = request.user.username
        u = User.objects.get(username=user)
        email = request.POST['changed_email']
        u.email = email
        u.save()
        return HttpResponse("Email Updated")
    else:
        return HttpResponse("Try Again Later")


def change_password(request):
    if request.method == 'POST':
        user = request.user.username
        u = User.objects.get(username=user)
        new_password = request.POST['new_password']
        u.set_password(new_password)
        u.save()
        return redirect('user_form')
    else:
        return HttpResponse("Try Again Later")


def my_acc(request):
    user = request.user.username
    u = User.objects.get(username=user)
    if request.method == 'POST':
        bio = request.POST['bio']
        try:
            m = my_acc_info.objects.get(i_id=u)
            m.bio = bio
            m.save()
        except ObjectDoesNotExist:
            my_acc_info.objects.update_or_create(i_id=u, bio=bio, profile_picture='')
        return HttpResponse("Bio Updated")
    else:
        try:
            m = my_acc_info.objects.get(i_id=u)
        except ObjectDoesNotExist:
            return render(request, 'vitaral_nutrition_app/my_account.html')
        try:
            c = competitors_info.objects.get(username=user)
            if c.are_you_eating_heathier:
                healthy = ''
            else:
                healthy = 'not'
            print(c.are_you_eating_heathier)
            obj = {
                'healthy': healthy,
                'p_picture': m.profile_picture,
                'bio': m.bio
            }
            return render(request, 'vitaral_nutrition_app/my_account.html', obj)
        except ObjectDoesNotExist:
            obj = {
                'p_picture': m.profile_picture,
                'bio': m.bio
            }
            return render(request, 'vitaral_nutrition_app/my_account.html', obj)


@login_required(function=None, login_url='user_form')
def competition_completion(request):
    user = request.user.username
    a = analytic_model.objects.first()
    a.thank_you = a.thank_you+1
    a.save()
    m = competitors_info.objects.get(username=user)
    m.competition_given = 1
    m.save()
    return redirect('thanku_page')


@login_required(function=None, login_url='user_form')
def add_my_answer(request):
    model = competition
    user = request.user.username
    m = competitors_info.objects.get(username=user)
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        correct_answer = request.POST['correct_answer']
        model.objects.create(i_id=m, question=question, answer=answer, correct_answer=correct_answer)
        return HttpResponse("Added")
    else:
        return HttpResponse("Failed")


@login_required(function=None, login_url='user_form')
def payment_data(request):
    user = request.user.username
    if request.method == 'POST':
        m = competitors_info.objects.get(username=user)
        payer_mail = request.POST['payer_mail']
        payer_id = request.POST['payer_id']
        status = request.POST['status']
        entries = request.POST['entries']
        c_time = request.POST['c_time']
        order_id = request.POST['order_id']
        payer_country_code = request.POST['payer_country_code']
        p = competitors_payment_info()
        p.i_id = m
        p.payer_mail = payer_mail
        p.payer_id = payer_id
        p.status = status
        p.order_id = order_id
        p.payer_country_code = payer_country_code
        p.c_time = c_time
        p.save()

        m.paid = 1
        if entries == '':
            pass
        else:
            m.entries = entries
            m.not_used_entries = 15 - int(entries)
        m.save()
        return HttpResponse("Done")
    else:
        m = competitors_info.objects.get(username=user)
        p = competitors_payment_info.objects.filter(i_id=m)
        details = serializers.serialize('json', p)
        return HttpResponse(details)


def participators_details(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        surname = request.POST['surname']

        username = request.POST['username']
        email = request.POST['email']
        id_password = request.POST['password']

        entries = request.POST['entries']
        region = request.POST['region']
        eating_healthier = request.POST['eating_healthier']
        agree = request.POST['agree']

        # recaptcha_response = request.POST['grecaptcharesponse']

        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # payload = {
        #     'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.parse.urlencode(payload).encode()
        # req = urllib.request.Request(url, data=data)
        # response = urllib.request.urlopen(req)
        # result = json.loads(response.read().decode())

        # if (not result['success']) or (not result['action'] == 'signup'):
        #     e = 'Invalid reCAPTCHA. Please try again.'
        #     return render(request, 'vitaral_nutrition_app/registration.html', {'e': e})

        u_name = User.objects.filter(username=username)
        e_mail = User.objects.filter(email=email)

        if u_name and e_mail:
            pass
        else:
            user = User.objects.create(username=username,  email=email, password=id_password)
            user.set_password(id_password)
            user.save()
            login(request, user)
        m = competitors_info()
        m.paid = 0
        m.username = username
        m.firstname = firstname
        m.surname = surname
        m.email = email
        m.region = region
        m.are_you_eating_heathier = eating_healthier
        m.agree = agree
        m.entries = entries
        m.save()
        return HttpResponse(m.entries)


#@login_required(function=None, login_url='user_form')
def way_to_competition(request):
    try:
        model = competitors_info.objects.get(username=request.user.username)
        p = model.paid
        p_id = model.id
        com_given = model.competition_given
        entry = model.entries
        if com_given == 1:
            if model.not_used_entries:
                dict = {
                    'not_used_entry': model.not_used_entries
                }
                return render(request, 'vitaral_nutrition_app/questions_page_2.html', dict)
            return redirect('thanku_page')
        elif p == 1:
            dict = {
                'entry': entry
            }
            return render(request, 'vitaral_nutrition_app/questions_page.html', dict)
        else:
            dict = {
                'message': 'Please Complete Your Payment To Enter In The Competition',
                'p_id': p_id,
                'entries': entry
            }
            return render(request, 'vitaral_nutrition_app/registration.html', dict)
    except ObjectDoesNotExist:
        return render(request, 'vitaral_nutrition_app/registration.html')


def user_form(request):
    return render(request, 'vitaral_nutrition_app/user_form.html')


import re
def user_login(request):
    if request.method == 'POST':
        id_username = request.POST['id_username1']
        id_password = request.POST['id_password1']

        # print(id_username, id_password)

        # reCaptcha Code Starts
        # recaptcha_response = request.POST['g-recaptcha-response']

        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # payload = {
        #     'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.parse.urlencode(payload).encode()
        # req = urllib.request.Request(url, data=data)
        # response = urllib.request.urlopen(req)
        # result = json.loads(response.read().decode())

        # if (not result['success']) or (not result['action'] == 'signup'):
        #     e = 'Invalid reCAPTCHA. Please try again.'
        #     return render(request, 'vitaral_nutrition_app/user_form.html', {'e': e})
        # reCaptcha Code Ends

        i = 0
        if '@' in id_username:
            u = User.objects.get(email=id_username)
            user = authenticate(request, username=u.username, email=id_username, password=id_password)
            login(request, user)
            return redirect('index')
        elif i==0:
            user = authenticate(request, username=id_username, password=id_password)
            login(request, user)
            return redirect('index')
        else:
            e = "Some Unkown Error Has Occured"
            return render(request, 'vitaral_nutrition_app/user_form.html', {'e': e})
    else:
        return render(request, 'vitaral_nutrition_app/user_form.html')



def logout_view(request):
    logout(request)
    return redirect('index')
