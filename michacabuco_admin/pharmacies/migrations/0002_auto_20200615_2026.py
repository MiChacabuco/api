# Generated by Django 2.2.12 on 2020-06-15 23:26

from django.db import migrations, models
import django.db.models.deletion
import michacabuco_admin.pharmacies.models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0001_initial'),
        ('businesses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacyshift',
            name='pharmacy',
            field=models.ForeignKey(limit_choices_to={'tags__value': 'farmacias'}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='businesses.Business', verbose_name='farmacia'),
        ),
        migrations.CreateModel(
            name='PharmacyShiftLegacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=michacabuco_admin.pharmacies.models.get_default_shift_start, verbose_name='inicio')),
                ('end', models.DateTimeField(verbose_name='fin')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='pharmacies.Pharmacy', verbose_name='farmacia')),
            ],
            options={
                'verbose_name': 'turno de farmacia',
                'verbose_name_plural': 'turnos de farmacias',
                'ordering': ['start'],
                'abstract': False,
            },
        ),
    ]
