# Generated by Django 4.2.1 on 2023-06-27 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_patient_diagnostic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
            ],
        ),
    ]
