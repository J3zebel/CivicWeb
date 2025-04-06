from django.urls import path
from KSEB import views
app_name="KSEB"

urlpatterns = [
    path('Homepage/',views.homepage,name="homepage"),
    path('MyProfile/',views.myprofile,name="myprofile"),
    path('Editprofile/',views.editprofile,name="editprofile"),
    path('Changepassword/',views.changepassword,name="changepassword"),
    path('Viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
    path('updatests/<int:id>/<int:sts>',views.updatests,name="updatests"),
    path('requpdate/<int:id>/<int:sts>',views.requpdate,name="requpdate"),
    path('viewreply/',views.viewreply,name="viewreply"),
    path('logout/',views.logout,name="logout"),
    path('publicpost/',views.publicpost,name="publicpost"),


]