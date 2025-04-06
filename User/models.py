from django.db import models
from Admin.models import *
from Guest.models import *
from KSEB.models import *

# Create your models here.
class tbl_complaint(models.Model):
    complaint_content=models.CharField(max_length=200)
    complaint_photo=models.TextField(null=True)
    complaint_response=models.CharField(max_length=200,null=True)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    kseb=models.ForeignKey(tbl_kseb,on_delete=models.CASCADE,null=True)
    mvd=models.ForeignKey(tbl_mvd,on_delete=models.CASCADE,null=True)
    pwd=models.ForeignKey(tbl_pwd,on_delete=models.CASCADE,null=True)
    muncipality=models.ForeignKey(tbl_muncipality,on_delete=models.CASCADE,null=True)
    complaint_status=models.IntegerField(default=0,null=True)
    complaint_date=models.DateField(auto_now_add=True)
    ksebcomplainttype=models.ForeignKey(tbl_ksebcomplainttype,on_delete=models.CASCADE,null=True)
    mvdcomplainttype=models.ForeignKey(tbl_mvdcomplainttype,on_delete=models.CASCADE,null=True)
    pwdcomplainttype=models.ForeignKey(tbl_pwdcomplainttype,on_delete=models.CASCADE,null=True)
    muncomplainttype=models.ForeignKey(tbl_muncipalitycomplainttype,on_delete=models.CASCADE,null=True)



class tbl_feedback(models.Model):
    feedback_content=models.CharField(max_length=200)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    feedback_date=models.DateField(auto_now_add=True)

class tbl_like(models.Model):
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    complaint=models.ForeignKey(tbl_complaint,on_delete=models.CASCADE,null=True)
    post=models.ForeignKey(tbl_publicpost,on_delete=models.CASCADE,null=True)

class tbl_request(models.Model):
    request_content=models.CharField(max_length=200)
    request_response=models.CharField(max_length=200,null=True)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    muncipality=models.ForeignKey(tbl_muncipality,on_delete=models.CASCADE,null=True)
    kseb=models.ForeignKey(tbl_kseb,on_delete=models.CASCADE,null=True)
    mvd=models.ForeignKey(tbl_mvd,on_delete=models.CASCADE,null=True)
    request_status=models.IntegerField(default=0,null=True)
    request_date=models.DateField(auto_now_add=True)
    ksebrequesttype=models.ForeignKey(tbl_ksebrequesttype,on_delete=models.CASCADE,null=True)
    mvdrequesttype=models.ForeignKey(tbl_mvdrequesttype,on_delete=models.CASCADE,null=True)
    request_photo=models.TextField(null=True)