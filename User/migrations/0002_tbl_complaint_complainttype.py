# Generated by Django 5.1.6 on 2025-02-15 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0003_rename_tbl_ksbecomplainttype_tbl_ksebcomplainttype'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_complaint',
            name='complainttype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_muncipalitycomplainttype'),
        ),
    ]
