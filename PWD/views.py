from django.shortcuts import render,redirect
from Guest.models import *
from User.models import *
from MVD.models import *
from django.db.models import Count
from django.conf import settings
from supabase import create_client
# Create your views here.
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Create your views here.
def homepage(request):
    return render(request, "PWD/Homepage.html")

def myprofile(request):
    pwd=tbl_pwd.objects.get(pwd_id=request.session['pid'])
    return render(request, "PWD/MyProfile.html",{'pwd':pwd})


def editprofile(request):
    pwd=tbl_pwd.objects.get(pwd_id=request.session['pid'])
    if request.method=="POST":
        pwd.pwd_name=request.POST.get("txt_name")
        pwd.pwd_email=request.POST.get("txt_email")
        pwd.pwd_contact=request.POST.get("txt_contact")
        pwd.pwd_address=request.POST.get("txt_address")
        pwd.save()
        return redirect('PWD:myprofile')
    else:
        return render(request, "PWD/EditProfile.html",{'pwd':pwd})

    

def changepassword(request):
    pwd=tbl_pwd.objects.get(pwd_id=request.session['pid'])
    if request.method=="POST":
        pswd=pwd.pwd_password
        old=request.POST.get("old")
        new=request.POST.get("new")
        retype=request.POST.get("retype")
        if pswd == old:
            if new == retype:
                pwd.pwd_password=new
                pwd.save()
                return redirect('PWD:myprofile')
            else:
                return render(request,"PWD/ChangePassword.html",{'msg':"Password Mismatch"})
        else:
            return render(request,"PWD/ChangePassword.html",{'msg':"Invalid Password"})
    else:
        return render(request, "PWD/ChangePassword.html")
    

def viewcomplaint(request):
    pwd=tbl_pwd.objects.get(pwd_id=request.session['pid']) 
    complaint=tbl_complaint.objects.filter(pwd_id=pwd).annotate(like_count=Count('tbl_like')).order_by('-like_count')
    return render(request, "PWD/Viewcomplaint.html",{'complaint':complaint})

def reply(request,id):
    complaint=tbl_complaint.objects.get(id=id)
    if request.method=="POST":
        complaint.complaint_response=request.POST.get("txt_reply")
        complaint.complaint_status=1
        complaint.save()
        return redirect("PWD:viewcomplaint")
    else:
        return render(request, "PWD/Reply.html")


def updatests(request,id,sts):
   comp=tbl_complaint.objects.get(id=id)
   comp.complaint_status=sts
   comp.save()
   return redirect("PWD:viewcomplaint")

def viewreply(request):
    pwd=tbl_pwd.objects.get(pwd_id=request.session['pid']) 
    request=tbl_request.objects.filter(pwd=pwd)
    return render(request,"PWD/Viewreply.html",{'reply':reply})

def logout(request):
    del request.session['pid']
    return redirect("Guest:login")

def publicpost(request):
    data=tbl_publicpost.objects.filter(pwd=request.session['pid'])
    if request.method == "POST":
        photo=request.FILES.get("file_photo")
        if photo:
            try:
                # File name uses only user_id and the original photo name
                file_name = f"PostDocs/_{photo.name}"
                photo_content = photo.read()
                storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                photo_url = supabase.storage.from_("civic").get_public_url(file_name)
            except Exception as e:
                print(e)
                return render(request, "PWD/PublicPost.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None  # Handle cases where no photo is uploaded
        tbl_publicpost.objects.create(post_details=request.POST.get("txt_content"),
        post_file=photo_url,
        pwd=tbl_pwd.objects.get(pwd_id=request.session['pid']))
        return redirect("PWD:publicpost")
    else:
        return render(request,"PWD/PublicPost.html",{'data':data})
