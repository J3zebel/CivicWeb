from django.urls import path
from Guest import views
app_name="Guest"

urlpatterns = [
    path('',views.index,name="index"),

    path('User Reg/',views.user,name="user"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
    path('Login/',views.login,name="login"),
    path('Muncipality/',views.muncipality,name="muncipality"),
    path('MVD/',views.mvd,name="mvd"),
    path('PWD/',views.pwd,name="pwd"),
    path('KSEB/',views.kseb,name="kseb"),
    path('ajaxlocal/',views.ajaxlocal,name="ajaxlocal"),
    path('ajaxmuncipality/',views.ajaxmuncipality,name="ajaxmuncipality")
]