from django.contrib import admin

from .models import competitors_info, competitors_payment_info, competition, initial_form_info, my_acc_info, timer_info, analytic_model

# Register your models here.
admin.site.register(initial_form_info)
admin.site.register(my_acc_info)
admin.site.register(timer_info)
admin.site.register(analytic_model)


class competition_payment_admin(admin.TabularInline):
    model = competitors_payment_info


class competition_questions_admin(admin.TabularInline):
    model = competition


@admin.register(competitors_info)
class competition_admin(admin.ModelAdmin):
    inlines = [
        competition_payment_admin,
        competition_questions_admin
    ]
