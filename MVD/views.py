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
    return render(request, "MVD/Homepage.html")

def logout(request):
    del request.session['mvdid']
    return redirect("Guest:login")

def myprofile(request):
    mvd=tbl_mvd.objects.get(mvd_id=request.session['mvdid'])
    return render(request, "MVD/MyProfile.html",{'mvd':mvd})


def editprofile(request):
    mvd=tbl_mvd.objects.get(mvd_id=request.session['mvdid'])
    if request.method=="POST":
        mvd.mvd_name=request.POST.get("txt_name")
        mvd.mvd_email=request.POST.get("txt_email")
        mvd.mvd_contact=request.POST.get("txt_contact")
        mvd.mvd_address=request.POST.get("txt_address")
        mvd.save()
        return redirect('MVD:myprofile')
    else:
        return render(request, "MVD/EditProfile.html",{'mvd':mvd})

    

def changepassword(request):
    mvd=tbl_mvd.objects.get(mvd_id=request.session['mvdid'])
    if request.method=="POST":
        pswd=mvd.mvd_password
        old=request.POST.get("old")
        new=request.POST.get("new")
        retype=request.POST.get("retype")
        if pswd == old:
            if new == retype:
                mvd.mvd_password=new
                mvd.save()
                return redirect('MVD:myprofile')
            else:
                return render(request,"MVD/ChangePassword.html",{'msg':"Password Mismatch"})
        else:
            return render(request,"MVD/ChangePassword.html",{'msg':"Invalid Password"})
    else:
        return render(request, "MVD/ChangePassword.html")
    

def viewcomplaint(request):
    mvd=tbl_mvd.objects.get(mvd_id=request.session['mvdid']) 
    complaint=tbl_complaint.objects.filter(mvd_id=mvd).annotate(like_count=Count('tbl_like')).order_by('-like_count')
    return render(request, "MVD/Viewcomplaint.html",{'complaint':complaint})

def reply(request,id):
    complaint=tbl_complaint.objects.get(id=id)
    if request.method=="POST":
        complaint.complaint_response=request.POST.get("txt_reply")
        complaint.complaint_status="1"
        complaint.save()
        return redirect("MVD:viewcomplaint")
    else:
        return render(request, "MVD/Reply.html")

def updatests(request,id,sts):
   comp=tbl_complaint.objects.get(id=id)
   comp.complaint_status=sts
   comp.save()
   return redirect("MVD:viewcomplaint")

def viewreply(request):
    mvd=tbl_mvd.objects.get(mvd_id=request.session['mvdid']) 
    req=tbl_request.objects.filter(mvd=mvd)
    return render(request,"MVD/Viewreply.html",{'reply':req})

def requpdate(request,id,sts):
   req=tbl_request.objects.get(id=id)
   req.request_status=sts
   req.save()
   return redirect("MVD:viewreply")

def publicpost(request):
    data=tbl_publicpost.objects.filter(mvd=request.session['mvdid'])
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
                return render(request, "MVD/PublicPost.html", { "error": "Failed to upload photo."})
        else:
            photo_url = None  # Handle cases where no photo is uploaded
        tbl_publicpost.objects.create(post_details=request.POST.get("txt_content"),
        post_file=photo_url,
        mvd=tbl_mvd.objects.get(mvd_id=request.session['mvdid']))
        return redirect("MVD:publicpost")
    else:
        return render(request,"MVD/PublicPost.html",{'data':data})