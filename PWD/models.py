from django.db import models
from Guest.models  import *

# Create your models here.


class tbl_public(models.Model):
    post_details=models.CharField(max_length=100)
    post_file=models.URLField()
    post_date=models.DateField(auto_now_add=True)
    mvd=models.ForeignKey(tbl_mvd,on_delete=models.CASCADE)
    pwd=models.ForeignKey(tbl_pwd,on_delete=models.CASCADE)
    muncipality=models.ForeignKey(tbl_muncipality,on_delete=models.CASCADE)
    kseb=models.ForeignKey(tbl_kseb,on_delete=models.CASCADE)



