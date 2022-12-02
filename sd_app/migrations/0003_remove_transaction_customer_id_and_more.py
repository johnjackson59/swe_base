# Generated by Django 4.0.5 on 2022-06-28 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sd_app', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='delivery_date',
            field=models.CharField(default='Never', max_length=100),
        ),
        migrations.AddField(
            model_name='transaction',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.CharField(default='Today', max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]