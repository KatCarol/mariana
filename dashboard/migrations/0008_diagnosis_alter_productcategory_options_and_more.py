# Generated by Django 4.2.1 on 2023-06-28 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_rename_productcategories_productcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=50)),
                ('details', models.TextField(blank=True, null=True)),
                ('prescription', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.patient')),
            ],
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name_plural': 'Product categories'},
        ),
        migrations.AddField(
            model_name='batch',
            name='quantity_stocked',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Diagnostic',
        ),
    ]
