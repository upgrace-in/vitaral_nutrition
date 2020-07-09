# Generated by Django 3.0.6 on 2020-06-30 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitaral_nutrition_app', '0002_discount_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timer_info',
            old_name='timer',
            new_name='days',
        ),
        migrations.AddField(
            model_name='timer_info',
            name='month_name',
            field=models.CharField(default='Jan', max_length=100),
            preserve_default=False,
        ),
    ]
