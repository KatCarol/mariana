# Generated by Django 4.2.2 on 2023-06-29 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_phone_1_user_phone_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('clinician', 'clinician'), ('sales_attendant', 'sales_attendant'), ('admin', 'admin')], default='none', max_length=20),
            preserve_default=False,
        ),
    ]