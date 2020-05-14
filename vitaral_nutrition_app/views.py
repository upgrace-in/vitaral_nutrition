import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from vitaral_nutrition_app.models import competitors_info, competitors_payment_info, competition, initial_form_info, my_acc_info, timer_info
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

i = [0]
i_i = [0]
already = []
q = []
correct_ans = []
correct_answers = ['Food! Health Edification', 'Obesity, Diabetes, Heart Disease', 'Cookware',
                           'Carrot', '93%', '4,500', '86 degree', '316Ti Surgical Steel and Titanium', 'Orange',
                           'Executive Chef Set', 'Vitaral Nutrition', 'Not a single drop of oil', 'Not a single drop of water', '5', 'https://blog.vitaral.co.uk']
questions = ["1.  Vitaral Nutrition is based in London and facilitates what presentation in the home?",
             "2.  By removing grease, fats and oil from our diet helps prevent",
             "3.  What is the last and most important step in the cooking process?",
             "4.  Which of these is naturally sweet, healthy and can eat on the go.",
             "5.  Using the Master Set cookware, what is the average nutritional retention without water ?",
             "6. What is the minimum sold ticket entries required for the Executive Chef Set to be won ?",
             "7.  What is the maximum cooking temperature before the Vapo value alerts ?",
             "8.  What material is the cookware made from ?",
             "9.   What is the colour of a vegetable and the name of a fruit ?",
             "10.   What is the name of the top price in this competition ?",
             "11.  What is the name of the team who provides guidance in your healthy eating quest?",
             "12.   How much Grease, Fat or Oil do you need when cooking with the Executive Chef Set ?",
             "13.   How much water do you need when cooking vegetable in the Executive Chef Set ?",
             "14.  How many layers are there that make up the 316Ti Cookware",
             "15.   Where can you find more information on healthy Foods"]


def timer(request):
    timer = timer_info.objects.all().first()
    return HttpResponse(timer.timer)


@login_required(function=None, login_url='user_form')
def questions_2(request):
    if request.method == 'POST':
        user = request.user.username
        model = competition
        m = competitors_info.objects.get(username=user)
        q_nos = request.POST['question_nos']
        ans = request.POST['answer']
        if already.count(1) != 1:
            already.append(1)
            del questions[0:(15-int(q_nos))]
            q.append(questions)
            del correct_answers[0:(15 - int(q_nos))]
            correct_ans.append(correct_answers)
            print("im")
        else:
            pass
        index = i_i[-1]
        model.objects.create(i_id=m, question=q[0][index], answer=ans, correct_answer=correct_ans[0][index])
        h = index + 1
        i_i.append(h)
        return HttpResponse("Added")
    else:
        return HttpResponse("Try Again Later...")


def email_my_frnd(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']

        name = name + ' ' + surname

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Vitaral Nutrition Invitation"
        html = """
            <html>
              <head></head>
              <body>
                <h1>Hi %s</h1>
                <p>I have just entered this raffle competition and thought this would be great opportunity for you since you are a great cook, health conscious and love a beautiful kitchen.</p>
                <img class='text-center mx-auto' src='https://vitaral.co.uk/images/email_logo.jpg' style='width: 300px;'><br>
                <button href="http://www.competition.vitaral.co.uk/" class="btn btn-primary">Click Here</button>
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
        ans = request.POST['answer']
        index = i[-1]
        model.objects.create(i_id=m, question=questions[index], answer=ans, correct_answer=correct_answers[index])
        index_of_f = index + 1
        i.append(index_of_f)
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


@login_required(function=None, login_url='user_form')
def participators_details(request):
    if request.method == 'POST':
        user = request.user.username
        username = user
        firstname = request.POST['fname']
        surname = request.POST['surname']
        email = request.POST['mail_id']
        entries = request.POST['entries']
        region = request.POST['region']
        eating_healthier = request.POST['eating_healthier']
        agree = request.POST['agree']

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


@login_required(function=None, login_url='user_form')
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
    if request.method == 'POST':
        id_username = request.POST['id_username']
        id_password = request.POST['id_password']
        try:
            user = authenticate(request, username=id_username, password=id_password)
            u_name = User.objects.get(username=id_username)
            if user is not None:
                login(request, user=user)
                print("Logged IN ")
                return redirect('index')
            elif u_name:
                e = "Wrong Credentials, Try Again !!!"
                return render(request, 'vitaral_nutrition_app/user_form.html', {'e': e})

        except (EOFError, ObjectDoesNotExist):
            user = User.objects.create_user(username=id_username, password=id_password)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        return render(request, 'vitaral_nutrition_app/user_form.html')


def logout_view(request):
    logout(request)
    return redirect('index')
