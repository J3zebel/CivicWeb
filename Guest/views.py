from django.shortcuts import render,redirect
from Guest.models import *
from django.conf import settings
from supabase import create_client
# Create your views here.



supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def index(request):
    return render(request, 'Guest/index.html')

def user(request):
    dis = tbl_district.objects.all()
    
    if request.method == "POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if auth_response.user:
                user_data = auth_response.user  
                user_id = user_data.id
                photo = request.FILES.get('photo')

                if photo:
                    try:
                        # File name uses only user_id and the original photo name
                        file_name = f"UserDocs/{user_id}_{photo}"
                        photo_content = photo.read()
                        storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                        photo_url = supabase.storage.from_("civic").get_public_url(file_name)
                    except Exception as e:
                        print(e)

                        return render(request, "Guest/User registration.html", {"district": dis, "error": "Failed to upload photo."})
                else:
                    photo_url = None  # Handle cases where no photo is uploaded
                
                # Save user details in the database
                
                tbl_user.objects.create(
                    user_id=user_id,
                    user_name=request.POST.get('txt_name'),
                    user_email=email,
                    user_contact=request.POST.get('txt_contact'),
                    localplace=tbl_localplace.objects.get(id=request.POST.get('local')),
                    user_address=request.POST.get('txt_address'),
                    muncipality=tbl_muncipality.objects.get(mun_id=request.POST.get('muncipality')),
                    user_photo=photo_url,
                    user_password=password,
                )
                

                
                return redirect('Guest:login')
            else:
                return render(request, "Guest/User registration.html", {"district": dis, "error": "Sign-up failed."})

        except Exception as e:
            print(e)
            return render(request, "Guest/User registration.html", {"district": dis, "error": "An error occurred during sign-up."})
    else:
        return render(request, "Guest/User registration.html", {"district": dis})

def ajaxplace(request):
    district_id = request.GET.get('did')
    place = tbl_place.objects.filter(district=district_id)
    return render(request, "Guest/AjaxPlace.html", {'place': place})

def ajaxmuncipality(request):
    mun_id = request.GET.get('mid')
    muncipality = tbl_muncipality.objects.filter(district=mun_id)
    return render(request, "Guest/Ajaxmuncipality.html", {'muncipality': muncipality})


def login(request):
    if request.method=="POST":
        email=request.POST.get('name')
        password=request.POST.get('password')

        auth_response=supabase.auth.sign_in_with_password({
            "email" : email,
            "password" : password
        })

        if auth_response.user:
            user_data=auth_response.user
            user_id=user_data.id
            
            
            try:
                user=tbl_user.objects.get(user_id=user_id)
                request.session['uid']=user.user_id

                return redirect("User:homepage")
                
            except tbl_user.DoesNotExist:
                try:
                    muncipality=tbl_muncipality.objects.get(mun_id=user_id)
                    request.session['mid']=muncipality.mun_id
                    return redirect("Muncipality:homepage")
                
                except tbl_muncipality.DoesNotExist:
                    try:
                        mvd=tbl_mvd.objects.get(mvd_id=user_id)
                        request.session['mvdid']=mvd.mvd_id
                        return redirect("MVD:homepage")
                
                    except tbl_mvd.DoesNotExist:
                        try:
                            pwd=tbl_pwd.objects.get(pwd_id=user_id)
                            request.session['pid']=pwd.pwd_id
                            return redirect("PWD:homepage")
                
                        except tbl_pwd.DoesNotExist:
                            try:
                                kseb=tbl_kseb.objects.get(kseb_id=user_id)
                                request.session['kid']=kseb.kseb_id
                                return redirect("KSEB:homepage")
                
                            except tbl_kseb.DoesNotExist:
                                try:
                                    admin=tbl_admin.objects.get(admin_id=user_id)
                                    request.session['aid']=admin.admin_id
                                    request.session['aname']=admin.admin_name
                                    return redirect("Admin:homepage")
                                except tbl_admin.DoesNotExist:
                                    return render(request,"Guest/Login.html",{"error":"User DoesNot Exist"})

        else:
            return render(request,"Guest/Login.html",{"error":"Invalid Data"})
    else:
        return render(request,'Guest/Login.html')
    

def muncipality(request):
    dis = tbl_district.objects.all()
    if request.method == "POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if auth_response.user:
                mun_data = auth_response.user  
                mun_id = mun_data.id
                proof = request.FILES.get('photo')

                if proof:
                    try:
                        # File name uses only user_id and the original photo name
                        file_name = f"MuncipalDocs/{mun_id}_{proof.name}"
                        photo_content = proof.read()
                        storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                        photo_url = supabase.storage.from_("civic").get_public_url(file_name)
                    except Exception as e:
                        print(e)
                        return render(request, "Guest/Muncipality.html", {"district": dis, "error": "Failed to upload photo."})
                else:
                    photo_url = None  # Handle cases where no photo is uploaded
                
                # Save user details in the database
                tbl_muncipality.objects.create(
                    mun_id=mun_id,
                    mun_name=request.POST.get('txt_name'),
                    mun_email=email,
                    mun_contact=request.POST.get('txt_contact'),
                    mun_address=request.POST.get('txt_address'),
                    mun_proof=photo_url,
                    mun_password=password,
                    district=tbl_district.objects.get(id=request.POST.get('district'))
                )
                
                return redirect('Guest:login')
            else:
                return render(request, "Guest/Muncipality.html", {"district": dis, "error": "Sign-up failed."})

        except Exception as e:
            print(e)
            return render(request, "Guest/Muncipality.html", {"district": dis, "error": "An error occurred during sign-up."})
    else:
        return render(request, "Guest/Muncipality.html", {"district": dis})


def mvd(request):
    dis = tbl_district.objects.all()
    if request.method == "POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if auth_response.user:
                mvd_data = auth_response.user  
                mvd_id = mvd_data.id
                proof = request.FILES.get('photo')

                if proof:
                    try:
                        # File name uses only user_id and the original photo name
                        file_name = f"mvdDocs/{mvd_id}_{proof.name}"
                        photo_content = proof.read()
                        storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                        photo_url = supabase.storage.from_("civic").get_public_url(file_name)
                    except Exception as e:

                        return render(request, "Guest/MVD.html", {"district": dis, "error": "Failed to upload photo."})
                else:
                    photo_url = None  # Handle cases where no photo is uploaded
                
                # Save user details in the database
                tbl_mvd.objects.create(
                    mvd_id=mvd_id,
                    mvd_name=request.POST.get('txt_name'),
                    mvd_email=email,
                    mvd_contact=request.POST.get('txt_contact'),
                    mvd_address=request.POST.get('txt_address'),
                    mvd_proof=photo_url,
                    mvd_password=password,
                    district=tbl_district.objects.get(id=request.POST.get('district'))
                )
                
                return redirect('Guest:login')
            else:
                return render(request, "Guest/MVD.html", {"district": dis, "error": "Sign-up failed."})

        except Exception as e:
            print(e)
            return render(request, "Guest/MVD.html", {"district": dis, "error": "An error occurred during sign-up."})
    else:
        return render(request, "Guest/MVD.html", {"district": dis})
    
def pwd(request):
    dis = tbl_district.objects.all()
    if request.method == "POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if auth_response.user:
                pwd_data = auth_response.user  
                pwd_id = pwd_data.id
                proof = request.FILES.get('photo')

                if proof:
                    try:
                        # File name uses only user_id and the original photo name
                        file_name = f"mvdDocs/{pwd_id}_{proof.name}"
                        photo_content = proof.read()
                        storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                        photo_url = supabase.storage.from_("civic").get_public_url(file_name)
                    except Exception as e:

                        return render(request, "Guest/PWD.html", {"district": dis, "error": "Failed to upload photo."})
                else:
                    photo_url = None  # Handle cases where no photo is uploaded
                
                # Save user details in the database
                tbl_pwd.objects.create(
                    pwd_id=pwd_id,
                    pwd_name=request.POST.get('txt_name'),
                    pwd_email=email,
                    pwd_contact=request.POST.get('txt_contact'),
                    pwd_address=request.POST.get('txt_address'),
                    pwd_proof=photo_url,
                    pwd_password=password,
                    district=tbl_district.objects.get(id=request.POST.get('district'))
                )
                
                return redirect('Guest:login')
            else:
                return render(request, "Guest/PWD.html", {"district": dis, "error": "Sign-up failed."})

        except Exception as e:
            print(e)
            return render(request, "Guest/PWD.html", {"district": dis, "error": "An error occurred during sign-up."})
    else:
        return render(request, "Guest/PWD.html", {"district": dis})
    
def kseb(request):
    dis=tbl_district.objects.all()
    if request.method == "POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if auth_response.user:
                kseb_data = auth_response.user  
                kseb_id = kseb_data.id
                proof = request.FILES.get('photo')

                if proof:
                    try:
                        # File name uses only user_id and the original photo name
                        file_name = f"ksebDocs/{kseb_id}_{proof.name}"
                        photo_content = proof.read()
                        storage_response = supabase.storage.from_("civic").upload(file_name, photo_content)
                        photo_url = supabase.storage.from_("civic").get_public_url(file_name)
                    except Exception as e:

                        return render(request, "Guest/PWD.html", {"district": dis, "error": "Failed to upload photo."})
                else:
                    photo_url = None  # Handle cases where no photo is uploaded
                
                # Save user details in the database
                tbl_kseb.objects.create(
                    kseb_id=kseb_id,
                    kseb_name=request.POST.get('txt_name'),
                    kseb_email=email,
                    kseb_contact=request.POST.get('txt_contact'),
                    kseb_address=request.POST.get('txt_address'),
                    localplace=tbl_localplace.objects.get(id=request.POST.get('local')),
                    kseb_proof=photo_url,
                    kseb_password=password,
                )
                
                return redirect('Guest:login')
            else:
                return render(request, "Guest/KSEB.html", {"district": dis, "error": "Sign-up failed."})

        except Exception as e:
            print(e)
            return render(request, "Guest/KSEB.html", {"district": dis, "error": e})
    else:
        return render(request, "Guest/KSEB.html", {"district": dis})
    
def ajaxlocal(request):
    place_id = request.GET.get('pid')
    local = tbl_localplace.objects.filter(place=place_id)
    return render(request, "Guest/AjaxLocal.html", {'local': local})



        

