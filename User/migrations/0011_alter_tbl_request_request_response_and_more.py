# Generated by Django 5.1.6 on 2025-04-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_alter_tbl_complaint_complaint_response_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_request',
            name='request_response',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tbl_request',
            name='request_status',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
