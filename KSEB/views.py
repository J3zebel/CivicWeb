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
    return render(request, "KSEB/Homepage.html")

def myprofile(request):
    kseb=tbl_kseb.objects.get(kseb_id=request.session['kid'])
    return render(request, "KSEB/MyProfile.html",{'kseb':kseb})


def editprofile(request):
    kseb=tbl_kseb.objects.get(kseb_id=request.session['kid'])
    if request.method=="POST":
        kseb.kseb_name=request.POST.get("txt_name")
        kseb.kseb_email=request.POST.get("txt_email")
        kseb.kseb_contact=request.POST.get("txt_contact")
        kseb.kseb_address=request.POST.get("txt_address")
        kseb.save()
        return redirect('KSEB:myprofile')
    else:
        return render(request, "KSEB/EditProfile.html",{'kseb':kseb})

    

def changepassword(request):
    kseb=tbl_kseb.objects.get(kseb_id=request.session['kid'])
    if request.method=="POST":
        pswd=kseb.kseb_password
        old=request.POST.get("old")
        new=request.POST.get("new")
        retype=request.POST.get("retype")
        if pswd == old:
            if new == retype:
                kseb.kseb_password=new
                kseb.save()
                return redirect('KSEB:myprofile')
            else:
                return render(request,"KSEB/ChangePassword.html",{'msg':"Password Mismatch"})
        else:
            return render(request,"KSEB/ChangePassword.html",{'msg':"Invalid Password"})
    else:
        return render(request, "KSEB/ChangePassword.html")


def viewcomplaint(request):
    kseb=tbl_kseb.objects.get(kseb_id=request.session['kid']) 
    complaint = (tbl_complaint.objects.filter(kseb_id=kseb).annotate(like_count=Count('tbl_like')).order_by('-like_count'))
    return render(request, "KSEB/View Complaint.html",{'complaint':complaint})

def reply(request,id):
    complaint=tbl_complaint.objects.get(id=id)
    if request.method=="POST":
        complaint.complaint_response=request.POST.get("txt_reply")
        complaint.complaint_status="1"
        complaint.save()
        return redirect("KSEB:viewcomplaint")
    else:
        return render(request, "KSEB/Reply.html")

def updatests(request,id,sts):
   comp=tbl_complaint.objects.get(id=id)
   comp.complaint_status=sts
   comp.save()
   return redirect("KSEB:viewcomplaint")
   
    
def viewreply(request):
    kseb=tbl_kseb.objects.get(kseb_id=request.session['kid']) 
    req=tbl_request.objects.filter(kseb=kseb)
    return render(request,"KSEB/Viewreply.html",{'reply':req})


def requpdate(request,id,sts):
   req=tbl_request.objects.get(id=id)
   req.request_status=sts
   req.save()
   return redirect("KSEB:viewreply")

def logout(request):
    del request.session['kid']
    return redirect("Guest:login")


def publicpost(request):
    data=tbl_publicpost.objects.filter(kseb=request.session['kid'])
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
                return render(request, "KSEB/PublicPost.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None  # Handle cases where no photo is uploaded
        tbl_publicpost.objects.create(post_details=request.POST.get("txt_content"),
        post_file=photo_url,
        kseb=tbl_kseb.objects.get(kseb_id=request.session['kid']))
        return redirect("KSEB:publicpost")
    else:
        return render(request,"KSEB/PublicPost.html",{'data':data})