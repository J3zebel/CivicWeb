from django.shortcuts import render,redirect
from Guest.models import *
from User.models import *
from MVD.models import *
from django.conf import settings
from django.http import JsonResponse
from supabase import create_client
# Create your views here.



supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Create your views here.
def homepage(request):
    data=tbl_publicpost.objects.all()
    likecount=0
    for i in data:
        likecount = tbl_like.objects.filter(post=i.id).count()
        mycount = tbl_like.objects.filter(post=i.id,user=request.session["uid"]).count()
        if mycount > 0:
            i.condition = 1
        else:
            i.condition = 0
        i.count = likecount
    return render(request, "User/Homepage.html",{'post':data})

def logout(request):
    del request.session["uid"]
    return redirect("Guest:login")

def myprofile(request):
    user=tbl_user.objects.get(user_id=request.session['uid'])
    return render(request, "User/MyProfile.html",{'user':user})


def editprofile(request):
    user=tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        user.user_name=request.POST.get("name")
        user.user_email=request.POST.get("email")
        user.user_contact=request.POST.get("contact")
        user.user_address=request.POST.get("address")
        user.save()
        return redirect('User:myprofile')
    else:
        return render(request, "User/EditProfile.html",{'user':user})

    

# def changepassword(request):
#     user=tbl_user.objects.get(user_id=request.session['uid'])
#     if request.method=="POST":
#         pswd=user.user_password
#         old=request.POST.get("old")
#         new=request.POST.get("new")
#         retype=request.POST.get("retype")
#         if pswd == old:
#             if new == retype:
#                 user.user_password=new
#                 user.save()
#                 return redirect('User:myprofile')
#             else:
#                 return render(request,"User/ChangePassword.html",{'msg':"Password Mismatch"})
#         else:
#             return render(request,"User/ChangePassword.html",{'msg':"Invalid Password"})
#     else:
#         return render(request, "User/ChangePassword.html")
    

def changepassword(request):
    if request.method == "POST":
        try:
            # Get the current authenticated user
            user_response = supabase.auth.get_user()
            print(user_response)
            if "user" not in user_response or user_response["user"] is None:
                return render(request, "User/ChangePassword.html", {"msg": "Authentication required"})

            # Extract user ID
            user_id = user_response["user"]["id"]

            # Verify user in the local database
            user = tbl_user.objects.get(user_id=user_id)

            # Get new password from form
            new_password = request.POST.get("new")
            if not new_password:
                return render(request, "User/ChangePassword.html", {"msg": "New password is required"})

            # Update password using Supabase auth API
            response = supabase.auth.update_user({"password": new_password})
            
            return render(request, "User/ChangePassword.html", {"msg": "Password updated successfully", "response": response})

        except tbl_user.DoesNotExist:
            return render(request, "User/ChangePassword.html", {"msg": "User not found"})

        except Exception as e:
            print(e)
            return render(request, "User/ChangePassword.html", {"msg": e})

    return render(request, "User/ChangePassword.html")

def muncipalitycomplaint(request,id):
    comptype=tbl_muncipalitycomplainttype.objects.all()
    user=tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        title=request.POST.get("txt_title")
        photo=request.FILES.get("txt_photo")
        if photo:
            try:
                
                file_name = f"ComplaintDocs/{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "User/MuncipalityComplaint.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None 
        tbl_complaint.objects.create(
            complaint_content=content,user=user,muncipality=tbl_muncipality.objects.get(mun_id=id),
            complaint_photo=photo_url,muncomplainttype=tbl_muncipalitycomplainttype.objects.get(id=request.POST.get("sel_complaintype")))
        return redirect("User:searchmunicipality")
    else:
        return render(request,"User/MuncipalityComplaint.html",{'user':user,'complainttype':comptype})
    
def mvdcomplaint(request,id):
    comptype=tbl_mvdcomplainttype.objects.all()
    user = tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        title=request.POST.get("txt_title")
        photo=request.FILES.get("txt_photo")
        if photo:
            try:
                
                file_name = f"ComplaintDocs/{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "User/MVDComplaint.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None 
        tbl_complaint.objects.create(
           complaint_content=content,user=user,mvd=tbl_mvd.objects.get(mvd_id=id),
            complaint_photo=photo_url,mvdcomplainttype=tbl_mvdcomplainttype.objects.get(id=request.POST.get("sel_complaintype")))
        return redirect("User:searchmvd")
    else:
        return render(request,"User/MVDComplaint.html",{'user':user,'complainttype':comptype})
    

def pwdcomplaint(request,id):
    comptype=tbl_pwdcomplainttype.objects.all()

    user = tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        title=request.POST.get("txt_title")
        photo=request.FILES.get("txt_photo")
        if photo:
            try:
                
                file_name = f"ComplaintDocs/{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "User/MVDComplaint.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None 
        tbl_complaint.objects.create(
            complaint_content=content,user=user,pwd=tbl_pwd.objects.get(pwd_id=id),
            complaint_photo=photo_url,pwdcomplainttype=tbl_pwdcomplainttype.objects.get(id=request.POST.get("sel_complaintype")))
        return redirect("User:searchpwd")
    else:
        return render(request,"User/PWDComplaint.html",{'user':user,'complainttype':comptype})
    

def ksebcomplaint(request,id):
    comptype=tbl_ksebcomplainttype.objects.all()

    user = tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        title=request.POST.get("txt_title")
        photo=request.FILES.get("txt_photo")
        if photo:
            try:
                
                file_name = f"ComplaintDocs/{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "User/KSEBComplaint.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None 
        tbl_complaint.objects.create(
            complaint_content=content,user=user,kseb=tbl_kseb.objects.get(kseb_id=id),
            complaint_photo=photo_url,ksebcomplainttype=tbl_ksebcomplainttype.objects.get(id=request.POST.get("sel_complaintype")))
        return redirect("User:searchkseb")
    else:
        return render(request,"User/KSEBComplaint.html",{'user':user,'complainttype':comptype})

    
def searchmunicipality(request):
    district = tbl_district.objects.all()
    municipality = tbl_muncipality.objects.all()

    return render(request,"User/SearchMuncipality.html",{'district':district,'data':municipality})

def ajaxsearchmunicipality(request): 
    municipality = tbl_muncipality.objects.filter(district=request.GET.get("district"))
    return render(request,"User/Ajaxsearchmunicipality.html",{'data':municipality})
    
def searchmvd(request):
    district = tbl_district.objects.all()
    mvd = tbl_mvd.objects.all()

    return render(request,"User/SearchMVD.html",{'district':district,'data':mvd})

def ajaxsearchmvd(request): 
    mvd = tbl_mvd.objects.filter(district=request.GET.get("district"))
    return render(request,"User/Ajaxsearchmvd.html",{'data':mvd})

def searchpwd(request):
    district = tbl_district.objects.all()
    pwd = tbl_pwd.objects.all()

    return render(request,"User/SearchPWD.html",{'district':district,'data':pwd})

def ajaxsearchpwd(request): 
    pwd = tbl_pwd.objects.filter(district=request.GET.get("district"))
    return render(request,"User/Ajaxsearchpwd.html",{'data':pwd})

def searchkseb(request):
    district = tbl_district.objects.all()
    kseb = tbl_kseb.objects.all()

    return render(request,"User/SearchKSEB.html",{'district':district,'data':kseb})

def ajaxsearchkseb(request): 
    kseb = tbl_kseb.objects.filter(localplace=request.GET.get("localplace"))
    return render(request,"User/Ajaxsearchkseb.html",{'data':kseb})


def feedback(request):
    user = tbl_user.objects.get(user_id=request.session['uid'])
    feedback=tbl_feedback.objects.all()
    if request.method=="POST":
        content=request.POST.get("txt_content")
        tbl_feedback.objects.create(
            feedback_content=content ,user=user
        )
        return render(request,'User/Feedback.html',{'msg':"Data inserted"})
    else:
        return render(request,'User/Feedback.html',{'feedback':feedback})

def mycomplaints(request):
    kseb = tbl_kseb.objects.all()
    ksebcomplaint=tbl_complaint.objects.filter(user_id=request.session['uid'], kseb__in=kseb)
    muncipality = tbl_muncipality.objects.all()
    muncipalitycomplaint=tbl_complaint.objects.filter(user_id=request.session['uid'], muncipality__in=muncipality)
    mvd = tbl_mvd.objects.all()
    mvdcomplaint=tbl_complaint.objects.filter(user_id=request.session['uid'], mvd__in=mvd)
    pwd = tbl_pwd.objects.all()
    pwdcomplaint=tbl_complaint.objects.filter(user_id=request.session['uid'], pwd__in=pwd)
    return render(request, "User/Mycomplaints.html",{'ksebcomplaint':ksebcomplaint,'muncipalitycomplaint':muncipalitycomplaint,'mvdcomplaint':mvdcomplaint,'pwdcomplaint':pwdcomplaint})

def myrequests(request):
    kseb = tbl_kseb.objects.all()
    ksebrequest=tbl_request.objects.filter(user_id=request.session['uid'], kseb__in=kseb)
    
    mvd = tbl_mvd.objects.all()
    mvdrequest=tbl_request.objects.filter(user_id=request.session['uid'], mvd__in=mvd)
   
    return render(request, "User/Myrequests.html",{'ksebrequest':ksebrequest,'mvdrequest':mvdrequest})


def updates(request):
    update=tbl_updates.objects.all()
    return render(request,'User/Updates.html',{'update':update})

def publiccomplaint(request):
    complaint=tbl_complaint.objects.all()
    likecount=0
    for i in complaint:
        likecount = tbl_like.objects.filter(complaint=i.id).count()
        mycount = tbl_like.objects.filter(complaint=i.id,user=request.session["uid"]).count()
        if mycount > 0:
            i.condition = 1
        else:
            i.condition = 0
        i.count = likecount
    return render(request,'User/PublicComplaints.html',{'complaint':complaint})


def ajaxlike(request):
    likecount = tbl_like.objects.filter(user=request.session["uid"],complaint=request.GET.get("comid")).count()
    if likecount > 0:
        tbl_like.objects.get(user_id=request.session["uid"],complaint=request.GET.get("comid")).delete()
        count = tbl_like.objects.filter(user=request.session["uid"],complaint=request.GET.get("comid")).count()
        return JsonResponse({"color":1,"count":count})
    else:
        tbl_like.objects.create(user=tbl_user.objects.get(user_id=request.session["uid"]),complaint=tbl_complaint.objects.get(id=request.GET.get("comid")))
        count = tbl_like.objects.filter(user=request.session["uid"],complaint=request.GET.get("comid")).count()
        return JsonResponse({"color":0,"count":count})
    

    
def muncipalityrequest(request,id):
    user=tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        title=request.POST.get("txt_title")
        tbl_request.objects.create(
            request_title=title,request_content=content,user=user,muncipality=tbl_muncipality.objects.get(mun_id=id),
            )
        return render(request,'User/MuncipalityRequest.html',{'msg':"Data inserted"})
    else:
        return render(request,"User/MuncipalityRequest.html",{'user':user},)
    
def mvdrequest(request,id):
    user=tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        title=request.POST.get("txt_title")
        tbl_request.objects.create(
            request_title=title,request_content=content,user=user,mvd=tbl_mvd.objects.get(mvd_id=id),
            )
        return render(request,'User/MvdRequest.html',{'msg':"Data inserted"})
    else:
        return render(request,"User/MvdRequest.html",{'user':user},)
    


def ksebrequest(request,id):
    reqtype=tbl_ksebrequesttype.objects.all()

    user = tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        photo=request.FILES.get("txt_photo")
        if photo:
            try:
                
                file_name = f"RequestDocs/{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "User/KsebRequest.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None 
        tbl_request.objects.create(
            request_content=content,user=user,kseb=tbl_kseb.objects.get(kseb_id=id),
            request_photo=photo_url,ksebrequesttype=tbl_ksebrequesttype.objects.get(id=request.POST.get("sel_requesttype")))
        return redirect("User:searchkseb")
    else:
        return render(request,"User/KsebRequest.html",{'user':user,'requesttype':reqtype})
    





def publicpost(request):
    data=tbl_publicpost.objects.all()
    likecount=0
    for i in data:
        likecount = tbl_like.objects.filter(post=i.id).count()
        mycount = tbl_like.objects.filter(post=i.id,user=request.session["uid"]).count()
        if mycount > 0:
            i.condition = 1
        else:
            i.condition = 0
        i.count = likecount
    return render(request,"User/PublicPost.html",{'post':data})


def mvdrequest(request,id):
    reqtype=tbl_mvdrequesttype.objects.all()

    user = tbl_user.objects.get(user_id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get("txt_content")
        photo=request.FILES.get("txt_photo")
        if photo:
            try:
                
                file_name = f"RequestDocs/{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "User/MvdRequest.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None 
        tbl_request.objects.create(
            request_content=content,user=user,mvd=tbl_mvd.objects.get(mvd_id=id),
            request_photo=photo_url,mvdrequesttype=tbl_mvdrequesttype.objects.get(id=request.POST.get("sel_requesttype")))
        return redirect("User:searchmvd")
    else:
        return render(request,"User/MvdRequest.html",{'user':user,'requesttype':reqtype})
    



def publicpost(request):
    data=tbl_publicpost.objects.all()
    likecount=0
    for i in data:
        likecount = tbl_like.objects.filter(post=i.id).count()
        mycount = tbl_like.objects.filter(post=i.id,user=request.session["uid"]).count()
        if mycount > 0:
            i.condition = 1
        else:
            i.condition = 0
        i.count = likecount
    return render(request,"User/PublicPost.html",{'post':data})


def ajaxlikepost(request):
    likecount = tbl_like.objects.filter(user=request.session["uid"],post=request.GET.get("comid")).count()
    if likecount > 0:
        tbl_like.objects.get(user_id=request.session["uid"],post=request.GET.get("comid")).delete()
        count = tbl_like.objects.filter(user=request.session["uid"],post=request.GET.get("comid")).count()
        return JsonResponse({"color":1,"count":count})
    else:
        tbl_like.objects.create(user=tbl_user.objects.get(user_id=request.session["uid"]),post=tbl_publicpost.objects.get(id=request.GET.get("comid")))
        count = tbl_like.objects.filter(user=request.session["uid"],post=request.GET.get("comid")).count()
        return JsonResponse({"color":0,"count":count})
    