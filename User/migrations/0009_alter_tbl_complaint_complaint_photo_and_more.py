# Generated by Django 5.1.6 on 2025-04-06 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_tbl_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_complaint',
            name='complaint_photo',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='tbl_request',
            name='request_photo',
            field=models.TextField(null=True),
        ),
    ]
