# Generated by Django 2.2.27 on 2022-07-09 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sd_app', '0006_alter_transaction_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='delivery_date',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
