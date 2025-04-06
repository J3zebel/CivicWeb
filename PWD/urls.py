from django.urls import path
from PWD import views
app_name="PWD"

urlpatterns = [
    path('Homepage/',views.homepage,name="homepage"),
    path('My Profile/',views.myprofile,name="myprofile"),
    path('Edit Profile/',views.editprofile,name="editprofile"),
    path('Change Password/',views.changepassword,name="changepassword"),
    path('View Complaint/',views.viewcomplaint,name="viewcomplaint"),
    path('Reply/<int:id>',views.reply,name="reply"),
     path('updatests/<int:id>/<int:sts>',views.updatests,name="updatests"),
    path('logout/',views.logout,name="logout"),
    path('publicpost/',views.publicpost,name="publicpost"),
    path('Viewreply/',views.viewreply,name="viewreply"),
]

    