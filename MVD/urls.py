from django.urls import path
from MVD import views
app_name="MVD"

urlpatterns = [
    path('Homepage/',views.homepage,name="homepage"),
    path('My Profile/',views.myprofile,name="myprofile"),
    path('Edit Profile/',views.editprofile,name="editprofile"),
    path('Change Password/',views.changepassword,name="changepassword"),
    path('View Complaint/',views.viewcomplaint,name="viewcomplaint"),
    path('updatests/<int:id>/<int:sts>',views.updatests,name="updatests"),
    path('logout/',views.logout,name="logout"),
    path('publicpost/',views.publicpost,name="publicpost"),
    path('Viewreply/',views.viewreply,name="viewreply"),
    path('requpdate/<int:id>/<int:sts>',views.requpdate,name="requpdate"),
]