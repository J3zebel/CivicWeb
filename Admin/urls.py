from django.urls import path
from Admin import views
app_name="Admin"

urlpatterns = [
    path('Sum/',views.sum,name="sum"),
    path('Largest/',views.largest,name="largest"),
    path('Salary/',views.salary,name="salary"),
    path('District/',views.district,name="district"),
    path('Category/',views.category,name="category"),
    path('Admin/',views.admin,name="Admin"),
    path('Homepage/',views.homepage,name="homepage"),
    path('deladmin/<int:id>',views.deladmin,name="deladmin"),
    path('editadmin/<int:id>',views.editadmin,name="editadmin"),
    path('deldistrict/<int:id>',views.deldistrict,name="deldistrict"),
    path('editdistrict/<int:id>',views.editdistrict,name="editdistrict"),
    path('delcategory/<int:id>',views.delcategory,name="delcategory"),
    path('Place/',views.place,name="place"),
    path('editplace/<int:id>',views.editplace,name="editplace"),
    path('delplace/<int:id>',views.delplace,name="delplace"),
    path('SubCategory/',views.subcategory,name="subcategory"),
    path('delsub/<int:id>',views.delsub,name="delsub"),
    path('editsub/<int:id>',views.editsub,name="editsub"),
    path('LocalPlace/',views.localplace,name="localplace"),
    path('dellocal/<int:id>',views.dellocal,name="dellocal"),
    path('Viewkseb/',views.viewkseb,name="viewkseb"),
    path('Viewmuncipality/',views.viewmuncipality,name="viewmunciplity"),
    path('ViewMvd/',views.viewmvd,name="viewmvd"),
    path('ViewPwd/',views.viewpwd,name="viewpwd"),
    path('ViewUser/',views.viewuser,name="viewuser"),
    path('KsebAccept/<str:id>',views.ksebaccept,name="ksebaccept"),
    path('KsebReject/<str:id>',views.ksebreject,name="ksebreject"),
    path('MunAccept/<str:id>',views.munaccept,name="munaccept"),
    path('MunReject/<str:id>',views.munreject,name="munreject"),
    path('MvdAccept/<str:id>',views.mvdaccept,name="mvdaccept"),
    path('MvdReject/<str:id>',views.mvdreject,name="mvdreject"),
    path('PwdAccept/<str:id>',views.pwdaccept,name="pwdaccept"),
    path('PwdReject/<str:id>',views.pwdreject,name="pwdreject"),
    path('UserRemove/<str:id>',views.userremove,name="userremove"),

    path('ksebcomptype/',views.ksebcomptype,name="ksebcomptype"),
    path('delksebcomp/<int:id>',views.delksebcomp,name="delksebcomp"),
    path('mvdcomptype/',views.mvdcomptype,name="mvdcomptype"),
    path('delmvdcomp/<int:id>',views.delmvdcomp,name="delmvdcomp"),
    path('pwdcomptype/',views.pwdcomptype,name="pwdcomptype"),
    path('delpwdcomp/<int:id>',views.delpwdcomp,name="delpwdcomp"),
    path('muncomptype/',views.muncomptype,name="muncomptype"),
    path('delmuncomp/<int:id>',views.delmuncomp,name="delmuncomp"),

    path('ksebreqtype/',views.ksebreqtype,name="ksebreqtype"),
    path('delksebreq/<int:id>',views.delksebreq,name="delksebreq"),
    path('mvdreqtype/',views.mvdreqtype,name="mvdreqtype"),
    path('delmvdreq/<int:id>',views.delmvdreq,name="delmvdreq"),
    path('logout/',views.logout,name="logout"),
    


]