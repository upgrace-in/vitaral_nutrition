"""vitaral_nutrition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from vitaral_nutrition_app import views
from django.views.generic import TemplateView

urlpatterns = [

    path('', views.index, name="index"),
    path('timer/', views.timer, name="timer"),
    path('howitworks/', views.how_it_works, name="how_it_works"),
    path('aboutus/', TemplateView.as_view(template_name='vitaral_nutrition_app/about_us.html'), name="about_us"),
    path('competition_page/', TemplateView.as_view(template_name='vitaral_nutrition_app/questions_page.html'), name="competition_page"),
    path('thank_you/', TemplateView.as_view(template_name='vitaral_nutrition_app/thank_you_page.html'), name="thanku_page"),

    path('initial_form/', views.initial_form, name="initial_form"),
    path('account/', views.my_acc, name="my_account"),
    path('add_my_answer/', views.add_my_answer, name="add_my_answer"),
    path('form/', views.user_form, name="user_form"),
    path('logout/', views.logout_view, name="logout"),
    path('invite_him/', views.email_my_frnd, name="invite_him"),
    path('way_to_competition/', views.way_to_competition, name="register_here"),
    path('competition/', views.participators_details, name="participators_details"),
    path('congrats/', views.competition_completion, name="competition_done"),
    path('competition_payment/', views.payment_data, name="payment_data"),

    path('check_code/', views.check_code, name="check_code"),

    path('login/', views.user_login, name="user_login"),
    # path('register/', views.user_register, name="user_register"),
    path('questions_page/', views.questions_2, name="questions_2"),
    path('change_email/', views.change_email, name="change_email"),
    path('upload_my_picture/', views.upload_my_picture, name="upload_my_pic"),
    path('change_password/', views.change_password, name="change_password"),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
