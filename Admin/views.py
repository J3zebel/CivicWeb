from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
from django.conf import settings
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
# Create your views here.
def sum(request):
    if request.method=="POST":
        Num1=int(request.POST.get('number 1'))
        Num2=int(request.POST.get('number 2'))
        btn=request.POST.get('btn')
        if btn=="+":
            Result= Num1 + Num2
        elif btn=="-":
            Result=Num1 - Num2
        elif btn=="*":
            Result=Num1 * Num2
        elif btn=="/":
            Result=Num1 / Num2
        elif btn=="%":
            Result=Num1 % Num2
        return render(request,'Admin/Sum.html',{'result':Result})
    else:
        return render(request,'Admin/Sum.html')
    
def largest(request):
        if request.method=="POST":
            Num1=int(request.POST.get('number1'))
            Num2=int(request.POST.get('number2'))
            Num3=int(request.POST.get('number3'))
            if Num1>Num2 and Num1>Num3:
                largest=Num1
            elif Num2>Num1 and Num2>Num3:
                largest=Num2
            elif Num3>Num1 and Num3>Num2:
                largest=Num3

            if Num1<Num2 and Num1<Num3:
                smallest=Num1
            elif Num2<Num1 and Num2<Num3:
                smallest=Num2
            elif Num3<Num1 and Num3<Num2:
                smallest=Num3
            return render(request,'Admin/Largest.html',{'result':largest,'smallest':smallest})
        else:
            return render(request,'Admin/Largest.html')

def salary(request):
    
    if request.method=="POST":
        Fname=(request.POST.get('f_name'))
        Lname=(request.POST.get('l_name'))
        Gender=(request.POST.get('Gender'))
        martial=(request.POST.get('martial'))   
        Dept=(request.POST.get('sel_dept'))
        Salary=int(request.POST.get('b_sal'))
        fullname= Fname + Lname
        if Gender=="male":
            name='Mr.'+fullname
            
        elif Gender=="female" and martial=="single":
            name='Miss.'+fullname
        elif Gender=="female" and martial=="married":
            name='Mrs.'+fullname
        if(Salary>=10000):
            ta=0.40*Salary
            da=0.35*Salary
            hra=0.30*Salary
            lic=0.25*Salary
            pf=0.20*Salary
        elif(Salary>=5000 and Salary<10000):
            ta=0.35*Salary
            da=0.30*Salary
            hra=0.25*Salary
            lic=0.20*Salary
            pf=0.15*Salary
        elif(Salary<5000):
            ta=0.3*Salary
            da=0.25*Salary
            hra=0.2*Salary
            lic=0.15*Salary
            pf=0.10*Salary
        Deduction=lic+pf
        net=Salary+ta+da+hra-(Deduction)
        return render(request,'Admin/Salary.html',{'name':name,'gender':Gender,'martial':martial,'dept':Dept,'salary':Salary,'ta':ta,'da':da,'hra':hra,'lic':lic,'pf':pf,'deduction':Deduction,'net':net})
    else:
         return render(request,'Admin/Salary.html')
    

def district(request):
    dis=tbl_district.objects.all()
    if request.method=="POST":
        district=request.POST.get("district")
        tbl_district.objects.create(
            district_name=district
        )
        return render(request,'Admin/District.html',{'msg':"Data Inserted Successfully",'district':dis})
    else:
        return render(request,'Admin/District.html',{'district':dis})

def category(request):
    cat=tbl_category.objects.all()
    if request.method=="POST":
        category=request.POST.get("category")
        tbl_category.objects.create(
            category_name=category
        )
        return render(request,'Admin/category.html',{'msg':"Data Inserted",'cat':cat})
    else:
        return render(request,'Admin/category.html',{'cat':cat})
    
# def admin(request):
#     sel=tbl_admin.objects.all()
#     if request.method=="POST":
#         name=request.POST.get("name")
#         email=request.POST.get("email")
#         pswd=request.POST.get("pswd")
#         tbl_admin.objects.create(
#             admin_name=name,admin_email=email,admin_pswd=pswd
#         )
#         msg="Data Inserted"
#         return render(request,'Admin/Admin.html',{'msg':msg,'admin':sel})
#     else:
#         return render(request,'Admin/Admin.html',{'admin':sel})

def admin(request):
    sel=tbl_admin.objects.all()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name=request.POST.get("name")

        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
           
            
            if auth_response.user:
                user_data = auth_response.user  
                user_id = user_data.id
                
                tbl_admin.objects.create(admin_id=user_id,admin_name=name,admin_email=email,admin_password=password)
                
                return redirect('Admin:admin')
            else:
                return render(request, "Admin/Admin.html", { "error": "Sign-up failed."})

        except Exception as e:
            print(e)
            return render(request, "Admin/Admin.html", {"Admin":sel ,"error": "An error occurred during sign-up."})
    else:
        return render(request, "Admin/Admin.html", {'Admin':sel})
    

def deladmin(request,id):
    tbl_admin.objects.get(id=id).delete()
    return redirect("Admin:admin")

def editadmin(request,id):
    edadm=tbl_admin.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        pswd=request.POST.get("pswd")
        edadm.admin_name=name
        edadm.admin_email=email
        edadm.admin_pswd=pswd
        edadm.save()
        return redirect("Admin:Admin")
    else:
        return render(request,"Admin/Admin.html",{'edit':edadm})

    

def deldistrict(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Admin:district")

def editdistrict(request,id):
    ed=tbl_district.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get("district")
        ed.district_name=name
        ed.save()
        return redirect("Admin:district")
    else:
        return render(request,"Admin/District.html",{'edit':ed})


def delcategory(request,id):
    tbl_category.objects.get(id=id).delete()
    return redirect("Admin:category")
    
def place(request):
    dis=tbl_district.objects.all()
    plc=tbl_place.objects.all()
    if request.method=="POST":
        district=tbl_district.objects.get(id=request.POST.get("district"))
        plc=request.POST.get("place")
        tbl_place.objects.create(district=district, place_name=plc )
        msg="Data Inserted"
        return render(request,'Admin/Place.html',{'msg':msg})
    else:
        return render(request,'Admin/Place.html',{'place':plc,'district':dis})
    
def editplace(request,id):
    dis=tbl_district.objects.all()
    ed=tbl_place.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get("place")
        ed.place_name=name
        ed.district=tbl_district.objects.get(id=request.POST.get("district"))
        ed.save()
        return redirect("Admin:place")
    else:
        return render(request,"Admin/Place.html",{'edit':ed,'district':dis})

def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:place")


def subcategory(request):
    sub=tbl_subcategory.objects.all()
    category=tbl_category.objects.all()
    if request.method=="POST":
        cat=tbl_category.objects.get(id=request.POST.get("category"))
        subcat=request.POST.get("subcategory")
        tbl_subcategory.objects.create(category=cat,sub_name=subcat)
        return render(request,'Admin/Subcategory.html',{'msg':"Data Inserted"})
    else:
        return render(request,'Admin/Subcategory.html',{'subcategory':sub,'category':category})
    
def delsub(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:subcategory")

def editsub(request,id):
    category=tbl_category.objects.all()
    subcategory=tbl_subcategory.objects.get(id=id)
    if request.method=="POST":
        cat=request.POST.get("category")
        subcat=request.POST.get("subcategory")
        category.category_name=cat
        category.sub_category_name=subcat 
        category.save()
        return redirect("Admin:editsub")
    else:
        return render(request,"Admin/Subcategory.html",{'cat':category,'edit':subcategory})
    
def localplace(request):
    dis=tbl_district.objects.all()
    loc=tbl_localplace.objects.all()
    if request.method=="POST":
        plc=tbl_place.objects.get(id=request.POST.get("place"))
        local=request.POST.get("local")
        tbl_localplace.objects.create(place=plc,local_place=local)
        msg="Data Inserted"
        return render(request,'Admin/Localplace.html',{'msg':msg})
    else:
        return render(request,'Admin/Localplace.html',{'local':loc,'district':dis})

def dellocal(request,id):
    tbl_localplace.objects.get(id=id).delete()
    return redirect("Admin:localplace")
    

def viewkseb(request):
    kseb=tbl_kseb.objects.all()
    return render(request, "Admin/ViewKseb.html",{'kseb':kseb})

def viewmuncipality(request):
    muncipality=tbl_muncipality.objects.all()
    return render(request, "Admin/ViewMuncipality.html",{'muncipality':muncipality})

def viewmvd(request):
    mvd=tbl_mvd.objects.all()
    return render(request, "Admin/ViewMvd.html",{'mvd':mvd})

def viewpwd(request):
    pwd=tbl_pwd.objects.all()
    return render(request, "Admin/ViewPwd.html",{'pwd':pwd})

def viewuser(request):
    user=tbl_user.objects.all()
    return render(request, "Admin/ViewUser.html",{'user':user})

def ksebaccept(request,id):
    kseb=tbl_kseb.objects.get(kseb_id=id)
    kseb.kseb_status="1"
    kseb.save()
    return redirect("Admin:viewkseb")
def ksebreject(request,id):
    kseb=tbl_kseb.objects.get(kseb_id=id)
    kseb.kseb_status="2"
    kseb.save()
    return redirect("Admin:viewkseb")

def munaccept(request,id):
    muncipality=tbl_muncipality.objects.get(mun_id=id)
    muncipality.mun_status="1"
    muncipality.save()
    return redirect("Admin:viewmunciplity")
def munreject(request,id):
    muncipality=tbl_muncipality.objects.get(mun_id=id)
    muncipality.mun_status="2"
    muncipality.save()
    return redirect("Admin:viewmunciplity")

def mvdaccept(request,id):
    mvd=tbl_mvd.objects.get(mvd_id=id)
    mvd.mvd_status="1"
    mvd.save()
    return redirect("Admin:viewmvd")
def mvdreject(request,id):
    mvd=tbl_mvd.objects.get(mvd_id=id)
    mvd.mvd_status="2"
    mvd.save()
    return redirect("Admin:viewmvd")

def pwdaccept(request,id):
    pwd=tbl_pwd.objects.get(pwd_id=id)
    pwd.pwd_status="1"
    pwd.save()
    return redirect("Admin:viewpwd")
def pwdreject(request,id):
    pwd=tbl_pwd.objects.get(pwd_id=id)
    pwd.pwd_status="2"
    pwd.save()
    return redirect("Admin:viewpwd")

def userremove(request,id):
    user=tbl_user.objects.get(user_id=id)
    user.user_status="1"
    user.save()
    return redirect("Admin:viewuser")


def homepage(request):
    # Counts for dashboard
    admin=tbl_admin.objects.all()
    usercount = tbl_user.objects.all().count()
    solvedcomplaint = tbl_complaint.objects.filter(complaint_status=5).count()
    pendingcomplaint = tbl_complaint.objects.filter(complaint_status=0).count()
    recent_complaints = tbl_complaint.objects.all().order_by('-complaint_date')[:5]


    context = {
        'admin':request.session['aname'],
        'user': usercount,
        'solvedcomplaint': solvedcomplaint,
        'pendingcomplaint': pendingcomplaint,
        'recent_complaints': recent_complaints,
    }
    return render(request, "Admin/Homepage.html", context)

def ksebcomptype(request):
    dis=tbl_ksebcomplainttype.objects.all()
    if request.method=="POST":
        typ=request.POST.get("txt_complaint")
        tbl_ksebcomplainttype.objects.create(
            complaint_type=typ
        )
        return render(request,'Admin/KsebComplaintType.html',{'msg':"Data Inserted Successfully",'complaint':dis})
    else:
        return render(request,'Admin/KsebComplaintType.html',{'complaint':dis})
    
def delksebcomp(request,id):
    tbl_ksebcomplainttype.objects.get(id=id).delete()
    return redirect("Admin:ksebcomptype")


def mvdcomptype(request):
    dis=tbl_mvdcomplainttype.objects.all()
    if request.method=="POST":
        typ=request.POST.get("txt_complaint")
        tbl_mvdcomplainttype.objects.create(
            complaint_type=typ
        )
        return render(request,'Admin/MVDComplaintType.html',{'msg':"Data Inserted Successfully",'complaint':dis})
    else:
        return render(request,'Admin/MVDComplaintType.html',{'complaint':dis})
    
def delmvdcomp(request,id):
    tbl_mvdcomplainttype.objects.get(id=id).delete()
    return redirect("Admin:mvdcomptype")


def pwdcomptype(request):
    dis=tbl_pwdcomplainttype.objects.all()
    if request.method=="POST":
        typ=request.POST.get("txt_complaint")
        tbl_pwdcomplainttype.objects.create(
            complaint_type=typ
        )
        return render(request,'Admin/PWDComplaintType.html',{'msg':"Data Inserted Successfully",'complaint':dis})
    else:
        return render(request,'Admin/PWDComplaintType.html',{'complaint':dis})
    
def delpwdcomp(request,id):
    tbl_pwdcomplainttype.objects.get(id=id).delete()
    return redirect("Admin:pwdcomptype")


def muncomptype(request):
    dis=tbl_muncipalitycomplainttype.objects.all()
    if request.method=="POST":
        typ=request.POST.get("txt_complaint")
        tbl_muncipalitycomplainttype.objects.create(
            complaint_type=typ
        )
        return render(request,'Admin/MuncipalityComplaintType.html',{'msg':"Data Inserted Successfully",'complaint':dis})
    else:
        return render(request,'Admin/MuncipalityComplaintType.html',{'complaint':dis})
    
def delmuncomp(request,id):
    tbl_muncipalitycomplainttype.objects.get(id=id).delete()
    return redirect("Admin:muncomptype")



def ksebreqtype(request):
    dis=tbl_ksebrequesttype.objects.all()
    if request.method=="POST":
        typ=request.POST.get("txt_request")
        tbl_ksebrequesttype.objects.create(
            request_type=typ
        )
        return render(request,'Admin/KsebRequestType.html',{'msg':"Data Inserted Successfully",'request':dis})
    else:
        return render(request,'Admin/KsebRequestType.html',{'request':dis})
    
def delksebreq(request,id):
    tbl_ksebrequesttype.objects.get(id=id).delete()
    return redirect("Admin:ksebreqtype")


def mvdreqtype(request):
    dis=tbl_mvdrequesttype.objects.all()
    if request.method=="POST":
        typ=request.POST.get("txt_request")
        tbl_mvdrequesttype.objects.create(
            request_type=typ
        )
        return render(request,'Admin/MVDRequestType.html',{'msg':"Data Inserted Successfully",'request':dis})
    else:
        return render(request,'Admin/MVDRequestType.html',{'request':dis})
    
def delmvdreq(request,id):
    tbl_mvdrequesttype.objects.get(id=id).delete()
    return redirect("Admin:mvdreqtype")



def logout(request):
    del request.session['aid']
    return redirect("Guest:login")