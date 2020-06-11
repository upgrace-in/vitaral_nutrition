from django.contrib.auth.models import User
from django.db import models
import uuid
# from django.contrib.auth import User


class competitors_info(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    entries = models.IntegerField()
    not_used_entries = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    paid = models.BooleanField(default=0)
    are_you_eating_heathier = models.BooleanField(default=0)
    agree = models.BooleanField(default=0)
    competition_given = models.BooleanField(default=0)

    def __str__(self):
        return self.username


class competitors_payment_info(models.Model):
    i_id = models.ForeignKey(competitors_info, on_delete=models.CASCADE)
    payer_id = models.CharField(max_length=200)
    payer_mail = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    c_time = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=100)
    payer_country_code = models.CharField(max_length=200)

    def __str__(self):
        return self.payer_id


class competition(models.Model):
    i_id = models.ForeignKey(competitors_info, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)


class initial_form_info(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    agree = models.BooleanField(default=0)
    cookware_set = models.CharField(max_length=100)
    other_cook_set = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email


class my_acc_info(models.Model):
    i_id = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(null=True, blank=True)
    bio = models.CharField(max_length=1000, null=True, blank=True)


class timer_info(models.Model):
    timer = models.IntegerField()

class analytic_model(models.Model):
    home_page = models.IntegerField()
    initial_page = models.IntegerField()
    how_it_work_page = models.IntegerField()
    thank_you = models.IntegerField()




