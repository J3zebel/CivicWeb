from django.db import models
from Admin.models import *
import uuid

# Create your models here.


class tbl_muncipality(models.Model):
    mun_id=models.TextField(primary_key=True, editable=False)
    mun_name=models.CharField(max_length=30)
    mun_email=models.CharField(max_length=40)
    mun_contact=models.CharField(max_length=30)
    mun_address=models.CharField(max_length=80)
    mun_proof=models.URLField()
    mun_password=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    mun_status=models.IntegerField(default=0)

class tbl_user(models.Model):
    user_id=models.TextField(primary_key=True, editable=False)
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=40)
    user_contact=models.CharField(max_length=30)
    localplace=models.ForeignKey(tbl_localplace,on_delete=models.CASCADE)
    user_address=models.CharField(max_length=80)
    muncipality=models.ForeignKey(tbl_muncipality,on_delete=models.CASCADE)
    user_photo=models.TextField(null=True)
    user_password=models.CharField(max_length=30)
    user_status=models.IntegerField(default=0,null=True)

class tbl_mvd(models.Model):
    mvd_id=models.TextField(primary_key=True, editable=False)
    mvd_name=models.CharField(max_length=30)
    mvd_email=models.CharField(max_length=40)
    mvd_contact=models.CharField(max_length=30)
    mvd_address=models.CharField(max_length=80)
    mvd_proof=models.URLField()
    mvd_password=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    mvd_status=models.IntegerField(default=0)

class tbl_pwd(models.Model):
    pwd_id=models.TextField(primary_key=True, editable=False)
    pwd_name=models.CharField(max_length=30)
    pwd_email=models.CharField(max_length=40)
    pwd_contact=models.CharField(max_length=30)
    pwd_address=models.CharField(max_length=80)
    pwd_proof=models.URLField()
    pwd_password=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    pwd_status=models.IntegerField(default=0)


class tbl_kseb(models.Model):
    kseb_id=models.TextField(primary_key=True, editable=False)
    kseb_name=models.CharField(max_length=30)
    kseb_email=models.CharField(max_length=40)
    kseb_contact=models.CharField(max_length=30)
    kseb_address=models.CharField(max_length=80)
    localplace=models.ForeignKey(tbl_localplace,on_delete=models.CASCADE)
    kseb_proof=models.URLField()
    kseb_password=models.CharField(max_length=30)
    kseb_status=models.IntegerField(default=0)

