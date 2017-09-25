from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect, get_object_or_404, render
from django.template import RequestContext
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponseRedirect
# from django_messages.models import Message
from django.utils import timezone
# from django_messages.utils import format_quote
from models import Message
from utils import format_quote
from django.utils.translation import ugettext as _
import sys
from django.conf import settings
import stripe
from django.core.mail import EmailMultiAlternatives

secretKey=settings.STRIPE_SECRET_KEY

stripe.api_key = secretKey

sys.setrecursionlimit(50000)

dashboard_type = ""


def index(request):  
    ''' Home Page'''
    home="index_page"
    role_user=Userroles.objects.filter(user_id=request.user.id)
    print ""
    conformation_researcher=""
    conformation_lab=""

    for role in role_user:
        usr_type=role.role_id
        if usr_type==1:
            conformation_researcher="researcher"
        elif usr_type==2:
            conformation_lab="conformation_lab"
        else:
            pass
    
    return render_to_response('new_index.html',{'conformation_researcher':conformation_researcher,'conformation_lab':conformation_lab,
        "home":home},context_instance=RequestContext(request))

def signup_researcher(request):
    '''Buyer Registration'''
    singup_view = "this is researcher signup"
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            first_name1 = request.POST.get("first_name")
            first_name =first_name1.capitalize()            
            last_name1 = request.POST.get("last_name")
            last_name=last_name1.capitalize()            
            pwd =request.POST.get("password")
            mail = request.POST.get("email")
            user_type = request.POST.get("check_user")
            phone_num=request.POST.get("phone_number")
            name = first_name+last_name
            company=request.POST.get("companey")
            email_check=User.objects.filter(email=mail)
            if email_check:
                error_message="Email address already exists"
                return render_to_response('signup_researcher.html',
                    {'form': form,'error_message':error_message,},
                    context_instance=RequestContext(request))
            else:
                user = User.objects.create_user(name, mail, pwd)
                user_id = User.objects.filter(username=name)
                for usr in user_id:
                    Userroles(user_id= usr.id,role_id=1,roll_name=user_type).save()   
                    Users(user_id=usr.id,role_id=1,
                        fname=first_name,lname=last_name,
                        email=mail,phone=phone_num,name_org=company,username=name,is_active=1).save()
                    Profilepic(user_id=user.id).save()   
                return render_to_response('signup_success.html',
                    context_instance=RequestContext(request))
    else:
        form = Registrationform()
    return render_to_response('signup_researcher.html', 
        {'form': form,'view_name':singup_view},
        context_instance=RequestContext(request))

def signup_lab(request):
    '''Provider Registration'''
    error_message=""
    type_org = ""
    action=1
    if request.method == 'POST':
        form = Lab_registrationform(request.POST)
        if form.is_valid():
            first_name1 = request.POST.get("first_name")
            first_name=first_name1.capitalize()
            last_name1 = request.POST.get("last_name")
            last_name=last_name1.capitalize()
            pwd =request.POST.get("password")
            mail = request.POST.get("email")
            user_type = request.POST.get("check_user")
            phone_num=request.POST.get("phone_number")
            title = request.POST.get("title")
            orgname=request.POST.get("orgname")
            type_org=request.POST.get("company")
            facility=request.POST.get("facility")
            servicedec=request.POST.get("service_cap")
            name = first_name+''+last_name
            email_check=User.objects.filter(email=mail)
            if email_check:
                error_message="Email address already exists"
                return render_to_response('signup_lab.html',
                    {'form': form,'error_message':error_message,},
                    context_instance=RequestContext(request))
            else: 
                user = User.objects.create_user(name, mail, pwd)
                user_id = User.objects.filter(email=mail)
                
                for usr in user_id:
                    Userroles(user_id= usr.id,role_id=2,roll_name=user_type).save()   
                    Users(user_id=usr.id,role_id=2, fname=first_name,lname=last_name,email=mail,phone=phone_num,name_org=orgname).save()    
                    Lab(user_id =usr.id,title=title,orgname=orgname,typeorg=type_org,core_facility=facility,desc=servicedec).save()
                deactivte_user = User.objects.filter(email=mail).update(is_active=0)
                success_message = "Thank you for your request. A provider listing specialist will contact you shortly."
                return render_to_response('new_index.html',{'success_message':success_message},
                    context_instance=RequestContext(request))
    else:
        form = Lab_registrationform()
    return render_to_response('signup_lab.html',{'form': form,'error_message':error_message,
        },
        context_instance=RequestContext(request))

def login(request):
    '''Login'''
    login_view="This is login view" 
    error_message=""
    user = ""
    print "login"
    if request.method == 'POST':
        print "pst method"
        form = Loginform(request.POST)
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if form.is_valid():
            print "valid"
            if user:
                if user.is_active:
                    print "active"
                    auth_login(request, user)


                    users = User.objects.filter(email=email)
                    uid=None
                    for user in users:
                        uid=user.id
                    check_lab=None
                    check_labs= Userroles.objects.filter(user_id=uid)
                    for i in check_labs:
                        check_lab=i.roll_name
                    print "roll_name"
                    print check_lab                    
                    
                    if user.is_superuser:
                        print "admin"
                        return redirect("/")
                    elif check_lab=="researcher":
                        print "buyer logged in"
                        return redirect("/buyer/")
                    else:
                        print "provider logged in"
                        return redirect("/provider/")
                    # print "&&&&&&&&&&"
                    # print user
                    # except Exception:
                    #     return redirect("/")
                    #     pass            
                    # try :                        
                    #     uid = User.objects.get(email=email).id
                    #     check_lab= Userroles.objects.get(user_id=uid).roll_name
                    #     print "roll_name"
                    #     print check_lab
                    #     if check_lab=="researcher":
                    #         return redirect("/buyer/")
                    #     else:
                    #         return redirect("/provider/") 
                    # except Exception:
                    #     return redirect("/")
                    #     pass                   
                else:
                    error_message ="Sorry your account not activated"
            else:
                error_message ="Email and Password did not match."
    else:
        form = Loginform()
    return render(request, 'login.html', {'form':form,
        'login_view':login_view,'error_message':error_message},context_instance=RequestContext(request))

def logout_page(request):
    ''' Logout '''
    logout(request)
    return redirect('/')

@login_required
def editprofile(request):
    '''Edit Lab Profile'''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2: 
        conformation_lab="conformation_lab"
        usr_data=Users.objects.filter(user_id=request.user.id)
        error_message=""
        name1 = ""
        name2=""
        email =""
        phone_num =""
        how_bio=""
        name_org=""
        roleid = None
        for usr in usr_data:
            name1 = usr.fname
            name2=usr.lname
            email=usr.email
            phone_num=usr.phone
            how_bio = usr.how_bio
            name_org =usr.name_org
            roleid = usr.role_id
        if request.method == 'POST':
            form = Editprofileform(request.POST)
            if form.is_valid():
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                mail = request.POST.get("email")
                user_type = request.POST.get("check_user")
                phone_num=request.POST.get("phone_number")
                how_bio=request.POST.get("how_bio")
                name_org=request.POST.get("name_org")
                name = first_name+last_name
                Users.objects.filter(user_id =request.user.id).update(fname=first_name,
                    lname=last_name,email=mail,how_bio=how_bio,
                    name_org=name_org,phone=phone_num)

                User.objects.filter(id=request.user.id).update(email=mail,username=name)
                return redirect("/login/")
        else:
            form =  Editprofileform()
        print name1,name2,email,phone_num    
        return render_to_response('edit_profile.html',{'form':form,'name1':name1,
            'conformation_lab':conformation_lab, 'name2':name2,'email':email,'phone_num':phone_num},
            context_instance=RequestContext(request))
    else :        
        return redirect("/logout/")

@login_required
def lab_listing(request):
    ''' Lab Listing Page'''
    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2: 
        conformation_lab="conformation_lab"
        uid = request.user.id
        if request.method == 'POST':
            form = Lablistingform(request.POST)
            if form.is_valid():
                title = request.POST.get('Title')
                caption= request.POST.get('Caption')
                desc=request.POST.get('Desc')
                country = request.POST.get('country')
                lab_store =Lab(user_id =uid,title=title,caption=caption,desc=desc,country=country).save()
                return redirect("/lab-services/")     
        else:
            form = Lablistingform()
        return render_to_response('lab_listing.html',{'form': form,"conformation_lab":conformation_lab,
            },
            context_instance=RequestContext(request))
    else :        
        return redirect("/logout/")

@login_required
def lab_services(request):
    ''' Lab Services View '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"
        # form = AddLabservicesform()
        print "Adding lab services view"
        if request.method == 'POST':
            print "if post  block"
            form = AddLabservicesform(request.POST)
            if form.is_valid():
                title = request.POST.get('service_title')
                descrption = request.POST.get('service_desc')
                price = request.POST.get('service_price')
                currency = request.POST.get('service_currency')
                unit = request.POST.get('service_unit')
                url=request.POST.get('service_url')
                lab_id=None
                labuser = Lab.objects.filter(user_id=request.user.id)
                for lab in labuser:
                    lab_id=lab.id
                LabServices(lab_id=lab_id,title =title,
                   desc=descrption,price=price,url=url,currency=currency,unit=unit).save()
                messages.success(request,(u"Your Lab Service added successfully"))
                return redirect("/provider/profile")        
        else:
            print "else block"
            form = AddLabservicesform()            
        return render_to_response('lab/lab-profile.html',{'form': form,'conformation_lab':conformation_lab},
            context_instance=RequestContext(request))
        '''Lab Services'''
        print "lab services"
        lab_id=None
        labuser=Lab.objects.filter(user_id=request.user.id)
        for lab in labuser:
            lab_id=lab.id
        lab_profle_info = Lab.objects.filter(user_id=request.user.id)
        lab_service_info = LabServices.objects.filter(lab_id=lab_id)

        return render_to_response('', 
            {'services':lab_service_info,},
            context_instance=RequestContext(request))


    else :        
        return redirect("/logout/")

@login_required
def lab_reviews(request):
    ''' Lab Reviews View '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"
        if request.method == 'POST':
            form = Labreviewsform(request.POST)
            if form.is_valid():
                descrption = request.POST.get('Desc')
                lab_id=None
                labuser = Lab.objects.filter(user_id=request.user.id)
                for lab in labuser:
                    lab_id=lab.id
                # labuser = Lab.objects.get(user_id=request.user.id).id
                LabReviews(lab_id =lab_id, desc=descrption).save()
                return HttpResponse("lab reviews store in DB")        
        else:
            form = Labreviewsform()        
        return render_to_response('reviews.html',{'form': form,'conformation_lab':conformation_lab,},
            context_instance=RequestContext(request))

    else :        
        return redirect("/logout/")

@login_required
def lab_endorse(request):
    ''' Lab Endorse View '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"
        if request.method == 'POST':
            form = Labendorseform(request.POST)
            if form.is_valid():
                desc = request.POST.get('Desc')
                # labuser = Lab.objects.get(user_id=request.user.id).id
                lab_id=None
                labuser = Lab.objects.filter(user_id=request.user.id)
                for lab in labuser:
                    lab_id=lab.id
                LabEndorse(lab_id =lab_id, desc=desc).save()
                return HttpResponse("lab endorse store in DB")        
        else:
            form = Labendorseform()
        return render_to_response('endorse.html',{'form': form,'conformation_lab':conformation_lab,},
            context_instance=RequestContext(request))
    else :        
        return redirect("/logout/")

@login_required
def show_your_lab(request):
    ''' Displaying Lab Details '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"
        labid = None
        labs = Lab.objects.filter(user_id=request.user.id)
        for lab in labs:
            labid=lab.id
        country =""
        descrption = ""
        title =""
        caption = ""
        service_title = ""
        service_desc=""
        service_price=None
        lab_user = Lab.objects.filter(user_id=request.user.id)
        for lab in lab_user:
            title=lab.title
            descrption = lab.desc
            caption = lab.caption
            country = lab.country
        lab_service = LabServices.objects.filter(lab_id = labid)
        lab_review = LabReviews.objects.filter(lab_id = labid)
        lab_endorse = LabEndorse.objects.filter(lab_id = labid)
        lab_profile = {'title':title,'descrption':descrption,'caption':caption,
        'country':country,'lab_service':lab_service,'lab_review':lab_review,'lab_endorse':lab_endorse,
        'conformation_lab':conformation_lab}
        
        return render_to_response('lab-details.html',lab_profile,
            context_instance=RequestContext(request))
    else :        
        return redirect("/logout/")

def list_your_lab(request):
    ''' List you lab View '''    
    conformation_lab="conformation_lab"
    return render_to_response('list-your-lab.html',{'conformation_lab':conformation_lab,},
        context_instance=RequestContext(request))   

def signup_select(request):
    ''' Registration based on this selection '''

    return render_to_response('signup.html',
        context_instance=RequestContext(request))

def autocomplete_searrch(request):
    ''' Auto Complete '''

    #demo = ['Audi', 'BMW', 'Bugatti', 'Ferrari', 'Ford', 'Lamborghini', 'Mercedes Benz', 'Porsche', 'Rolls-Royce', 'Volkswagen']
    demo = ['test', 'test1', 'raghu', 'swamy', 'swamy123', '', 'Mercedes Benz', 'Porsche', 'Rolls-Royce', 'Volkswagen']
    return render_to_response('auto.html',{'demo':demo},
        context_instance=RequestContext(request))

@login_required
def lab_profile_page(request):
    ''' Lab Profile View '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"
        # lab_id=Lab.objects.get(user_id=request.user.id).id
        lab_id=None
        labuser = Lab.objects.filter(user_id=request.user.id)
        for lab in labuser:
            lab_id=lab.id
        lab_profle_info = Lab.objects.filter(user_id=request.user.id)
        lab_service_info =LabServices.objects.filter(lab_id=lab_id)
        paginator = Paginator(lab_service_info,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        lab_title = ""
        lab_name = ""
        lab_description=""
        orgtype=""
        ser_title=""
        ser_price=None
        ser_desc=""
        ser_url=""
        pic=""
        caption=""

        for lab_info in lab_profle_info:
            lab_title=lab_info.title
            lab_name=lab_info.orgname
            lab_description=lab_info.desc
            orgtype=lab_info.typeorg
            city=lab_info.city
            state=lab_info.state
            country=lab_info.country
            pic=lab_info.model_pic
            caption=lab_info.caption

        for service in lab_service_info:
            ser_title=service.title
            ser_price=service.price
            ser_desc=service.desc
            ser_url=service.url

        return render_to_response('lab-profile-new.html',
            {
            'lab_title':lab_title,
            'lab_name':lab_name,
            'lab_description':lab_description,
            'orgtype':orgtype,
            'city':city,
            'state':state,
            'country':country,
            'pic':pic,
            "caption":caption,
            'ser_title':ser_title,
            'ser_price':ser_price,
            'ser_desc':ser_desc,
            'ser_url':ser_url,
            'lab_service_info':contacts,
            'contacts':contacts,
            'conformation_lab':conformation_lab,
            },
            context_instance=RequestContext(request))
    else :        
        return redirect("/logout/")

@login_required
def researcher_profile_page(request):
    ''' Buyer Profile View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    print role_users
    for user in role_users:
        role_user=user.role_id
    print "buyer_profile"
    print role_user

    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        current_loggedin_user=request.user.id
        logged_user=request.user.id
        userinfo=Users.objects.filter(user_id=logged_user)
        fname=""
        lname=""
        username=fname+lname
        company= ""
        logo=""
        for usr in userinfo:
            fname=usr.fname
            lname=usr.lname
            username=fname+lname
            company=usr.name_org        
        image_logo=Profilepic.objects.filter(user_id=request.user.id)
        for img in image_logo:
            logo=img.model_pic

        return render_to_response('researcher/new_researcher_dashboard.html',{'username':username,
            'company':company,
            'conformation_researcher':conformation_researcher,
            'logo':logo},
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")

@login_required
def edit_lab_profile(request):
    ''' Edit Lab Profile View '''

    
    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"
        current_loggedin_user=request.user.id
        if request.method == 'POST':
            form = EditLabform(request.POST,request.FILES)
            if form.is_valid():
                title = request.POST.get("title")
                orgname = request.POST.get("orgname")
                service_cap = request.POST.get("desc")
                city=request.POST.get("city")            
                state=request.POST.get("state")
                country=request.POST.get("country")
                logo = form.cleaned_data['model_pic'] 

                if logo:
                    Lab.objects.filter(user_id=request.user.id).delete()
                    Lab(user_id=request.user.id,title=title,
                    orgname=orgname,desc=service_cap,city=city,
                    state=state,country=country,model_pic=logo).save()
                else:
                    Lab.objects.filter(user_id=request.user.id).update(title=title,
                    orgname=orgname,desc=service_cap,city=city,
                    state=state,country=country)            
                return redirect("/provider/profile/")
        else:
            form = EditLabform()

        return render_to_response('edit_lab_profile.html',{'form':form,'conformation_lab':conformation_lab},
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")

def addservices(request,id):
    return lab_profile_page(request)

@login_required
def edit_lab_services(request,lab_service_id):
    ''' Edit Lab Services View '''

    
    print "edit provider service"
    print lab_service_id
    print "88888888888888888888"
    l_service=""
    print "-----------------------"
    print request.GET

    service_id=""
    service_title=""
    service_desc=""
    service_price=""
    service_currency=""
    service_url=""
    service_unit=""


    # for key,value in request.GET.items():
    #     print key
    #     print value
    print "---------------------"
    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:

        l_service = LabServices.objects.get(id=lab_service_id)
        print "==================="
        print l_service.title
        print l_service.id
        print l_service.desc
        print l_service.price

        print type(l_service)

        service_id=l_service.id
        service_title=l_service.title
        service_desc=l_service.desc
        service_price=l_service.price
        service_currency=l_service.currency
        service_unit=l_service.unit
        service_url=l_service.url
        
        data = {"service_title":"l_service.title"}
        form = AddLabservicesform(initial=data)
        # print l_service.title
        conformation_lab="conformation_lab"
        if request.method == 'POST':
            form = AddLabservicesform(request.POST)
            if form.is_valid():
                service_id = request.POST.get('service_id')
                title = request.POST.get('service_title')
                descrption = request.POST.get('service_desc')
                price = request.POST.get('service_price')
                currency = request.POST.get('service_currency')
                unit = request.POST.get('service_unit')
                url=request.POST.get('service_url')
                # labuser = Lab.objects.get(user_id=request.user.id).id
                labuser=None
                labusers = Lab.objects.filter(user_id=request.user.id)
                for lab in labusers:
                    labuser=lab.id
                # LabServices.objects.filter(id=service_id).update(title=title,
                #    desc=descrption,price=price,url=url,currency=currency,unit=unit)
                LabServices.objects.filter(id=lab_service_id).update(title=title,
                   desc=descrption,price=price,url=url,currency=currency,unit=unit)
                messages.success(request,(u"Your Lab Service updated successfully"))
                return redirect("/provider/profile/")
        else:
            print "else block"

        print "not in loop"
        print form
        return render_to_response('lab/lab-profile.html',
            {'form': form,'conformation_lab':conformation_lab,
            'service_id':service_id,
            'service_title':service_title,
            'service_desc':service_desc,
            'service_price':service_price,
            'service_currency':service_currency,},
            context_instance=RequestContext(request))

    else:
        return redirect("/logout/")

@login_required
def edit_provider_service(request,lab_service_id):

    print "edit provider service"
    print lab_service_id
    print "---------"


    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:

        l_service = LabServices.objects.get(id=lab_service_id)

        service_id=l_service.id
        service_title=l_service.title
        service_desc=l_service.desc
        service_price=l_service.price
        service_currency=l_service.currency
        service_unit=l_service.unit
        service_url=l_service.url

        currency = ['US-dollor','UK-Pound','UAE-Dirham']
        unit = ['Unit-I','Unit-II','Unit-III']

        conformation_lab="conformation_lab"
        if request.method == 'POST':
            form = AddLabservicesform(request.POST)
            if form.is_valid():
                service_id = request.POST.get('service_id')
                title = request.POST.get('service_title')
                descrption = request.POST.get('service_desc')
                price = request.POST.get('service_price')
                currency = request.POST.get('service_currency')
                unit = request.POST.get('service_unit')
                url=request.POST.get('service_url')
                # labuser = Lab.objects.get(user_id=request.user.id).id
                labuser=None
                labusers = Lab.objects.filter(user_id=request.user.id)
                for lab in labusers:
                    labuser=lab.id
                # LabServices.objects.filter(id=service_id).update(title=title,
                #    desc=descrption,price=price,url=url,currency=currency,unit=unit)
                LabServices.objects.filter(id=lab_service_id).update(title=title,
                   desc=descrption,price=price,url=url,currency=currency,unit=unit)
                messages.success(request,(u"Your Lab Service updated successfully"))
                return redirect("/provider/profile/")
        else:
            print "else block"
            form = AddLabservicesform()

        return render_to_response("lab/provider-service-edit.html",
        {'form':form,
        'service_id':service_id,
        'service_title':service_title,
        'service_desc':service_desc,
        'service_price':service_price,
        'service_unit':service_unit,
        'service_currency':service_currency,
        'service_url':service_url,
        'currency':currency,'unit':unit,},
        context_instance=RequestContext(request))

    else:
        return redirect("/logout/") 



@login_required
def del_lab_service(request,lab_service_id):
    print " deleting lab service"
    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        print "before delete labservice"

        result = LabServices.objects.filter(id=lab_service_id).delete()

        print "After delete labservice"
        messages.success(request,(u"Your Lab Service deleted successfully"))
        return redirect("/provider/profile/")

    else:
        return redirect("/logout/")


def upload_labphotos(request):
    conformation_lab="conformation_lab"
    if request.method == 'POST':
        form = LabphotosForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()            
            return HttpResponse("image succesfully uploaded")
            #return redirect("/lab-profile-page/")
    else:
        form = LabphotosForm()
    return render_to_response('labphotos.html',{'form': form,'conformation_lab':conformation_lab},
        context_instance=RequestContext(request))

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = ExampleModel.objects.get(pk=course_id)
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    else:
        form = ImageUploadForm()
    return render_to_response('labphotos.html',{'form': form,},
        context_instance=RequestContext(request))

@login_required
def edit_researcher_profile(request):
    ''' Edit Researcher Profile View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:   
        conformation_researcher="researcher"
        researchr_info=Users.objects.filter(user_id=request.user.id)
        email=""
        fname=""
        lname=""
        org_name=""
        phone=""
        logo=""
        user_desc=""
        model_pic=""
        username=fname+lname
        researcher_logo=""    
        res_logo =Profilepic.objects.filter(
            user_id=request.user.id)
        for res in res_logo:
            researcher_logo=res.model_pic
        for res in researchr_info:
            email=res.email
            fname=res.fname
            lname=res.lname
            org_name=res.name_org
            phone=res.phone
        description =Researcher_more_info.objects.filter(user_id=request.user.id)
        for desc in description:
            user_desc=desc.desc

        """ Employment View Start  """
        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse() 

        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()
        publications_data =Researcher_publications.objects.filter(
            user_id=request.user.id).order_by('id').reverse()

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        paginator2 = Paginator(publications_data,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
            contacts2 = paginator2.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
            contacts2 = paginator2.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
            contacts2 = paginator2.page(paginator2.num_pages)

        """ Employment View End  """
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()
        if request.method == 'POST':
            form = EditResearcherForm(request.POST,request.FILES)
            if form.is_valid():
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                name1=request.POST.get('first_name')
                name2=request.POST.get('last_name')
                orgname=request.POST.get('companey')
                mobile=request.POST.get('phone_number')
                publication=request.POST.get('publications')            
                model_pic = form.cleaned_data['image']
                fullname=name1+name2
                User.objects.filter(id=request.user.id).update(email=mail_id,
                    username=fullname)
                Users.objects.filter(user_id=request.user.id).update(
                   email=mail_id,
                   fname=name1,
                   lname=name2,
                   name_org=orgname,
                   phone=mobile,
                   username=fullname
                   )
                if model_pic:               
                    Profilepic.objects.filter(user_id=request.user.id).delete()
                    Profilepic(user_id=request.user.id,model_pic=model_pic).save()
                    logo=Profilepic.objects.get(user_id=request.user.id).model_pic

                messages.success(request, (u"Your profile updated succesfully"))
                return redirect("/buyer/edit/basics/")            
        else:
            form = EditResearcherForm()    
        
        return render_to_response('researcher/edit-researcher-basic.html',{'form':form,
            'form1':form1,
            'form2':form2,
            'form3':form3,
            'form4':form4,
            'email':email,
            'fname':fname,
            'lname':lname,
            'org_name':org_name,
            'phone':phone,
            'conformation_researcher':conformation_researcher,
            'user_desc':user_desc,
            'researcher_logo':researcher_logo,
            'education_info':education_info,
            'education_info3':education_info3,
            'contacts':contacts,
            'contacts1':contacts1,
            'contacts2':contacts2,
            },
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")

@login_required
def edit_researcher_password(request):
    ''' Edit Researcher Password View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        error_msg=""
        email=User.objects.get(id=request.user.id).email
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()
        if request.method == 'POST':
            form1 = EditPasswordForm(request.POST)
            if form1.is_valid():
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                if password1==password2:
                    user = User.objects.get(id=request.user.id)
                    user.set_password(password1)
                    user.save()
                    messages.success(request, (u"Your Password Changed Succesfully"))
                    user = authenticate(email=email, password=password1)                
                    if user.is_active:                    
                        auth_login(request, user)
                        return redirect("/buyer/edit/basics/")
                    else:
                        return redirect("/login/")
                else:
                    error_msg="Confirm new password doesn't match"
        else:
            form1 = EditPasswordForm()    
        return render_to_response('researcher/edit-res-password.html',{'form1':form1,
            'form2':form2,
            'form3':form3,
            'form4':form4,
            'error_msg':error_msg,
            'conformation_researcher':conformation_researcher},
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")


@login_required
def researcher_education(request):
    ''' Edit Researcher Education View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()        
        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse()
        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
        return render_to_response('researcher/new_res_education.html',{'education_info3':education_info3,
                'contacts1':contacts1,'conformation_researcher':conformation_researcher,
                'education_info':education_info, 'contacts':contacts,
                'form1':form1, 'form2':form2, 'form3':form3,'form4':form4,
                },
        context_instance=RequestContext(request))
    else:
        return redirect("/logout/")

@login_required
def add_degree(request):
    ''' Add degree for Researcher Profile View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        error_msg=""
        researchr_info=Users.objects.filter(user_id=request.user.id)
        email=""
        fname=""
        lname=""
        org_name=""
        phone=""
        logo=""
        user_desc=""
        model_pic=""
        username=fname+lname
        researcher_logo=""    
        res_logo =Profilepic.objects.filter(
            user_id=request.user.id)
        for res in res_logo:
            researcher_logo=res.model_pic
        for res in researchr_info:
            email=res.email
            fname=res.fname
            lname=res.lname
            org_name=res.name_org
            phone=res.phone
        description =Researcher_more_info.objects.filter(user_id=request.user.id)
        for desc in description:
            user_desc=desc.desc
        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse()
        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()
        publications_data =Researcher_publications.objects.filter(
            user_id=request.user.id).order_by('id').reverse()

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        paginator2 = Paginator(publications_data,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
            contacts2 = paginator2.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
            contacts2 = paginator2.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
            contacts2 = paginator2.page(paginator2.num_pages)

        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()

        ''' Edit Basics Form '''

        if request.method == 'POST':
            form = EditResearcherForm(request.POST,request.FILES)
            if form.is_valid():
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                name1=request.POST.get('first_name')
                name2=request.POST.get('last_name')
                orgname=request.POST.get('companey')
                mobile=request.POST.get('phone_number')
                publication=request.POST.get('publications')
                
                model_pic = form.cleaned_data['image']
                fullname=name1+name2
                User.objects.filter(id=request.user.id).update(email=mail_id,
                    username=fullname)
                Users.objects.filter(user_id=request.user.id).update(
                   email=mail_id,
                   fname=name1,
                   lname=name2,
                   name_org=orgname,
                   phone=mobile,
                   username=fullname
                   )
                
                if model_pic:                   
                    Profilepic.objects.filter(user_id=request.user.id).delete()
                    Profilepic(user_id=request.user.id,model_pic=model_pic).save()
                    logo=Profilepic.objects.get(user_id=request.user.id).model_pic

                messages.success(request, (u"Your profile updated succesfully"))
                return redirect("/buyer/edit/basics/")


        ''' Edit education form '''

        if request.method == 'POST':
            form3 = ResearcherEducationForm(request.POST)
            study_end=""
            study_checked=""
            if form3.is_valid():
                institute = request.POST.get('institute')
                degree = request.POST.get('degree')
                field_study = request.POST.get('field_study')
                notes = request.POST.get('notes')
                study_start=request.POST.get('study_start')
                study_end=request.POST.get('study_end')
                study_checked=request.POST.get('study_checked')
                if study_end  and not(study_start):
                    error_msg="Please select date started field"

                else:
                    if study_checked:
                        Researcher_education(user_id=request.user.id,institute=institute,
                            degree=degree,field_study=field_study,notes=notes,
                            study_start=study_start,study_stop=study_end,
                            study_continue="continuing"
                            ).save()
                        messages.success(request, (u"Education record was successfully created."))
                        return redirect("/buyer/edit/education")

                    else:
                        if study_start and study_end:
                            Researcher_education(user_id=request.user.id,institute=institute,
                                degree=degree,field_study=field_study,notes=notes,
                                study_start=study_start,study_stop=study_end,
                                ).save()
                            messages.success(request, (u"Education record was successfully created."))
                            return redirect("/buyer/edit/education")

                        else:
                            error_msg="Please select date ended field"

        else:
            form3 = ResearcherEducationForm()     

        return render_to_response('researcher/add-res-education.html',{'form3':form3,
            'form1':form1,
            'form2':form2,
            'form4':form4,
            'email':email,
            'fname':fname,
            'lname':lname,
            'org_name':org_name,
            'phone':phone,
            'user_desc':user_desc,
            'researcher_logo':researcher_logo,
            'education_info':education_info,
            'education_info3':education_info3,
            'contacts':contacts,
            'contacts1':contacts1,
            'contacts2':contacts2,
            'conformation_researcher':conformation_researcher,'error_msg':error_msg
            },
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")


@login_required
def edit_add_degree(request,degree_id):
    ''' Edit Researcher Degree View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        error_msg=""

        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()


        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse()   
        
        education_info3=Researcher_education.objects.filter(id=degree_id)

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
        if request.method == 'POST':
            form3 = ResearcherEducationForm(request.POST)
            study_end=""
            study_checked=""
            study_start=""
            if form3.is_valid():
                institute = request.POST.get('institute')
                degree = request.POST.get('degree')
                field_study = request.POST.get('field_study')
                notes = request.POST.get('notes')
                study_start=request.POST.get('study_start')
                study_end=request.POST.get('study_end')
                study_checked=request.POST.get('study_checked')

                if study_end  and not(study_start):                
                    error_msg="Please select date started field"
                else:
                    if study_checked:
                        Researcher_education.objects.filter(user_id=request.user.id,id =degree_id
                            ).update(institute=institute,
                         degree=degree,field_study=field_study,notes=notes,
                         study_start=study_start,study_stop=study_end,
                         )         
                    
                        messages.success(request, (u"Education record was successfully created."))
                        return redirect("/buyer/edit/education")

                    else:
                        if study_start and study_end:

                            Researcher_education.objects.filter(user_id=request.user.id,id =degree_id
                                ).update(institute=institute,
                             degree=degree,field_study=field_study,notes=notes,
                             study_start=study_start,study_stop=study_end,
                             )         

                            messages.success(request, (u"Education record was successfully updated."))
                            return redirect("/buyer/edit/education")

                        else:
                            error_msg="Please select date ended field"

        else:
            form3 = ResearcherEducationForm()        
        return render_to_response('researcher/edit-addeducation.html',{'form2':form2,
            'form1':form1, 'form3':form3, 'form4':form4,
            'conformation_researcher':conformation_researcher,
            'education_info3':education_info3,
            'contacts1':contacts1,
            'education_info':education_info,
            'contacts':contacts,
            'error_msg':error_msg},
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")

@login_required
def delete_degree(request,degree_id):
    ''' Delete Degree of researcher View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        success_msg ="Your Record deleted successfully"
        conformation_researcher="researcher"
        delete_education=Researcher_education.objects.filter(id=degree_id).delete()
        messages.success(request, (u"Education record was successfully deleted."))
        return redirect("/buyer/edit/education",msg=success_msg)
    else:
        return redirect("/logout/")

 

@login_required
def publications(request):
    ''' Researcher Publications View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        email=""
        fname=""
        lname=""
        org_name=""
        phone=""
        logo=""
        user_desc=""
        model_pic=""
        username=fname+lname
        researcher_logo=""

        researchr_info=Users.objects.filter(user_id=request.user.id)
        res_logo =Profilepic.objects.filter(
            user_id=request.user.id)
        for res in res_logo:
            researcher_logo=res.model_pic
        for res in researchr_info:
            email=res.email
            fname=res.fname
            lname=res.lname
            org_name=res.name_org
            phone=res.phone
        description =Researcher_more_info.objects.filter(user_id=request.user.id)
        for desc in description:
            user_desc=desc.desc

        if request.method == 'POST':
            form = EditResearcherForm(request.POST,request.FILES)
            if form.is_valid():
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                name1=request.POST.get('first_name')
                name2=request.POST.get('last_name')
                orgname=request.POST.get('companey')
                mobile=request.POST.get('phone_number')
                publication=request.POST.get('publications')            
                model_pic = form.cleaned_data['image']
                fullname=name1+name2
                User.objects.filter(id=request.user.id).update(email=mail_id,
                    username=fullname)
                Users.objects.filter(user_id=request.user.id).update(
                   email=mail_id,
                   fname=name1,
                   lname=name2,
                   name_org=orgname,
                   phone=mobile,
                   username=fullname
                   )
                
                if model_pic:               
                    Profilepic.objects.filter(user_id=request.user.id).delete()
                    Profilepic(user_id=request.user.id,model_pic=model_pic).save()
                    logo=Profilepic.objects.get(user_id=request.user.id).model_pic

                messages.success(request, (u"Your profile updated succesfully"))
                return redirect("/buyer/edit/basics/")

        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()

        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse()    
        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()
        publications_data =Researcher_publications.objects.filter(
            user_id=request.user.id).order_by('id').reverse()

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        paginator2 = Paginator(publications_data,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
            contacts2 = paginator2.page(page)

        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
            contacts2 = paginator2.page(1)

        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
            contacts2 = paginator2.page(paginator2.num_pages)

        return render_to_response('researcher/new_res_publications.html',
            {';form4':form4,
            'form1':form1,'form2':form2,'form3':form3,
            'email':email,
            'fname':fname,
            'lname':lname,
            'org_name':org_name,
            'phone':phone,
            'user_desc':user_desc,
            'researcher_logo':researcher_logo,
            'contacts':contacts,
            'contacts1':contacts1,
            'contacts2':contacts2,
            'education_info':education_info,
            'education_info3':education_info3,
            'conformation_researcher':conformation_researcher},
            context_instance=RequestContext(request)) 
    else:
        return redirect("/logout/")


@login_required
def add_publications(request):
    ''' Researcher Adding publications View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        result=""
        contacts_r=""
        error_msg=""
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()

        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse()
        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()
        publications_data =Researcher_publications.objects.filter(
            user_id=request.user.id).order_by('id').reverse()

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        paginator2 = Paginator(publications_data,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
            contacts2 = paginator2.page(page)

        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
            contacts2 = paginator2.page(1)

        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
            contacts2 = paginator2.page(paginator2.num_pages)

        email=""
        fname=""
        lname=""
        org_name=""
        phone=""
        logo=""
        user_desc=""
        model_pic=""
        username=fname+lname
        researcher_logo=""

        researchr_info=Users.objects.filter(user_id=request.user.id)
        res_logo =Profilepic.objects.filter(
            user_id=request.user.id)
        for res in res_logo:
            researcher_logo=res.model_pic
        for res in researchr_info:
            email=res.email
            fname=res.fname
            lname=res.lname
            org_name=res.name_org
            phone=res.phone
        description =Researcher_more_info.objects.filter(user_id=request.user.id)
        for desc in description:
            user_desc=desc.desc

        if request.method == 'POST':
            form = EditResearcherForm(request.POST,request.FILES)
            if form.is_valid():
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                name1=request.POST.get('first_name')
                name2=request.POST.get('last_name')
                orgname=request.POST.get('companey')
                mobile=request.POST.get('phone_number')
                publication=request.POST.get('publications')            
                model_pic = form.cleaned_data['image']
                fullname=name1+name2
                User.objects.filter(id=request.user.id).update(email=mail_id,
                    username=fullname)
                Users.objects.filter(user_id=request.user.id).update(
                   email=mail_id,
                   fname=name1,
                   lname=name2,
                   name_org=orgname,
                   phone=mobile,
                   username=fullname
                   )
                if model_pic:               
                    Profilepic.objects.filter(user_id=request.user.id).delete()
                    Profilepic(user_id=request.user.id,model_pic=model_pic).save()
                    logo=Profilepic.objects.get(user_id=request.user.id).model_pic

                messages.success(request, (u"Your profile updated succesfully"))
                return redirect("/buyer/edit/basics/")

        if request.method == 'POST':
            form4 = PublicationsForm(request.POST)
            if form4.is_valid():
                publications = request.POST.get('publications')
                result = Publications.objects.filter(title__contains=publications)
                if result:
                    paginator = Paginator(result,3)
                    page = request.GET.get('page')
                    try:
                        contacts_r = paginator.page(page)
                    except PageNotAnInteger:
                        contacts_r = paginator.page(1)
                    except EmptyPage:
                        contacts_r = paginator.page(paginator.num_pages)
                else:
                    error_msg="Sorry no records available"

                return render_to_response('researcher/add-publications.html',{'form4':form4,
                    'form1':form1, 'form2':form2, 'form3':form3,
                    'email':email,'fname':fname,'lname':lname,'org_name':org_name,
                    'phone':phone, 'user_desc':user_desc,'researcher_logo':researcher_logo,
                    'contacts':contacts,'contacts1':contacts1,'contacts2':contacts2,
                    'education_info':education_info,'education_info3':education_info3,
                    'conformation_researcher':conformation_researcher,
                    'contacts_r':contacts_r,'error_msg':error_msg},
                context_instance=RequestContext(request))
        else:
            form4 = PublicationsForm()
        return render_to_response('researcher/add-publications.html',{'form4':form4,
            'form1':form1,
            'form2':form2,
            'form3':form3,
            'result':result,
            'email':email,
            'fname':fname,
            'lname':lname,
            'org_name':org_name,
            'phone':phone,
            'user_desc':user_desc,
            'researcher_logo':researcher_logo,
            'contacts':contacts,'contacts1':contacts1,'contacts2':contacts2,
            'education_info':education_info,'education_info3':education_info3,
            'contacts_r':contacts_r,'conformation_researcher':conformation_researcher},
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")


@login_required
def store_publications(request,degree_id):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        publications = Publications.objects.filter(id=degree_id)
        for pub in publications:
            title=pub.title
            name=pub.scientist_name
            usedfor=pub.used_for
            Researcher_publications(user_id=request.user.id,title=title,
                scientist_name=name,used_for=usedfor).save()
        return redirect("/buyer/edit/publications/")
    else:
        return redirect("/logout/")

@login_required
def researcher_employment(request):
    ''' Researcher Employment View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm() 
        form4 = PublicationsForm()
        education_info=Researcher_emplyment.objects.filter(
                user_id=request.user.id).order_by('id').reverse()
        paginator = Paginator(education_info,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render_to_response('researcher/new_res_employment.html',{'education_info':education_info,
                'contacts':contacts,'conformation_researcher':conformation_researcher,
                'form1':form1,'form2':form2,'form3':form3,'form4':form4,
                },
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")


@login_required
def researcher_add_employment(request):
    ''' Researcher adding employment View '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        study_checked=""
        error_msg=""
        researchr_info=Users.objects.filter(user_id=request.user.id)
        email=""
        fname=""
        lname=""
        org_name=""
        phone=""
        logo=""
        user_desc=""
        model_pic=""
        username=fname+lname
        researcher_logo=""    
        res_logo =Profilepic.objects.filter(
            user_id=request.user.id)
        for res in res_logo:
            researcher_logo=res.model_pic
        for res in researchr_info:
            email=res.email
            fname=res.fname
            lname=res.lname
            org_name=res.name_org
            phone=res.phone
        description =Researcher_more_info.objects.filter(user_id=request.user.id)
        for desc in description:
            user_desc=desc.desc        

        education_info=Researcher_emplyment.objects.filter(
            user_id=request.user.id).order_by('id').reverse()
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm()
        form4 = PublicationsForm() 

        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()

        publications_data =Researcher_publications.objects.filter(
            user_id=request.user.id).order_by('id').reverse()

        paginator = Paginator(education_info,3)
        paginator1 = Paginator(education_info3,3)
        paginator2 = Paginator(publications_data,3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
            contacts2 = paginator2.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
            contacts2 = paginator2.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
            contacts2 = paginator2.page(paginator2.num_pages)


        ''' Edit Basics Form '''

        if request.method == 'POST':
            form = EditResearcherForm(request.POST,request.FILES)
            if form.is_valid():
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                name1=request.POST.get('first_name')
                name2=request.POST.get('last_name')
                orgname=request.POST.get('companey')
                mobile=request.POST.get('phone_number')
                publication=request.POST.get('publications')
                
                model_pic = form.cleaned_data['image']
                fullname=name1+name2
                User.objects.filter(id=request.user.id).update(email=mail_id,
                    username=fullname)
                Users.objects.filter(user_id=request.user.id).update(
                   email=mail_id,
                   fname=name1,
                   lname=name2,
                   name_org=orgname,
                   phone=mobile,
                   username=fullname
                   )
                
                if model_pic:               
                    Profilepic.objects.filter(user_id=request.user.id).delete()
                    Profilepic(user_id=request.user.id,model_pic=model_pic).save()
                    logo=Profilepic.objects.get(user_id=request.user.id).model_pic

                messages.success(request, (u"Your profile updated succesfully"))
                return redirect("/buyer/edit/basics/")

        if request.method == 'POST':
            form2 =ResearcherEmploymentForm(request.POST)
            study_end=""
            study_checked=""
            if form2.is_valid():
                employer = request.POST.get('employer')
                title = request.POST.get('title')
                notes = request.POST.get('notes')
                study_start=request.POST.get('study_start')
                study_end=request.POST.get('study_end')
                study_checked=request.POST.get('study_checked')

                if study_end  and not(study_start):                
                    error_msg="Please select year started field"

                else:
                    if study_checked:
                        Researcher_emplyment(user_id=request.user.id,employer=employer,
                            title=title,
                            notes=notes,study_start=study_start,study_stop=study_end,
                            study_continue=study_checked).save()
                        
                        messages.success(request, (u"Employment record was successfully created."))
                        return redirect("/buyer/edit/employment/")


                    else:
                        if study_start and study_end:                        
                            study_checked="no value"
                            Researcher_emplyment(user_id=request.user.id,employer=employer,
                                    title=title,
                                    notes=notes,study_start=study_start,study_stop=study_end,
                                study_continue="continuing").save()
                        
                            messages.success(request, (u"Employment record was successfully created."))
                            return redirect("/buyer/edit/employment/")
                        
                        else:
                            error_msg="Please select year ended field"

        else:
            form2 = ResearcherEmploymentForm()        
        return render_to_response('researcher/add-res-employment.html',{'form2':form2,
            'form1':form1,
            'form3':form3,
            'form4':form4,
            'email':email,
            'fname':fname,
            'lname':lname,
            'org_name':org_name,
            'phone':phone,
            'user_desc':user_desc,
            'researcher_logo':researcher_logo,
            'education_info':education_info,
            'conformation_researcher':conformation_researcher,
            'education_info3':education_info3,
            'contacts1':contacts1,
            'contacts':contacts,
            'contacts2':contacts2,
            'error_msg':error_msg
            },
            context_instance=RequestContext(request))

    else:
        return redirect("/logout/")

@login_required
def edit_add_employment(request,emp_id):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        error_msg=""
        form1 = EditPasswordForm()
        form2 = ResearcherEmploymentForm()
        form3 = ResearcherEducationForm()
        form4 = PublicationsForm() 
        education_info=Researcher_emplyment.objects.filter(id=emp_id)
        education_info3=Researcher_education.objects.filter(user_id=request.user.id).order_by('id').reverse()

        paginator1 = Paginator(education_info3,3)
        page = request.GET.get('page')
        try:
            # contacts = paginator.page(page)
            contacts1 = paginator1.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            # contacts = paginator.page(1)
            contacts1 = paginator1.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            # contacts = paginator.page(paginator.num_pages)
            contacts1 = paginator1.page(paginator1.num_pages)
        
        if request.method == 'POST':
            form2 = ResearcherEmploymentForm(request.POST)
            study_end=""
            study_checked=""
            if form2.is_valid():
                employer = request.POST.get('employer')
                title = request.POST.get('title')
                notes = request.POST.get('notes')
                study_start=request.POST.get('study_start')
                study_end=request.POST.get('study_end')
                study_checked=request.POST.get('study_checked')
                month_start=request.POST.get('month_start')
                month_end=request.POST.get('month_end')
                if study_end  and not(study_start):
                    error_msg="Please select year started field"

                else:
                    if study_checked:
                        Researcher_emplyment.objects.filter(user_id=request.user.id,
                            id =emp_id).update(employer=employer,title=title,notes=notes,
                            study_start=study_start,study_stop=study_end,
                            study_continue="continuing",month_start=month_start,
                            month_stop=month_end
                            )
                        messages.success(request, (u"Employment record was successfully updated."))
                        return redirect("/buyer/edit/employment")

                    else:
                        if study_start and study_end:
                            study_checked="no value"
                            Researcher_emplyment.objects.filter(user_id=request.user.id,
                                    id =emp_id).update(employer=employer,
                                    title=title,
                                    notes=notes,study_start=study_start,study_stop=study_end,
                                    study_continue="no-value",month_start=month_start,
                                    month_stop=month_end
                                )                            
                            messages.success(request, (u"Employment record was successfully updated."))
                            return redirect("/buyer/edit/employment")
                        else:
                            error_msg="Please select year ended field"
        else:
            form2 = ResearcherEmploymentForm() 
        return render_to_response('researcher/edit-add-employnment.html',{'form2':form2,
            'form1':form1, 'form3':form3, 'form4':form4,
            'conformation_researcher':conformation_researcher,
            'education_info':education_info,
            'education_info3':education_info3,
            'contacts1':contacts1,
            'error_msg':error_msg},
            context_instance=RequestContext(request))
    else:
        return redirect("/logout/")

@login_required
def delete_employment(request,emp_id):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        success_msg ="Your Record deleted successfully"
        conformation_researcher="researcher"
        delete_education=Researcher_emplyment.objects.filter(id=emp_id).delete()
        messages.success(request, (u"Employment record was successfully deleted."))
        return redirect("/buyer/edit/employment/",msg=success_msg)
    else:
        return redirect("/logout/")

@login_required
def delete_publications(request,emp_id):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        delete_education=Researcher_publications.objects.filter(id=emp_id).delete()
        messages.success(request, (u"Publication record was successfully deleted."))
        return redirect("/buyer/edit/publications/")
    else:
        return redirect("/logout/")

@login_required
def upload_profile_pic(request):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:
        conformation_researcher="researcher"
        researchr_info=Users.objects.filter(user_id=request.user.id)
        email=""
        fname=""
        lname=""
        org_name=""
        phone=""
        username=fname+lname
        for res in researchr_info:
            email=res.email
            fname=res.fname
            lname=res.lname
            org_name=res.name_org
            phone=res.phone

        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                name1=request.POST.get('first_name')
                name2=request.POST.get('last_name')
                orgname=request.POST.get('companey')
                mobile=request.POST.get('phone_number')
                publication=request.POST.get('publications')
                model_pic = form.cleaned_data['image']
                fullname=name1+name2
                User.objects.filter(id=request.user.id).update(email=mail_id,
                    username=fullname)
                Users.objects.filter(user_id=request.user.id).update(
                   email=mail_id,
                   fname=name1,
                   lname=name2,
                   name_org=orgname,
                   phone=mobile,
                   username=fullname
                   )
                Researcher_more_info.objects.filter(user_id=request.user.id).update(model_pic=model_pic)
                Profilepic(model_pic=model_pic).save()
                messages.success(request, (u"Your profile updated succesfully"))
                return redirect("/buyer/")
        else:
            form = ImageUploadForm()    

        return render_to_response('researcher/edit-researcher-basic.html',
            {'form':form,
            'email':email,
            'fname':fname,
            'lname':lname,
            'org_name':org_name,
            'phone':phone,
            'conformation_researcher':conformation_researcher,},
             context_instance=RequestContext(request))

    else:
        return redirect("/logout/")            



def search_publications(request,degree_id):
    return render_to_response('researcher/publication-search-results.html',
        context_instance=RequestContext(request))


def image_upload(request):
    if request.method == 'POST':    

        form = UploadImage(request.POST,request.FILES)       
        if form.is_valid():
            form.save()
        else:
            pass
    else:
        form=UploadImage()
    return render(request,'upload.html',{"form":form})

def lab_list_all(request):   
    return render(request,'store_front.html',{})

from django.http import JsonResponse
def searching_labs(request):
    lab_result=[]
    lab_count=[]
    lab_value=Lab.objects.all()
    for lab in lab_value:
        lab_result.append(lab.title) 
    return HttpResponse(lab_result)

def search_result(request):
    ''' Search Results View '''

    form=SearchingForm()
    expfilter=[]
    cityfilter=[]
    lab_name_filter=[]
    item = []
    title_search=[]
    caption_search=[]
    desc_search=[]
    search_results_list=[]
    lab_final_list=[]
    labservices_list=[]
    labservices_list_1=[]
    experiment_filter=LabServices.objects.all()
    for exp in experiment_filter:
        expfilter.append(exp.title)
    
    labfilter=Lab.objects.all().distinct()
    for lab in labfilter:
        cityfilter.append(lab.country)
        lab_name_filter.append(lab.title)
    cityset= set(cityfilter)
    city_filter_list=list(cityset)
    conformation_researcher=""
    conformation_lab=""
    roll_name = Userroles.objects.filter(user_id=request.user.id)
    name = ""
    for roll in roll_name:
        name = roll.roll_name
    if name == "lab":
        conformation_lab="conformation_lab"
    elif name == "researcher":
        conformation_researcher="researcher"
    else:
        pass
    if request.method == 'POST':        
        form = SearchingForm(request.POST)
        search_word = request.POST.get("search_word")
        request.session['text1'] =search_word
        lab_search_title=Lab.objects.filter(title__icontains=search_word)
        for tid in lab_search_title:
            search_results_list.append(tid.id)
        lab_search_caption=Lab.objects.filter(caption__icontains=search_word)
        
        for cid in lab_search_caption:
            search_results_list.append(cid.id)
        lab_search_country=Lab.objects.filter(country__icontains=search_word)
        for dscid in lab_search_country:
            search_results_list.append(dscid.id)
        resultset=set(search_results_list)
        search_lab_resultset=list(set(search_results_list))
        request.session["total_searchlabs_id"]=search_lab_resultset

        lab_country_lsit=list(set(search_results_list))

        lab_countries_list=[]

        countries=Lab.objects.filter(id__in=lab_country_lsit)
        country_list=[]
        for con in countries:
            country_list.append(con.country)
    
        country_set=list(set(country_list))
        country_set_1=filter(None, country_set)

        lab_final_list=[]
        for res in resultset:
            lab_list=[]
            lab_result=Lab.objects.filter(id=res)
            for l in lab_result:
                lab_list.append(l.title)
                lab_list.append(l.desc)
                lab_list.append(l.id)
                lab_final_list.append(lab_list)
        
        lab_services_title=LabServices.objects.filter(title__icontains=search_word)
        labservices_list=[]
        for lab in lab_services_title:
            service_list=[]
            service_list.append(lab.title)
            service_list.append(lab.desc)
            labservices_list.append(service_list)

        return render(request,'new_search.html',{'form':form,'lab_final_list':lab_final_list,
            'labservices_list':labservices_list,
            "conformation_researcher":conformation_researcher,
            "conformation_lab":conformation_lab,
            'expfilter':expfilter,
            'city_filter_list':city_filter_list,
            'lab_name_filter':lab_name_filter,
            'country_set_1':country_set_1})
    else:
        form=SearchingForm()

    return render(request,'new_search.html',{'form':form,'lab_final_list':lab_final_list,
            'labservices_list':labservices_list,
            "conformation_researcher":conformation_researcher,
            "conformation_lab":conformation_lab,
            'expfilter':expfilter,
            'city_filter_list':city_filter_list,
            'lab_name_filter':lab_name_filter,
            })


def search_keywords(request):
    keywords_list=[]

    keywords=Lab.objects.all()
    service_result=""
    lab_result=""
    for key in keywords:
        title=key.title
        caption=key.caption
        city=key.city
        keyword=title+','+caption+','+city        
        Labkeywords(lab_keywords=keyword).save()
    
    return HttpResponse("jgdhsgd")

def dynamic_searching(request):
    records_list=[]
    records=Lab.objects.all()
    lab_services=LabServices.objects.all()
    for re in records:
        title=re.title
        addition=title+'*'
        records_list.append(addition) 
    for lab in lab_services:
        title=lab.title
        addition=title+'*'
        records_list.append(addition) 
    # print "$$$$$$$$$$$$$$$$"    
    # print records_list
    # print "$$$$$$$$$$$$"   
    return HttpResponse(records_list)


def demo_publications(request):
    title="The victorivirus Helminthosporium victoriae virus 190S is the primary cause of disease/hypovirulence in its natural host and a heterologous host."
    scientist_name="Havens WM"
    used_for="heterologous host"

    for x in range(1,5):
        Publications(title=title,scientist_name=scientist_name,used_for=used_for).save()
    return HttpResponse("hiiiii")

def dashboard(request):   
    return render_to_response('new_researcher_dashboard.html',{},)


def search_filters(request):
    ''' Search Filters View '''

    search_word=request.session.get('text1')
    search_results_list=[]
    search_results_list_checked=[]
    lab_final_list=[]
    all_filter_labs=[]
    all_filter_services=[]
    if request.GET:        
        checkd_value_list=[]
        list_filter_labs = request.GET
        myDict = dict(list_filter_labs.iterlists())
       
        for key,value in  myDict.items():
            checkd_value_list=value   

        all_services=""
        all_lab=""
        all_ser_results_list=[]
        all_lab_results_list=[]

        lab_search_title=Lab.objects.filter(title__icontains=search_word)
        for tid in lab_search_title:
                search_results_list.append(tid.id)
        
        lab_search_title_filter=Lab.objects.filter(title__in=checkd_value_list)
        for tid in lab_search_title_filter:
                search_results_list_checked.append(tid.id)

        lab_search_caption=Lab.objects.filter(caption__icontains=search_word)
        for cid in lab_search_caption:
            search_results_list.append(cid.id)

        lab_search_caption_filter=Lab.objects.filter(caption__in=checkd_value_list)
        for cid in lab_search_caption_filter:
            search_results_list_checked.append(cid.id)

        lab_search_country=Lab.objects.filter(country__icontains=search_word)
        for dscid in lab_search_country:            
            search_results_list.append(dscid.id)

        lab_search_country_filter=Lab.objects.filter(country__in=checkd_value_list)
        for dscid in lab_search_country_filter:            
            search_results_list_checked.append(dscid.id) 
        
        resultset=list(set(search_results_list).intersection(search_results_list_checked))

        for res in resultset:
            lab_list=[]
            lab_result=Lab.objects.filter(id=res)
            for l in lab_result:
                lab_list.append(l.title)
                lab_list.append(l.desc)
                lab_list.append(l.id)
                lab_final_list.append(lab_list)

        labservices_list=[]
        service_list_checked=[]
        service_list_search=[]
        lab_services_title_filter=LabServices.objects.filter(title__in=checkd_value_list)
        for lab in lab_services_title_filter:
            service_list_checked.append(lab.id)

        lab_services_title=LabServices.objects.filter(title__icontains=search_word)
        for lab in lab_services_title:
            service_list_search.append(lab.id)

        service_final_list=[]
        all_filter_res=[]
        resultset_service=list(set(service_list_search).intersection(service_list_checked))

        for res in resultset_service:
            lab_service_list=[]
            lab_result=LabServices.objects.filter(id=res)
            for l in lab_result:
                lab_service_list.append(l.title)
                lab_service_list.append(l.desc)
                service_final_list.append(lab_service_list)

        for chk in checkd_value_list:
            if chk=="all-services":
                all_services=LabServices.objects.all()
                for all_ser in all_services:
                    all_ser_results_list.append(all_ser.id)
                   
            elif chk=="all-labs":                
                all_lab=Lab.objects.all()
                for lab in all_lab:
                    all_lab_results_list.append(lab.id)                  

            elif chk=="all-country":
                print 'all-country'
            else:
                pass

        resultset_all_lab_filter=list(set(search_results_list).intersection(all_lab_results_list))

        for res in resultset_all_lab_filter:
            lab_list=[]
            lab_result=Lab.objects.filter(id=res)
            for l in lab_result:
                lab_list.append(l.title)
                lab_list.append(l.desc)
                lab_list.append(l.id)
                all_filter_labs.append(lab_list)
            
        resultset_all_service_filter=list(set(service_list_search).intersection(all_ser_results_list))
        for res in resultset_all_service_filter:
            lab_service_list=[]
            lab_result=LabServices.objects.filter(id=res)
            for l in lab_result:
                lab_service_list.append(l.title)
                lab_service_list.append(l.desc)
                all_filter_services.append(lab_service_list)

        data="hai"
    else:
        lab_search_title=Lab.objects.filter(title__icontains=search_word)
        for tid in lab_search_title:
            search_results_list.append(tid.id)
        lab_search_caption=Lab.objects.filter(caption__icontains=search_word)
        
        for cid in lab_search_caption:
            search_results_list.append(cid.id)
        lab_search_country=Lab.objects.filter(country__icontains=search_word)
        for dscid in lab_search_country:
            search_results_list.append(dscid.id)
        resultset=set(search_results_list)

        service_final_list=[]
        for res in resultset:
            lab_list=[]
            lab_result=Lab.objects.filter(id=res)
            for l in lab_result:
                lab_list.append(l.title)
                lab_list.append(l.desc)
                lab_list.append(l.id)
                lab_final_list.append(lab_list)
        lab_services_title=LabServices.objects.filter(title__icontains=search_word)
        labservices_list=[]
        for lab in lab_services_title:
            service_list=[]
            service_list.append(lab.title)
            service_list.append(lab.desc)
            service_final_list.append(service_list)
    return render(request,'search_filters.html',
        {'service_final_list':service_final_list,
        'lab_final_list':lab_final_list,
        'all_filter_labs':all_filter_labs,
        'all_filter_services':all_filter_services,
        })
    

def store_front(request,store_id):
    conformation_lab="conformation_lab"
    lab_profle_info = Lab.objects.filter(id=store_id)
    lab_service_info =LabServices.objects.filter(lab_id=store_id)
    paginator = Paginator(lab_service_info,3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    lab_title = ""
    lab_name = ""
    lab_description=""
    orgtype=""
    ser_title=""
    ser_price=None
    ser_desc=""
    ser_url=""
    pic=""
    caption=""

    for lab_info in lab_profle_info:
        lab_title=lab_info.title
        lab_name=lab_info.orgname
        lab_description=lab_info.desc        
        orgtype=lab_info.typeorg
        city=lab_info.city
        state=lab_info.state
        country=lab_info.country
        pic=lab_info.model_pic
        caption=lab_info.caption

    for service in lab_service_info:
        ser_title=service.title
        ser_price=service.price
        ser_desc=service.desc
        ser_url=service.url

    return render_to_response('store_front.html',
        {
        'lab_title':lab_title,
        'lab_name':lab_name,
        'lab_description':lab_description,
        'orgtype':orgtype,
        'city':city,
        'state':state,
        'country':country,
        'pic':pic,
        "caption":caption,
        'ser_title':ser_title,
        'ser_price':ser_price,
        'ser_desc':ser_desc,
        'ser_url':ser_url,
        'lab_service_info':contacts,
        'contacts':contacts,
        'conformation_lab':conformation_lab,
        },
        context_instance=RequestContext(request))


def add_parentservices(request):
    parent_serivice=["Anatomical Force Microscopy",
    "Color Doppler Ultrasound",
    "Computed Tomography",
    "Confocal/Optical Microscopy",
    "Cryo Electron Microscopy",
    "Electron Microscopy",
    "Fluorescence Mediated Tomography",
    "In vivo Whole Tissue and Animal Imaging",
    "Light Sheet Fluorescence Microscopy",
    "Luminescence Imaging",
    "Microscopy",
    "Nano-Imaging",
    "Optical Birefringence Analysis",
    "Phase Contrast X-Ray Imaging",
    "Photo-Activated Localization Microscopy (PALM)",
    "SPECT-CT and PET-CT Imaging",
    "Single Molecule Localization Microscopy",
    "Scintigraphy",
    "Ultrasound Tomography",
    "X-Ray Microscopy and Nano-tomography (Nano-CT)",
    ]
    for i in parent_serivice:
        Service(pid=1,name=i).save()

    return HttpResponse("addd-services")


def book_detail(request):
    book1 = ""
    title =""
    description = ""
    try:
        books = Book.objects.get(id=1)
        title = books.title
        description = books.desc
        
    except Book.DoesNotExist:
        raise Http404
    return render_to_response('book1.html', 
        {'title': title, 'description':description},
        context_instance=RequestContext(request))

def sample(request):
    return render_to_response('sample.html')

@login_required
def labdashboard(request): 

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    print role_users
    for user in role_users:
        role_user=user.role_id
    print "provider_dash_board"
    print role_user
    if dashboard_type == "provider" and role_user == 2: 
        user = request.user        
        conformation_researcher=""              
        conformation_lab="conformation_lab"
        print "what is this user role"
        print conformation_researcher
        print "88888888888888888888888888888888"
        print conformation_lab
        return render_to_response("lab/lab-dashboard.html", {'user':user,
                'conformation_lab':conformation_lab,
                'conformation_researcher':conformation_researcher,})        
    else :        
        return redirect("/logout/")
    

@login_required
def new_lab_profile(request):
    ''' Lab Profile View '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    print role_users
    for user in role_users:
        role_user=user.role_id
    print "provider_profile"
    print role_user
    print request.user
    if dashboard_type == "provider" and role_user == 2:
        conformation_lab="conformation_lab"    
        labs=Lab.objects.filter(user_id=request.user.id)
        lab_id=None
        for lab in labs:
            lab_id=lab.id
        lab_profle_info = Lab.objects.filter(user_id=request.user.id)
        lab_service_info =LabServices.objects.filter(lab_id=lab_id)
        # paginator = Paginator(lab_service_info,3)
        # page = request.GET.get('page')
        # try:
        #     contacts = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer, deliver first page.
        #     contacts = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range (e.g. 9999), deliver last page of results.
        #     contacts = paginator.page(paginator.num_pages)

        lab_title = ""
        lab_name = ""
        lab_description=""
        orgtype=""
        ser_title=""
        ser_price=None
        ser_desc=""
        ser_url=""
        pic=""
        caption=""

        for lab_info in lab_profle_info:
            lab_title=lab_info.title
            lab_name=lab_info.orgname
            lab_description=lab_info.desc        
            orgtype=lab_info.typeorg
            city=lab_info.city
            state=lab_info.state
            country=lab_info.country
            pic=lab_info.model_pic
            caption=lab_info.caption

        for service in lab_service_info:
            ser_title=service.title
            ser_price=service.price
            ser_desc=service.desc
            ser_url=service.url


        form = AddLabservicesform()
       
        return render_to_response('lab/lab-profile.html',
            {
            'form1':form,
            'lab_title':lab_title,
            'lab_name':lab_name,
            'lab_description':lab_description,
            'orgtype':orgtype,
            'city':city,
            'state':state,
            'country':country,
            'pic':pic,
            "caption":caption,
            'ser_title':ser_title,
            'ser_price':ser_price,
            'ser_desc':ser_desc,
            'ser_url':ser_url,
            'services':lab_service_info,
            # 'contacts':contacts,
            'conformation_lab':conformation_lab,
            },
            context_instance=RequestContext(request)) 
    else :        
        return redirect("/logout/")
    

# def about(request):
#     '''About View'''

#     user = request.user
#     role_user=Userroles.objects.filter(user_id=request.user.id)
#     conformation_researcher=""
#     conformation_lab=""

#     for role in role_user:
#         usr_type=role.role_id

#         if usr_type==1:
#             conformation_researcher="researcher"
#         elif usr_type==2:
#             conformation_lab="conformation_lab"
#         else:
#             pass

#     about="about_page"
#     return render_to_response('new_about.html',{"about":about,"user":user,
#         'conformation_researcher':conformation_researcher,'conformation_lab':conformation_lab,},
#         context_instance=RequestContext(request))

def new_services(request):
    ''' Services View'''


    main_list=[]
    parent_id=[]
    main_list=[]

    parent=Services.objects.filter(pid=0)   

    for i in parent:
        parent_name=[]
        parent_name.append(i.name)
        parent_name.append(i.id)
        child=Services.objects.filter(pid=i.id)
        child_name=[]
        for j in child:
            child_name.append(j.name)
        parent_name.append(child_name)
        main_list.append(parent_name)    

    return render_to_response('new_services.html', 
        {'main_list':main_list,})

def new_services_result(request,pid):
    ''' Services Result View'''

    list_filter_labs = request.GET
    myDict = dict(list_filter_labs.iterlists())

    for key,value in  myDict.items():
        checkd_value_list=value        
    for i in checkd_value_list:
        lab_name= i

    main_list=[]
    parent_id=[]
    main_list=[]
    parent=Services.objects.filter(pid=pid)
    for i in parent:
        parent_name=[]
        parent_name.append(i.name)
        parent_name.append(i.id)         
        child=Services.objects.filter(pid=i.id)
        child_name=[]
        for j in child:
            child_name.append(j.name)
        parent_name.append(child_name)
        main_list.append(parent_name)
    max_list =[main_list,lab_name]
    json_encode(max_list)
    return HttpResponse(max_list[0],max_list[1])

def new_services_inner(request,p_id):
    ''' Sub Services View'''

    services="new_services"
    sub_services = Services.objects.filter(id=p_id)
    service_id = None
    
    for s in sub_services:        
        service_id = s.id  
    request.session["filter_services_id"]=service_id
    all_labs = Lab.objects.filter(service_id=s.id)
    
    lab1 = []
    for l in all_labs:        
        lab1.append(l)

    lab_details = []
    for l in lab1:
        lab_name = []
        lab_desc = []        
        lab_name.append(l.title)
        lab_name.append(l.desc)
        lab_details.append(lab_name)
        lab_details.append(lab_name)

    countries=Lab.objects.filter(service_id=service_id)
    country_list=[]
    for con in countries:
        country_list.append(con.country)

    country_set=list(set(country_list))
    country_set_1=filter(None, country_set)

    return render_to_response('new_services-inner.html', 
        {'services':services,'all_labs':all_labs,'p_id':p_id,
        'country_set_1':country_set_1,},
        context_instance=RequestContext(request))


def new_projects(request):
    ''' Projects View'''

    user = request.user
    role_user=Userroles.objects.filter(user_id=request.user.id)
    conformation_researcher=""
    conformation_lab=""
    for role in role_user:
        usr_type=role.role_id
        if usr_type==1:
            conformation_researcher="researcher"
        elif usr_type==2:
            conformation_lab="conformation_lab"
        else:
            pass
    # print user

    project="new_projects"

    if request.method == 'POST':
        form = SplRequestForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            university= request.POST.get('university')
            desc = request.POST.get('desc')
            phone_number=request.POST.get('phone_number')
            SplRequest(name=name,email =email,
               university=university,phone_number=phone_number,desc=desc).save()
            messages.success(request,(u"Request Received!Our Customer Service Team will Reach Out Servicehortly."))
            return redirect("/projects/")
    else:
        form = SplRequestForm()

    result=edit_about.objects.filter(id=3)
    project_result=None
    for i in result:
        print i.data
        project_result=i.data
    print "&&&&&&&&&&&&&&&&"*10
    print project_result
    print "&&&&&&&&&&&&&&&&"*10

    return render_to_response('new_projects.html',{"project_result":project_result,"project":project, "user":user,'form':form,
        'conformation_researcher':conformation_researcher,'conformation_lab':conformation_lab,},
        context_instance=RequestContext(request))

def show_services(request,ser_name):
    ''' Displaying Services View'''


    user = request.user
    role_user=Userroles.objects.filter(user_id=request.user.id)
    conformation_researcher=""
    conformation_lab=""
    for role in role_user:
        usr_type=role.role_id
        if usr_type==1:
            conformation_researcher="researcher"
        elif usr_type==2:
            conformation_lab="conformation_lab"
        else:
            pass

    services="new_services"
    expnd="expand_value"

    '''Left side Content'''

    main_list=[]
    parent_id=[]
    main_list=[]
    parent=Services.objects.filter(pid=0)   
    for i in parent:
        parent_name=[]
        parent_name.append(i.name)
        parent_name.append(i.id)        
        child=Services.objects.filter(pid=i.id)
        child_name=[]
        for j in child:
            child_name.append(j.name)
        parent_name.append(child_name)
        main_list.append(parent_name)

    '''For Right Content'''

    par_ser_list=[]
    services =Services.objects.filter(name=ser_name)
    for ser in services:
        parent_name=[]
        parent_name.append(ser.name)
        child_service=Services.objects.filter(pid=ser.id)
        child_name=[]
        for ser_1 in child_service:
            child_id=[]            
            child_id.append(ser_1.id)
            child_id.append(ser_1.name)
            child_name.append(child_id)
        parent_name.append(child_name)
        par_ser_list.append(parent_name)

    return render_to_response('new_services.html', 
        {'par_ser_list':par_ser_list,
        'main_list':main_list,'ser_name':ser_name,
        "services":services,"user":user,
        'conformation_researcher':conformation_researcher,
        'conformation_lab':conformation_lab,},
         context_instance=RequestContext(request))

def new_lab_messages(request):

    # return HttpResponse("this is about messages")
    return render_to_response('lab/new_messages.html')

def new_contactus(request):
    ''' Contact Us View'''

    user = request.user
    role_user=Userroles.objects.filter(user_id=request.user.id)
    conformation_researcher=""
    conformation_lab=""
    for role in role_user:
        usr_type=role.role_id
        if usr_type==1:
            conformation_researcher="researcher"
        elif usr_type==2:
            conformation_lab="conformation_lab"
        else:
            pass

    contact="contact"
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject= request.POST.get('subject')
            message = request.POST.get('message')

            ContactUS(name=name,email =email,
               subject=subject,messages=message).save()
            messages.success(request,(u"Inquiry Received!Our Customer Service Team will reach out shortly."))
            return redirect("/support/")
    else:
        form = ContactUsForm()

    return render_to_response('contact.html',{"contact":contact,"user":user,'form':form,
        'conformation_researcher':conformation_researcher,'conformation_lab':conformation_lab,},
        context_instance=RequestContext(request)) 

def new_consulting(request):
    ''' Consulting View'''

    user = request.user
    role_user=Userroles.objects.filter(user_id=request.user.id)
    conformation_researcher=""
    conformation_lab=""
    for role in role_user:
        usr_type=role.role_id
        if usr_type==1:
            conformation_researcher="researcher"
        elif usr_type==2:
            conformation_lab="conformation_lab"
        else:
            pass

    consult="consulting"
    result=edit_about.objects.filter(id=2)
    consult_result=None
    for i in result:
        print i.data
        consult_result=i.data
    print "&&&&&&&&&&&&&&&&"*10
    print consult_result
    print "&&&&&&&&&&&&&&&&"*10
    return render_to_response('consulting.html',{"consult_result":consult_result,"consult":consult, "user":user,
        'conformation_researcher':conformation_researcher,'conformation_lab':conformation_lab,},
        context_instance=RequestContext(request))

def send_quote(request,lab_id,serv_id):
    ''' Send Quote View'''

    error_message=""
    service_name=""
    if serv_id: 
        service_name=Services.objects.get(id=serv_id).name
    labname=Lab.objects.filter(id=lab_id)
    lab_title=""
    image=""
    city=""
    for lname in labname:
        lab_title=lname.title
        image=lname.model_pic
        city=lname.city
    services_list=[]
    services=LabServices.objects.filter(lab_id=lab_id)
    for ser in services:
        services_list.append(ser.title)
    conformation_researcher="researcher"

    if request.user.id:
        if request.method == 'POST':            
            form = SendQuote_loggedinForm(request.POST,request.FILES)
            if form.is_valid():
                userid=request.user.id
                email=request.user.email
                user_name=request.user.username                
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                send_file = form.cleaned_data['send_file']
                service=request.POST.get('service')                
                serviceid=None

                Quotes(researcher_id=userid,lab_id=lab_id,
                        service_id=serv_id,desc=desc,status_id=1,
                        researcher_name=email,service_name=service_name).save()

                quoteid=Quotes.objects.latest('created_at').id
                servid=str(quoteid).zfill(4)
                Quotes.objects.filter(id=quoteid).update(sid=servid)
                Quote_files(quote_id=quoteid,filename=send_file).save()
                Quote_status(quote_id=quoteid,name="Pending",
                    description="no response from buyer",status_id=1).save()
                return HttpResponseRedirect ('/send-quote/thanks/')
        else:
            form = SendQuote_loggedinForm()
    else:        
        if request.method == 'POST':
            form = SendQuote_not_loginForm(request.POST,request.FILES)
            if form.is_valid():
                email_create=request.POST.get("email")
                password1_create=request.POST.get("password1")
                password2_create=request.POST.get("password2")
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                send_file = form.cleaned_data['send_file']
                service=request.POST.get('service')
                if password1_create==password2_create:
                    email_check=User.objects.filter(email=email_create)
                    if email_check:
                        error_message="Email address already exists"
                        
                    else:
                        user = User.objects.create_user(email_create,email_create, password1_create)
                        
                        new_user_id=None
                        new_user_name=""
                        user_info=User.objects.filter(email= email_create)
                        for usr in user_info:
                            new_user_id=usr.id
                            new_user_name=usr.username
                            
                        Quotes(researcher_id=new_user_id,lab_id=lab_id,
                                service_id=serv_id,desc=desc,status_id=1,
                                researcher_name=new_user_name,service_name=service_name).save()

                        quoteid=Quotes.objects.latest('created_at').id
                        servid=str(quoteid).zfill(4)

                        Quotes.objects.filter(id=quoteid).update(sid=servid)
                        Quote_files(quote_id=quoteid,filename=send_file).save()
                        Quote_status(quote_id=quoteid,name="Pending",
                            description="no response from buyer",status_id=1).save()
                        return HttpResponseRedirect ('/send-quote/thanks/')
                        # return redirect('/provider/quotes/')
                else:
                    error_message="Password and Confirm Passwords are doesn't match"

        else:
            form = SendQuote_not_loginForm()

    return render_to_response('send-quote.html',{'form':form,
        'services_list':services_list,
        'service_name':service_name,        
        'lab_title':lab_title,
        'image':image,
        'city':city,
        'error_message':error_message,
        },
        context_instance=RequestContext(request))


@login_required
def new_lab_quotes(request):
    ''' Lab Quotes View'''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    print role_users
    for user in role_users:
        role_user=user.role_id
    print "provider_quotes"
    print role_user
    if dashboard_type == "provider" and role_user == 2:
        user = request.user    
        userid=request.user.id
        labID=None
        labdetails = Lab.objects.filter(user_id=userid)
        for lab in labdetails:
            labID=lab.id        
        if labID:
            display_list=[]
            display_quotes=Quotes.objects.filter(lab_id=labID)
            return render_to_response('lab/lab-quotes.html',{'display_quotes':display_quotes, 'user':user,})
        else:
            return render_to_response('lab/lab-quotes.html',)
    else :       
        return redirect("/logout/")


@login_required
def view_quote(request,id):
    '''Particular Quote Details View'''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        message_list = Message.objects.inbox_for_provider(request.user)
        user = request.user
        userid=request.user.id
        labID=None
        labdetails = Lab.objects.filter(user_id=userid)
        for lab in labdetails:
            labID=lab.id        
        quote_desription=""
        quote_id=""
        sid=""
        title=""
        name=""
        date=""
        status_name=""
        viewquote=Quotes.objects.filter(id=id)
        for quote in viewquote:
            sid=quote.sid
            title=quote.service_name
            name=quote.researcher_name
            date=quote.created_at
            quote_id=quote.id
            statusid=quote.status_id
            if statusid==1:
                status_name="Pending"
        for qid in viewquote:
            quote_desription=qid.desc
        download_file=""        
        download=Quote_files.objects.filter(quote_id=quote_id)
        for down in download:
            download_file=down.filename
        download_file1=str(download_file).replace('quotes/','')
        display_quotes=Quotes.objects.filter(lab_id=labID)
        paginator = Paginator(display_quotes, 4)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        
        return render_to_response('lab/lab-quote-desc.html',{'quote_desription':quote_desription,
            'title':title,
            'sid':sid,
            'date':date,
            'name':name,
            'quote_id':quote_id,
            'display_quotes':display_quotes,
            'status_name':status_name,
            'download_file':download_file1,
            'user':user,'message_list':message_list,})
    else :       
        return redirect("/logout/")

def multiquote(request,serv_id):
    
    multiquote_labs_list=request.POST.getlist('multiquote')
    request.session["lab_list"]=multiquote_labs_list

    if multiquote_labs_list:
        return redirect("/multiquote-res/%s/" %serv_id)     
    else:
        messages.error(request,(u"Please Select Atleast One Lab For Multi Quote Request."))
        return redirect('/services/sub/%s/'%(serv_id))


def Multiquote_researcher(request,serv_id):
    ''' Sending Multi Quote View'''
   
    multi_lab_list=request.session["lab_list"]
    error_message=""
    service_name=""
    if serv_id: 
        service_name=Services.objects.get(id=serv_id).name
    conformation_researcher="researcher"

    if request.user.id:        
        if request.method == 'POST':            
            form = SendQuote_loggedinForm(request.POST,request.FILES)
            if form.is_valid():
                userid=request.user.id
                email=request.user.email
                user_name=request.user.username                
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                send_file = form.cleaned_data['send_file']
                service=request.POST.get('service')               
                serviceid=None
                for multi in request.session["lab_list"]:                    
                    Quotes(researcher_id=userid,lab_id=multi,
                            service_id=serv_id,desc=desc,status_id=1,
                            researcher_name=email,service_name=service_name).save()
                        
                    quoteid=Quotes.objects.latest('created_at').id
                    servid=str(quoteid).zfill(4)
                    Quotes.objects.filter(id=quoteid).update(sid=servid)
                    Quote_files(quote_id=quoteid,filename=send_file).save()                    
                return HttpResponseRedirect ('/send-quote/thanks/')                
        else:
            form = SendQuote_loggedinForm()

    else:        
        if request.method == 'POST':
            form = SendQuote_not_loginForm(request.POST,request.FILES)
            if form.is_valid():
                email_create=request.POST.get("email")
                password1_create=request.POST.get("password1")
                password2_create=request.POST.get("password2")
                desc = request.POST.get('Desc')
                mail_id=request.POST.get('email')
                send_file = form.cleaned_data['send_file']
                service=request.POST.get('service')
                if password1_create==password2_create:
                    email_check=User.objects.filter(email=email_create)
                    if email_check:
                        error_message="Email address already exists"
                        print error_message
                    else:
                        user = User.objects.create_user(email_create,email_create, password1_create)
                        new_user_id=None
                        new_user_name=""
                        user_info=User.objects.filter(email= email_create)
                        for usr in user_info:
                            new_user_id=usr.id
                            new_user_name=usr.username

                        for multi in multi_lab_list:                         
                            Quotes(researcher_id=new_user_id,lab_id=multi,
                                    service_id=serv_id,desc=desc,status_id=1,
                                    researcher_name=new_user_name,service_name=service_name).save()

                            quoteid=Quotes.objects.latest('created_at').id
                            servid=str(quoteid).zfill(4)

                            Quotes.objects.filter(id=quoteid).update(sid=servid)
                            Quote_files(quote_id=quoteid,filename=send_file).save()

                        return HttpResponseRedirect ('/send-quote/thanks/')
                        return redirect('/provider/quotes/')
                else:
                    error_message="Password and Confirm Passwords are doesn't match"

        else:
            form = SendQuote_not_loginForm()

    return render_to_response('multiquote.html',{'form':form,
        'service_name':service_name,
        'serv_id':serv_id,        
        'error_message':error_message,
        },
        context_instance=RequestContext(request))
    
    
@login_required
def quote_status_filter(request):
    ''' Quote Status View'''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        filter_data=request.GET
        quote_status_id=None
        value_filter=""
        userid=request.user.id
        labID=None
        labdetails = Lab.objects.filter(user_id=userid)
        for lab in labdetails:
            labID=lab.id
        quote_filters=[]

        for key,value in filter_data.items():
            value_filter=key
            if value_filter=="Pending":
                quote_status_id=1
            elif value_filter=="Declined":
                quote_status_id=2
            elif value_filter=="Active-Pending":
                 quote_status_id=3

            elif value_filter=="Active":
                 quote_status_id=4

            else:
                pass

        if value_filter=="All":
            quote_filters=Quotes.objects.filter(lab_id=labID)

        else:
            quote_filters=Quotes.objects.filter(status_id=quote_status_id,lab_id=labID)      


        return render_to_response('lab/quote_filter_result.html',{'quote_filters':quote_filters},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")    
    

@login_required
def lab_send_quote(request,qut_id):
    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        labname=Lab.objects.filter(user_id=request.user.id)
        image=""
        name=""
        city=""
        for lname in labname:
            image=lname.model_pic
            name=lname.title
            city=lname.city
       
        quote_info=Quotes.objects.filter(id=qut_id)
        if request.method == 'POST':
            form = LabQuoteForm(request.POST,request.FILES)
            if form.is_valid():
                ser_price = request.POST.get('service_price')
                ser_duration=request.POST.get('duration')
                ser_notes=request.POST.get('notes')
                send_file = form.cleaned_data['send_file']
                Quotes.objects.filter(id=qut_id).update(price=ser_price,duration=ser_duration,notes=ser_notes,
                    sent_by="Lab")
                
                if send_file:
                    Quote_files(quote_id=qut_id,filename=send_file,sent_by="Lab").save()
                messages.success(request,(u"Thanks For Sending Quote."))
                return redirect('/provider-quote/%s/'%qut_id)
        else:
            form = LabQuoteForm()
        return render_to_response('lab/lab-quote-form.html',{'form':form,
            'image':image,
            'name':name,
            'city':city,
            'quote_info':quote_info,
            },
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")    
    
def send_quote_thanks(request):        
    ''' Thank You Page '''

    return render_to_response('thanks.html', 
        context_instance=RequestContext(request)) 


def service_filters(request):
    ''' Services Filters View'''

    serviceID=request.session["filter_services_id"]
    checkd_value_list=[]
    frst_filtr_rslt_lst=[]
    list_filter_labs = request.GET
    myDict = dict(list_filter_labs.iterlists())
    fitr_results=[]

    for key,value in  myDict.items():
        checkd_value_list.append(value)

    size_checkd_value_list=len(checkd_value_list)

    if size_checkd_value_list==1:
        ser_search_country=Lab.objects.filter(country__in=checkd_value_list[0],service_id=serviceID)
        for ser_country in ser_search_country:
            frst_filtr_rslt_lst.append(ser_country.id)
        ser_search_typeorg=Lab.objects.filter(typeorg__in=checkd_value_list[0],service_id=serviceID)
        for ser_org in ser_search_typeorg:
            frst_filtr_rslt_lst.append(ser_org.id)
        fitr_results=Lab.objects.filter(id__in=frst_filtr_rslt_lst)       

    elif size_checkd_value_list==2:        
        ser_search_country=Lab.objects.filter(country__in=checkd_value_list[0],typeorg__in=checkd_value_list[1],
            service_id=serviceID)
        for ser_country in ser_search_country:
            frst_filtr_rslt_lst.append(ser_country.id)
        ser_search_typorg=Lab.objects.filter(country__in=checkd_value_list[1],typeorg__in=checkd_value_list[0],
            service_id=serviceID)
        for ser_org in ser_search_typorg:
            frst_filtr_rslt_lst.append(ser_org.id)

        fitr_results=Lab.objects.filter(id__in=frst_filtr_rslt_lst)
    else:   
        fitr_results=Lab.objects.filter(service_id=serviceID)    

    return render_to_response('service-filter.html',{'fitr_results':fitr_results,
     'serviceID':serviceID },
        context_instance=RequestContext(request))

@login_required
def new_res_quotes(request):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    user = request.user
    print "res-quotes"
    print user.id
    print user
    print request.user
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    print role_user
    if dashboard_type == "buyer" and role_user == 1:   
        print "after if condition"
        print user
        print type(user)
        print user.user_id
        user_email=User.objects.get(id=user.user_id)
        print user_email

        # for u in user:
        #     print"$$$$"
        #     print u   
        conformation_researcher="researcher"
        # user = request.user        
        display_res_quotes=Quotes.objects.filter(researcher_id=user.user_id,
            sent_by="Lab")
        print display_res_quotes
        if display_res_quotes:
            print "display_quotes"
            return render_to_response('researcher/new_res_quotes.html',
                {'display_quotes':display_res_quotes,"conformation_researcher":conformation_researcher,
                'user':user_email,})
        else:
            print "else"
            print user_email
            # return render_to_response('researcher/new_res_quotes.html',
            #     {'display_quotes':display_res_quotes,"conformation_researcher":conformation_researcher,
            #     'user':user_email,})
            return render_to_response('researcher/new_res_quotes.html',
                {'display_quotes':display_res_quotes,"conformation_researcher":conformation_researcher,
                'user':user_email,})
    else :       
        return redirect("/logout/") 


@login_required
def res_view_quote(request,id):
    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1:  
        message_list = Message.objects.inbox_for(request.user)
        user = request.user
        userid=request.user.id
        labID=None
        labdetails = Lab.objects.filter(user_id=userid)
        for lab in labdetails:
            labID=lab.id

        quote_desription=""
        quote_id=""
        sid=""
        title=""
        name=""
        date=""
        status_name=""
        price=""
        duration=""
        lab_name=""
        labID=None
        viewquote=Quotes.objects.filter(id=id)
        
        for quote in viewquote:
            sid=quote.sid
            title=quote.service_name
            name=quote.researcher_name
            date=quote.created_at
            quote_id=quote.id
            statusid=quote.status_id
            price=quote.price
            duration=quote.duration
            labID=quote.lab_id
        labinfo=Lab.objects.filter(id=labID)
        for lab in labinfo:
            lab_name=lab.title

            if statusid==1:
                status_name="Pending"

        for qid in viewquote:
            quote_desription=qid.desc

        download_file=""    
        download=Quote_files.objects.filter(quote_id=quote_id)

        for down in download:
            download_file=down.filename
        download_file1=str(download_file).replace('quotes/','')
        display_quotes=Quotes.objects.filter(researcher_id=request.user.id,sent_by="Lab")
        
        return render_to_response('researcher/res_quote_desc_1.html',{'quote_desription':quote_desription,
            'title':title,
            'sid':sid,
            'date':date,
            'name':name,
            'quote_id':quote_id,
            'display_quotes':display_quotes,
            'status_name':status_name,
            'download_file':download_file1,
            'display_quotes':display_quotes,
            'lab_name':lab_name,
            'price':price,
            'duration':duration,
            'user':user,
            'message_list':message_list,})
    else :       
        return redirect("/logout/") 


def breadcroomb(request):   
    
    breadcrumb_value=""
    req_value=request.GET
    for key,value in  req_value.items():
        breadcrumb_value=key
    
    return render_to_response('breadcrumb.html',{'breadcrumb_value':breadcrumb_value},
        context_instance=RequestContext(request))


@login_required
def inbox(request):    
    '''
    handles the index page when user is not logged in
    @request  request object    '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1: 
        user = request.user
        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""
        for role in role_user:
            usr_type=role.role_id
            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass

        #for Inbox
        message_list = Message.objects.inbox_for(request.user)
        index = Message.objects.filter(recipient=request.user).count()
        no_of_unread = message_list.filter(read_at=None).count()    
        
        #for Outbox
        sentmessage_list = Message.objects.outbox_for(request.user)    

        return render_to_response('messages/messages_inbox.html',
                           {'message_list': message_list,
                            'sentmessage_list': sentmessage_list,
                            'index': index, 'unread_count': no_of_unread,
                            "user":user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,},
                            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")

@login_required
def buyer_msg_view(request, msg_id,form_class=ComposeForm,
    quote_helper=format_quote,subject_template=_(u"Re: %(subject)s")):   

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1: 
        user = request.user
        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""
        for role in role_user:
            usr_type=role.role_id
            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        # user = request.user
        now = timezone.now()
        message_id=msg_id
        message = get_object_or_404(Message, id=message_id)
        if (message.sender != user) and (message.recipient != user):
            raise Http404
        if message.read_at is None and message.recipient == user:
            message.read_at = now
            message.save() 
        # context = {'message': message, 'reply_form': None}  
        if message.recipient == user:
            form = form_class(initial={
                'body': quote_helper(message.sender, message.body),
                'subject': subject_template % {'subject': message.subject},
                'recipient': [message.sender,]
                })
        # context['reply_form'] = form

        return render_to_response('messages/messages_view.html',
            {'message' : message,"user":user,'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")

@login_required
def compose(request, recipient=None, form_class=ComposeForm, 
    recipient_filter=None):
    ''' composing messages for contact form  '''

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    body = ""
    if dashboard_type == "buyer" and role_user == 1: 

        error_message = ""
        present_user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass

        body_data = request.GET
        body = ""
        for key, value in body_data.items():        
            body1=str(key)
            request.session["body_value"]=body1
            body = body1
        body = request.session.get('body_value')

        print "body value"
        print body
        body1 = str(body)
        users = Userroles.objects.filter(user_id=request.user.id)
        value = 0
        rollname = ""
        users_list = []
        for user in users:
            rollname = user.roll_name   
        print rollname
        if rollname == "researcher":        
            labusers = Userroles.objects.filter(roll_name="lab")
            list1 = []
            for i in labusers:
                user1 = User.objects.filter(id=i.user_id)
                list2=[]
                for j in user1:
                    users_list.append(j.username)

        recipient_list = []
        if request.method == "POST":
            form = form_class(request.POST, recipient_filter=recipient_filter)
            id1 = request.POST.get('recipient')
            print id1
            print type(id1)


            try :
                if id1 :           
                    index1 = list(id1)
                    digit =  id1.split(",")            
                    for l in digit :
                        print l
                        ll = int(l)
                        print ll
                        emails = users_list[ll]               
                        try :
                            em_obj = User.objects.get(username=emails)
                        except Exception:
                            pass                
                        if em_obj:                    
                            recipient_list.append(em_obj)
                        else:                    
                            pass            

                    if form.is_valid():                
                        current_user = User.objects.get(id=request.user.id)

                        if recipient_list:
                            for res in recipient_list:
                                print "resdafdsfsad"
                                print res
                                form.save(sender=current_user,recpt=res,body1=body1)
                        else:
                            pass
                        messages.info(request, (u"Message successfully sent."))            
                        return HttpResponseRedirect('/buyer/messages/inbox')
                else:
                    error_message = "Please fill the Recipient Email"
            except Exception:
                print "except block"
                email = User.objects.get(email=id1)
                recipient_list.append(email)

                if form.is_valid():                
                    current_user = User.objects.get(id=request.user.id)
                    if recipient_list:
                        for res in recipient_list:                            
                            form.save(sender=current_user,recpt=res,body1=body1)
                    else:
                        pass
                    messages.info(request, (u"Message successfully sent."))            
                    return HttpResponseRedirect('/buyer/messages/inbox')

      
        else:
            form = form_class()
            if recipient is not None:
                recipients = [u for u in UserProfile.objects.filter(
                    **{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
                form.fields['recipient'].initial = recipients

        return render_to_response('messages/messages_compose.html', {'form': form,
            "user":present_user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
            'error_message':error_message,},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")


@login_required
def reply(request, msg_id, form_class=ComposeForm, success_url=None,
        recipient_filter=None):
    ''' reply to the contact messages''' 

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1: 

        user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass

        message_id = msg_id
        parent = get_object_or_404(Message, id=message_id)
        messages = Message.objects.filter(id=message_id)
        reply_recipient = ""
        for msg in messages:
            print "reply messages"
            print msg.sender_id
            re = User.objects.get(id=msg.sender_id).email
            print re
            print msg.recipient
            reply_recipient = re

        if parent.sender != request.user and parent.recipient != request.user:
            raise Http404
        if request.method == "POST":
            sender = request.user
            form = form_class(request.POST, recipient_filter=recipient_filter)
            if form.is_valid():
                form.save(sender=request.user, parent_msg=parent)
                messages.info(request, (u"Message successfully sent."))

                if success_url is None:
                    success_url = reverse('inbox')
                return HttpResponseRedirect(success_url)
        else:
            form = form_class(initial={
                'subject': parent.subject,
                'recipient': parent.sender
                })
        return render_to_response('messages/messages_reply.html', {'form': form,
            "user":user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
            'recipient':reply_recipient,},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")


@login_required
def outbox(request):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """
    
    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1: 

        user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        message_list = Message.objects.outbox_for(request.user)
       

        return render_to_response('messages/messages_outbox.html', {
            'message_list': message_list,
            "user":user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
        }, context_instance=RequestContext(request))

    else :       
        return redirect("/logout/")

@login_required
def trash(request):

    dashboard_type = "buyer"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "buyer" and role_user == 1: 
        user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        message_list=Message.objects.filter(buyer_display_status=1)
        return render_to_response('messages/messages_trash.html', {
            "user":user,
            'message_list':message_list,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
        }, context_instance=RequestContext(request))

    else :       
        return redirect("/logout/")

@login_required
def provider_inbox(request):    
    '''
    handles the index page when user is not logged in
    @request  request object    '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    print role_users
    for user in role_users:
        role_user=user.role_id
    print "provider_profile"
    print role_user
    print request.user
    if dashboard_type == "provider" and role_user == 2:
        user = request.user
        print "user"
        print request.user
        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id
            print "provider role id"

            print usr_type
            print "-----------------------------"

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        #for Inbox
        message_list = Message.objects.inbox_for_provider(request.user)
        # print message_list
        index = Message.objects.filter(recipient=request.user).count()
        no_of_unread = message_list.filter(read_at=None).count()    
        
        #for Outbox
        sentmessage_list = Message.objects.outbox_for(request.user)    

        return render_to_response('messages/provider_messages_inbox.html',
                           {'provider_message_list': message_list,
                            'sentmessage_list': sentmessage_list,
                            'index': index, 'unread_count': no_of_unread,
                            "user":user,
                            'conformation_researcher':conformation_researcher,
                            'conformation_lab':conformation_lab,},
                            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")



@login_required
def provider_msg_view(request, msg_id,form_class=ComposeForm,
    quote_helper=format_quote,subject_template=_(u"Re: %(subject)s")):   

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2: 
        user = request.user
        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""
        for role in role_user:
            usr_type=role.role_id
            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        # user = request.user
        now = timezone.now()
        message_id=msg_id
        message = get_object_or_404(Message, id=message_id)
        if (message.sender != user) and (message.recipient != user):
            raise Http404
        if message.read_at is None and message.recipient == user:
            message.read_at = now
            message.save() 
        # context = {'message': message, 'reply_form': None}  
        if message.recipient == user:
            form = form_class(initial={
                'body': quote_helper(message.sender, message.body),
                'subject': subject_template % {'subject': message.subject},
                'recipient': [message.sender,]
                })
        # context['reply_form'] = form

        return render_to_response('messages/provider_messages_view.html',
            {'message' : message,"user":user,'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")



@login_required
def provider_trash(request):    
    '''
    handles the index page when user is not logged in
    @request  request object    '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        #for Inbox
        message_list=Message.objects.filter(provider_display_status=1)
        # message_list = Message.objects.inbox_for(request.user)
        # index = Message.objects.filter(recipient=request.user).count()
        # no_of_unread = message_list.filter(read_at=None).count()    
        
        # #for Outbox
        # sentmessage_list = Message.objects.outbox_for(request.user)    

        return render_to_response('messages/provider_messages_trash.html',
                           {
                            "user":user,
                            'message_list':message_list,
                            'conformation_researcher':conformation_researcher,
                            'conformation_lab':conformation_lab,},
                            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")

@login_required
def provider_compose(request, recipient=None, form_class=ComposeForm, 
    recipient_filter=None):
    ''' composing messages for contact form  '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        error_message = ""
        present_user = request.user

        role_user1=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user1:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass

        body_data = request.GET
        body = ""
        for key, value in body_data.items():        
            body1=str(key)
            request.session["body_value"]=body1
            body = body1
        body = request.session.get('body_value')

        print "body value"
        print body
        body1 = str(body)
        current_users = Userroles.objects.filter(user_id=request.user.id)
        # value = 0
        rollname = ""
        users_list = []
        for user1 in current_users:
            rollname = user1.roll_name   
        print "((((((((("
        print rollname
        if rollname == "lab":        
            buyers = Userroles.objects.filter(roll_name="researcher")
            list1 = []
            print "buyers"
            print buyers
            for i in buyers:
                print i
                user1 = User.objects.filter(id=i.user_id)
                list2=[]
                for j in user1:
                    users_list.append(j.username)

        recipient_list = []
        if request.method == "POST":
            form = form_class(request.POST, recipient_filter=recipient_filter)
            id1 = request.POST.get('recipient')
            print id1
            print type(id1)


            try :
                print "try block"
                if id1:  
                    print "if id1"        
                    index1 = list(id1)
                    print index1
                    digit =  id1.split(",") 
                    print "digit"           
                    print type(digit)
                    print digit
                    print users_list
                    for l in digit :
                        print "in digit for loop"
                        print l
                        ll = int(l)
                        print ll
                        emails = users_list[ll] 
                        print "emails"              
                        print emails
                        
                        try :
                            em_obj = User.objects.get(username=emails)
                        except Exception:
                            pass                
                        if em_obj:                    
                            recipient_list.append(em_obj)
                        else:                    
                            pass            

                    if form.is_valid():                
                        current_user = User.objects.get(id=request.user.id)

                        if recipient_list:
                            for res in recipient_list:
                                print "provider"
                                print res
                                form.save(sender=current_user,recpt=res,body1=body1)
                        else:
                            pass
                        messages.info(request, (u"Message successfully sent."))            
                        return HttpResponseRedirect('/provider/messages/inbox')
                else:
                    error_message = "Please fill the Recipient Email"
            except Exception:
                print "except block"
                email = User.objects.get(email=id1)
                recipient_list.append(email)

                if form.is_valid():                
                    current_user = User.objects.get(id=request.user.id)
                    if recipient_list:
                        for res in recipient_list:                            
                            form.save(sender=current_user,recpt=res,body1=body1)
                    else:
                        pass
                    messages.info(request, (u"Message successfully sent."))            
                    return HttpResponseRedirect('/provider/messages/inbox')

      
        else:
            form = form_class()
            if recipient is not None:
                recipients = [u for u in UserProfile.objects.filter(
                    **{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
                form.fields['recipient'].initial = recipients

        return render_to_response('messages/provider_messages_compose.html', {'form': form,
            "user":present_user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
            'error_message':error_message,},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")

@login_required
def provider_reply(request, msg_id, form_class=ComposeForm, success_url=None,
        recipient_filter=None):
    ''' reply to the contact messages''' 

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2: 

        user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass

        message_id = msg_id
        parent = get_object_or_404(Message, id=message_id)
        messages = Message.objects.filter(id=message_id)
        reply_recipient = ""
        subject1 = ""
        for msg in messages:
            print "reply messages"
            print msg.sender_id
            print "subject"
            print msg.subject
            subject1 = msg.subject
            re = User.objects.get(id=msg.sender_id).email
            print re
            print msg.recipient
            reply_recipient = re

        if parent.sender != request.user and parent.recipient != request.user:
            raise Http404
        if request.method == "POST":
            sender = request.user
            form = form_class(request.POST, recipient_filter=recipient_filter)
            if form.is_valid():
                form.save(sender=request.user, parent_msg=parent)
                messages.info(request, (u"Message successfully sent."))

                if success_url is None:
                    success_url = reverse('inbox')
                return HttpResponseRedirect(success_url)
        else:
            form = form_class(initial={
                'subject': parent.subject,
                'recipient': parent.sender
                })
        return render_to_response('messages/provider_messages_reply.html', 
            {'form': form,
            "user":user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
            'recipient':reply_recipient,
            'subject':subject1,},
            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")


@login_required
def provider_outbox(request):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        user = request.user
        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""
        for role in role_user:
            usr_type=role.role_id
            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        message_list = Message.objects.outbox_for(request.user)
       

        return render_to_response('messages/provider_messages_outbox.html', {
            'message_list': message_list,
            "user":user,
            'conformation_researcher':conformation_researcher,
            'conformation_lab':conformation_lab,
        }, context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")



@login_required
def provider_trash(request):    
    '''
    handles the index page when user is not logged in
    @request  request object    '''

    dashboard_type = "provider"
    # role_user=Userroles.objects.get(user_id=request.user.id).role_id
    role_users=Userroles.objects.filter(user_id=request.user.id)
    role_user=None
    for user in role_users:
        role_user=user.role_id
    if dashboard_type == "provider" and role_user == 2:
        user = request.user

        role_user=Userroles.objects.filter(user_id=request.user.id)
        conformation_researcher=""
        conformation_lab=""

        for role in role_user:
            usr_type=role.role_id

            if usr_type==1:
                conformation_researcher="researcher"
            elif usr_type==2:
                conformation_lab="conformation_lab"
            else:
                pass
        #for Inbox
        message_list=Message.objects.filter(provider_display_status=1)
        # message_list = Message.objects.inbox_for(request.user)
        # index = Message.objects.filter(recipient=request.user).count()
        # no_of_unread = message_list.filter(read_at=None).count()    
        
        # #for Outbox
        # sentmessage_list = Message.objects.outbox_for(request.user)    

        return render_to_response('messages/provider_messages_trash.html',
                           {
                            "user":user,
                            'message_list':message_list,
                            'conformation_researcher':conformation_researcher,
                            'conformation_lab':conformation_lab,},
                            context_instance=RequestContext(request))
    else :       
        return redirect("/logout/")



def allmessages(request):

    return render_to_response("messages/messages_base.html")

def messages_inbox(request):

    return render_to_response("messages/messages_inbox.html")

def messages_compose(request):

    users = Userroles.objects.filter(user_id=request.user.id)
    rollname = ""
    users_list = []
    for user in users:
        rollname = user.roll_name
    
    if rollname == "researcher":        
        labusers = Userroles.objects.filter(roll_name="lab")
        list1 = []
        for i in labusers:            
            user = User.objects.filter(id=i.user_id)
            list2=[]
            for j in user:                
                email = j.email                
                users_list.append(j.email)

    return HttpResponse(json.dumps(users_list), content_type='application/json')

@login_required
def provider_messages_compose(request):
    users = Userroles.objects.filter(user_id=request.user.id)
    rollname = ""
    users_list = []
    for user in users:
        rollname = user.roll_name
    
    if rollname == "lab":        
        labusers = Userroles.objects.filter(roll_name="researcher")
        list1 = []
        for i in labusers:            
            user = User.objects.filter(id=i.user_id)
            list2=[]
            for j in user:                
                email = j.email                
                users_list.append(j.email)

    return HttpResponse(json.dumps(users_list), content_type='application/json')

    

def sort_by_value(request):
    sort_value=""
    for key,value in request.GET.items():
        sort_value=key

    service_value=sort_value.split('*')
    services="new_services"
    sub_services = Services.objects.filter(id=int(service_value[1]))
    service_id = None
    for s in sub_services:        
        service_id = s.id  
    request.session["filter_services_id"]=service_id
    all_labs = Lab.objects.filter(service_id=s.id)
    serviceID=int(service_value[1])

    return render_to_response('sort-results.html', 
        {'all_labs':all_labs,
        'serviceID':serviceID,
        },
        context_instance=RequestContext(request))


def Quote_accept(request,qut_id):

    # Quote_status.objects.filter(quote_id=qut_id).update(
    #     name="Active-Pending",description="selected but waiting on payment",
    #     status_id=3)
    # Quotes.objects.filter(id=qut_id).update(status_id=3)    

    #quote_info=Quotes.objects.filter(id=qut_id)
    quote_info=Quotes.objects.filter(id=qut_id)
    lab_name=""
    lab_country=""
    res_phone=""
    res_email=""
    res_name=""

    for quote in quote_info:
        lab_info=Lab.objects.get(id=quote.lab_id)
        lab_name=lab_info.title
        lab_country=lab_info.country
        res_user_info=Users.objects.get(user_id=quote.researcher_id)
        res_phone=res_user_info.phone
        res_email=res_user_info.email
        res_name=res_user_info.username


    return render_to_response('researcher/purchase.html', 
        {'quote_info':quote_info,
        'lab_name':lab_name,
        'lab_country':lab_country,
        'res_phone':res_phone,
        'res_email':res_email,
        'res_name':res_name,
        'qut_id':qut_id,
        },
 
        context_instance=RequestContext(request))


def Quote_reject(request,qut_id):
    print "this is Quote Rejectance"
    print qut_id

    Quote_status.objects.filter(quote_id=qut_id).update(
        name="DECLINED",description="Quote Rejected",
        status_id=2)
    Quotes.objects.filter(id=qut_id).update(status_id=2)
    messages.success(request,(u"Your Quote has been rejected "))
    return HttpResponse("this is quote rejectance")
    #return redirect('/buyer/quotes/')


def testing(request):
    return HttpResponse("this is form")

def lab_serch_filters(request):

    total_search_list=request.session["total_searchlabs_id"]

    if request.GET:
        checkd_value_list=[]
        frst_filtr_rslt_lst=[]
        list_filter_labs = request.GET
        myDict = dict(list_filter_labs.iterlists())
        fitr_results=[]
        for key,value in  myDict.items():
            checkd_value_list.append(value)
        print checkd_value_list
        size_checkd_value_list=len(checkd_value_list)

        if size_checkd_value_list==1:
            ser_search_country=Lab.objects.filter(id__in=total_search_list,country__in=checkd_value_list[0],)
            for ser_country in ser_search_country:
                frst_filtr_rslt_lst.append(ser_country.id)

            ser_search_typeorg=Lab.objects.filter(id__in=total_search_list,typeorg__in=checkd_value_list[0])
            for ser_org in ser_search_typeorg:
                frst_filtr_rslt_lst.append(ser_org.id)

        elif size_checkd_value_list==2:
            ser_search_country=Lab.objects.filter(id__in=total_search_list,country__in=checkd_value_list[0],typeorg__in=checkd_value_list[1],
                )
            for ser_country in ser_search_country:
                frst_filtr_rslt_lst.append(ser_country.id)

            ser_search_typorg=Lab.objects.filter(id__in=total_search_list,country__in=checkd_value_list[1],typeorg__in=checkd_value_list[0],
                )
            for ser_org in ser_search_typorg:
                frst_filtr_rslt_lst.append(ser_org.id)


        elif size_checkd_value_list==3:
            pass

        lab_results_dsply=Lab.objects.filter(id__in=frst_filtr_rslt_lst)
    else:
        lab_results_dsply=Lab.objects.filter(id__in=total_search_list)


    return render_to_response('lab-serch-results.html',
        {'lab_results_dsply':lab_results_dsply}, 
        context_instance=RequestContext(request))


def quote_payment_form(request):
    return render_to_response('researcher/payment-form.html', 
     context_instance=RequestContext(request))



def trash_messages(request):
    trash_value_list=[]
    trash_values= request.GET
    myDict = dict(trash_values.iterlists())
    for key,value in  myDict.items():
        trash_value_list=value
    data1 = Message.objects.filter(id__in=trash_value_list).update(buyer_display_status=1)
    msg_val=Message.objects.filter(id__in=trash_value_list)
    messages.success(request,(u"Conversation Moved To Trash"))
    return HttpResponse("Hiii this is trashbox")

def trash_move_inbox(request):
    move_inbox_list=[]
    move_inbox_values= request.GET
    myDict = dict(move_inbox_values.iterlists())
    for key,value in  myDict.items():
        move_inbox_list=value
    data1 = Message.objects.filter(id__in=move_inbox_list).update(buyer_display_status=None)
    #msg_val=Message.objects.filter(id__in=trash_value_list)
    messages.success(request,(u"Conversation Moved To Inbox"))
    return HttpResponse("Hiii this is trashbox")


def trash_delete(request):
    delete_list=[]
    delete_values= request.GET
    myDict = dict(delete_values.iterlists())
    for key,value in  myDict.items():
        delete_list=value
    data1 = Message.objects.filter(id__in=delete_list).update(buyer_display_status=2)
    #msg_val=Message.objects.filter(id__in=trash_value_list)
    messages.success(request,(u"Conversation Deleted"))
    return HttpResponse("Hiii this is trashbox")


def move_inbox_trash_provider(request):
    inbox_trash_value_list=[]
    inbox_trash_values= request.GET
    myDict = dict(inbox_trash_values.iterlists())
    for key,value in  myDict.items():
        inbox_trash_value_list=value

    print '**********************'
    print inbox_trash_value_list
    print '**********************'
    data1 = Message.objects.filter(id__in=inbox_trash_value_list).update(provider_display_status=1)
    return HttpResponse("Hiii this is trashbox")

def trash_move_inbox_provider(request):
    print "this is trash to inbox"
    prvdr_inbox_list=[]
    prvdr_inbox_values= request.GET
    myDict = dict(prvdr_inbox_values.iterlists())
    for key,value in  myDict.items():
        prvdr_inbox_list=value

    print prvdr_inbox_list
    data1 = Message.objects.filter(id__in=prvdr_inbox_list).update(provider_display_status=None)
    # #msg_val=Message.objects.filter(id__in=trash_value_list)
    messages.success(request,(u"Conversation Moved To Inbox"))
    return HttpResponse("Hiii this is trashbox")


def trash_delete_provider(request):
    delete_list=[]
    delete_values= request.GET
    myDict = dict(delete_values.iterlists())
    for key,value in  myDict.items():
        delete_list=value
    print delete_list
    data1 = Message.objects.filter(id__in=delete_list).update(provider_display_status=2)
    return HttpResponse("Hiii this is trashbox")

def sent_box_provider(request):
    sentbox_list=[]
    sentbox_values= request.GET
    myDict = dict(sentbox_values.iterlists())
    for key,value in  myDict.items():
        sentbox_list=value
    print sentbox_list
    # data1 = Message.objects.filter(id__in=sentbox_list).update(provider_display_status=2)
    # #msg_val=Message.objects.filter(id__in=trash_value_list)
    # messages.success(request,(u"Conversation Deleted"))
    return HttpResponse("Hiii this is trashbox")

def buyer_quote_accept_creditcard(request,qut_id):
    publishkey=settings.STRIPE_PUBLISHABLE_KEY
    email=request.user.email
    price=None
    Quote_info=Quotes.objects.filter(id=qut_id)
    for quote in Quote_info:
        price=quote.price
    print '***********************'
    price_quote=int(price)*100

    if request.method == 'POST':
        token=request.POST['stripeToken']
        print token
        try:
            stripe_customer = stripe.Customer.create(
                    card=token,
                    description=request.user.email
                )
            charge_custmer=stripe.Charge.create(
                    amount=price_quote, # in cents
                    currency="usd",
                    customer=stripe_customer.id
                )

            stripe_amount=charge_custmer["amount"]/100
            stripe_customer=charge_custmer["customer"]
            stripe_charge=charge_custmer["id"]

            Quote_payments(quote_id=qut_id,amount=stripe_amount,
                customer=stripe_customer,
                charge_id=stripe_charge).save()
            print '*******************'
            print stripe_amount
            print charge_custmer
            print '*******************'
            Quote_status.objects.filter(quote_id=qut_id).update(
                name="Active",description="Payment has been made to BioMarketX and Project starts",
                status_id=4)
            Quotes.objects.filter(id=qut_id).update(status_id=4)

            quote_data=Quotes.objects.filter(id=qut_id)
            for qutdta in quote_data:
                #pass
                Orders(
                    researcher_id=qutdta.researcher_id,
                    researcher_name=qutdta.researcher_name,
                    lab_id=qutdta.lab_id,
                    service_id=qutdta.service_id,
                    service_name=qutdta.service_name,
                    desc=qutdta.desc,
                    notes=qutdta.notes,
                    price=qutdta.price,
                    duration=qutdta.duration,
                    memo=qutdta.memo,
                    status_id=1,
                    ).save()

            orderid=Orders.objects.latest('created_at').id
            servid=str(orderid).zfill(4)
            Orders.objects.filter(id=orderid).update(sid=servid)
            order_status(order_id=orderid,name="Order Active",
                description="Quote paid",status_id=1).save()
            quote_files=Quote_files.objects.filter(quote_id=qut_id)    
            
            for qutfile in quote_files:
                order_files(order_id=orderid,filename=qutfile.filename).save()

        except stripe.error.CardError, e:
          pass

        messages.success(request,(u"Your Transaction Done Succesfully"))
        return redirect('/buyer/quotes/')
    else:
        pass
    return render_to_response('researcher/stripe-payments.html',
        {'publishkey':publishkey,'qut_id':qut_id},
        context_instance=RequestContext(request))
        
def select_payment_type(request,qut_id):
    return render_to_response('researcher/payment-type.html',
        {'qut_id':qut_id},
        context_instance=RequestContext(request))
        
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def wiretransfer_payment(request,qut_id):
    email_address=request.user.email
    print email_address
    quote_id=""
    price=None
    title=""
    description=""
    quote_data=Quotes.objects.filter(id=qut_id)
    for quote in quote_data:
        quote_id=quote.sid
        price=quote.price
        title=quote.service_name
        description=quote.desc
    subject, from_email, = 'Quote Acceptance Payment Through Wire Transfer', 'from@yopmail.com', 
    to_email=['vinod_nyros@yahoo.com',email_address]
    text_content = 'This is an important message.'
    html_content = '<p><strong>QuoteID:</strong>%s</p><p><strong>Title:</strong>%s</p><p><strong>Price:</strong>%s</p><p><strong>Description:</strong>%s</p>'%(quote_id,title,price,description)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    Quote_status.objects.filter(quote_id=qut_id).update(
            name="Active-Pending",description="selected but waiting on payment",
            status_id=3)
    Quotes.objects.filter(id=qut_id).update(status_id=3)
    quote_data=Quotes.objects.filter(id=qut_id)
    for qutdta in quote_data:
                #pass
        Orders(
            researcher_id=qutdta.researcher_id,
            researcher_name=qutdta.researcher_name,
            lab_id=qutdta.lab_id,
            service_id=qutdta.service_id,
            service_name=qutdta.service_name,
            desc=qutdta.desc,
            notes=qutdta.notes,
            price=qutdta.price,
            duration=qutdta.duration,
            memo=qutdta.memo,
            status_id=2,
            ).save()
        orderid=Orders.objects.latest('created_at').id
        servid=str(orderid).zfill(4)
        Orders.objects.filter(id=orderid).update(sid=servid)
        order_status(order_id=orderid,name="Order Accepted Pending",
            description="Quote waiting for ADMIN to approval",
                status_id=1).save()

    messages.success(request,(u"Email has been sent to you.My specialist will contact you shortly"))
    return redirect('/buyer/quotes/')
 
    #return HttpResponse("hiiiii this is wire transfer payments")



def provider_orders(request):
    dashboard_type = "provider"
    role_user=Userroles.objects.get(user_id=request.user.id).role_id
    if dashboard_type == "provider" and role_user == 2:
        user = request.user    
        userid=request.user.id
        labID=None
        labdetails = Lab.objects.filter(user_id=userid)
        for lab in labdetails:
            labID=lab.id        
        
        if labID:
            print '*******************'
            print labID
            print '*******************'
            display_list=[]
            display_orders=Orders.objects.filter(lab_id=labID)
            
            return render_to_response('lab/provider-orders.html',{'display_orders':display_orders, 'user':user,})
        else:
            return render_to_response('lab/provider-orders.html',)
    else :       
        return redirect("/logout/")


@login_required
def privider_order_desc(request,ordr_id):
    dashboard_type = "provider"
    role_user=Userroles.objects.get(user_id=request.user.id).role_id
    if dashboard_type == "provider" and role_user == 2:
        user = request.user    
        userid=request.user.id
        labID=None
        labdetails = Lab.objects.filter(user_id=userid)
        for lab in labdetails:
            labID=lab.id        
        
        if labID:
            print '*******************'
            print labID
            print '*******************'
            display_list=[]
            display_orders=Orders.objects.filter(lab_id=labID)

        download_file=[]    
        download=order_files.objects.filter(order_id=ordr_id)

        for downld in download:
            #download_file.append(downld.filename)
            download_file1=str(downld.filename).replace('quotes/','')
            download_file.append(download_file1)
        lenght_download=len(download_file)
        order_info=Orders.objects.filter(id=ordr_id)
        
        print '********************'
        print download_file
        print download

        print '********************'


        return render_to_response('lab/provider-order-desc.html',{'user':user,
            'display_orders':display_orders,
            'order_info':order_info,
            'download_file':download_file,
            'lenght_download':lenght_download})
    else :       
        return redirect("/logout/")

    #return HttpResponse("hii this is testing the providers orders")


def buyer_orders(request):
    dashboard_type = "buyer"
    print request.user.id
    role_user=Userroles.objects.get(user_id=request.user.id).role_id
    if dashboard_type == "buyer" and role_user == 1:        
        conformation_researcher="researcher"
        user = request.user        
        buyer_orders=Orders.objects.filter(researcher_id=request.user.id,
            )
        print '*******************'
        print buyer_orders
        print '*******************'
        return render_to_response('researcher/buyer-orders.html',
                {'buyer_orders':buyer_orders,"conformation_researcher":conformation_researcher,
                'user':user,})

    else :       
        return redirect("/logout/") 


@login_required
def buyer_order_desc(request,ordr_id):
    dashboard_type = "buyer"
    role_user=Userroles.objects.get(user_id=request.user.id).role_id
    if dashboard_type == "buyer" and role_user == 1:  
        user = request.user
        userid=request.user.id
        # labID=None
        # labdetails = Lab.objects.filter(user_id=userid)
        # for lab in labdetails:
        #     labID=lab.id

        labID=None
        lab_name=""
        order_info=Orders.objects.filter(id=ordr_id)
        for ordr in order_info:
            labID=ordr.lab_id

        labinfo=Lab.objects.filter(id=labID)
        for lab in labinfo:
            lab_name=lab.title
        download_file=[]    
        download=order_files.objects.filter(order_id=ordr_id)

        for downld in download:
            #download_file.append(downld.filename)
            download_file1=str(downld.filename).replace('quotes/','')
            download_file.append(download_file1)
        lenght_download=len(download_file)
        
        buyer_orders=Orders.objects.filter(researcher_id=request.user.id)

        return render_to_response('researcher/buyer-order-desc.html',{
            'buyer_orders':buyer_orders,
            'user':user,
            'order_info':order_info,
            'lab_name':lab_name,
            'download_file':download_file,
            'lenght_download':lenght_download})
    else :       
        return redirect("/logout/") 

@login_required
def workroom_allocation(request,ordr_id):
    dashboard_type = "buyer"
    role_user=Userroles.objects.get(user_id=request.user.id).role_id
    if dashboard_type == "buyer" and role_user == 1:  
        if request.method == 'POST':
            form = WorkroomForm(request.POST,request.FILES)
            if form.is_valid():
                print request.POST
                print request.FILES
                print type(request.FILES)
                files_list=[]
                files_values= request.FILES
                myDict = dict(files_values.iterlists())
                for key,value in  myDict.items():
                    files_list=value
                desc = request.POST.get('description')
                send_file = form.cleaned_data['send_file']
                send_file1 = request.POST.getlist('send_file[]')

                print '********************'
                print desc
                print len(files_list)
                print '********************'
                role_name=""
                if role_user==1:
                    role_name="researcher"
                elif role_user==2:
                    role_name=lab
                Workroom(description=desc,
                    name=request.user,
                    order_id=ordr_id,
                    user_role=role_name,
                    user_id=request.user.id
                    ).save()

                workroom_id=Workroom.objects.latest('created_at').id
                for files in files_list:
                    workroom_files(workroom_id=workroom_id,order_id=ordr_id,filename=files,).save()
                return redirect('/buyer/workroom/%s/'%ordr_id)
        else:
            form = WorkroomForm()
        workroom_info=Workroom.objects.filter(order_id=ordr_id)
        order_info=Orders.objects.filter(id=ordr_id)
        workroomfile=workroom_files.objects.filter(order_id=ordr_id)
        print '*******************'
        print workroom_info
        print '*******************'
        return render(request, 'researcher/workroom_new.html', {'form':form,
            'workroom_info':workroom_info,'order_info':order_info,
            'workroomfile':workroomfile,
            },context_instance=RequestContext(request))
    else :       
        return redirect("/logout/") 


@login_required
def provider_workroom(request,ordr_id):
    dashboard_type = "provider"
    role_user=Userroles.objects.get(user_id=request.user.id).role_id
    if dashboard_type == "provider" and role_user == 2:

        if request.method == 'POST':
            form = WorkroomForm(request.POST,request.FILES)
            if form.is_valid():
                print request.POST
                print request.FILES
                print type(request.FILES)
                files_list=[]
                files_values= request.FILES
                myDict = dict(files_values.iterlists())
                for key,value in  myDict.items():
                    files_list=value
                desc = request.POST.get('description')
                send_file = form.cleaned_data['send_file']
                send_file1 = request.POST.getlist('send_file[]')

                print '********************'
                print desc
                print len(files_list)
                print '********************'
                role_name=""
                if role_user==1:
                    role_name="researcher"
                elif role_user==2:
                    role_name="lab"
                Workroom(description=desc,
                    name=request.user,
                    order_id=ordr_id,
                    user_role=role_name,
                    user_id=request.user.id
                    ).save()

                workroom_id=Workroom.objects.latest('created_at').id
                for files in files_list:
                    workroom_files(workroom_id=workroom_id,order_id=ordr_id,filename=files,).save()
                return redirect('/provider/workroom/%s/'%ordr_id)
        else:
            form = WorkroomForm()
        workroom_info=Workroom.objects.filter(order_id=ordr_id)
        order_info=Orders.objects.filter(id=ordr_id)
        workroomfile=workroom_files.objects.filter(order_id=ordr_id)
        print '*******************'
        print workroom_info
        print '*******************'
        return render(request, 'lab/provider-workroom.html', {'form':form,
            'workroom_info':workroom_info,'order_info':order_info,
            'workroomfile':workroomfile,
            
            },context_instance=RequestContext(request))
    else :       
        return redirect("/logout/") 


@login_required(login_url='/backend/login/')
def admin_edit_static(request):
    print "admin_edit_static"
    # print request.session['edit_name']
    # value=edit_about.objects.filter(id)
    # print "_____________________________________________________________"
    # print value
    # print "_______________________________________________________________"
    info=edit_about.objects.filter(id=1)
    information_about=None
    for i in info:
        print i.data
        information_about=i.data
    if request.method == 'POST':
        form = about_editForm(request.POST)
        # print form
        print request.POST
        if form.is_valid():
            about_data = request.POST.get("Description")
            print about_data
            edit_about.objects.filter(id=1).update(data=about_data) 
            return redirect('/about/')
        else:
            print "not valied"
    else:

        form = about_editForm()
    print "*****************"
    print information_about
    print "*********************"
    return render_to_response('admin/about_edit.html',
        {"form":form,"information_about":information_about},
        context_instance=RequestContext(request))

@login_required(login_url='/backend/login/')
def admin_edit_staticdata_display(request):
    print "admin_edit_staticdata_display"
    info=edit_about.objects.filter(id=1)
    information=None
    for i in info:
        print i.data
        information=i.data
    # return HttpResponse(information)
    print "*********************"
    print information
    print "**************************8"
    return render_to_response('new_about.html',
        {"information":information},
        context_instance=RequestContext(request))
    # if request.method == 'POST':
    #     form = about_editForm(request.POST)
    #     # print form
    #     print request.POST
    #     if form.is_valid():
    #         about_data = request.POST.get("Description")
    #         print about_data
    #         edit_about.objects.filter(id=1).update(data=about_data) 
    #     else:
    #         print "not valied"
    # else:

    #     form = about_editForm()

    # return render_to_response('admin/static_edit.html',
    #     {"form":form},
    #     context_instance=RequestContext(request))



@login_required(login_url='/backend/login/')
def admin_staticdata(request):
    print "admin_staticdata"
    about_page_getdata = request.GET
    print "_______________________________________________________________"
    # print about_page_getdata
    print "_______________________________________________________________"
    myabout = dict(about_page_getdata.iterlists())
    about_static_value=None
    for key,value in  myabout.items():
        about_static_value=value  
        # print checkd_value_list      
    for i in about_static_value:
        about= i
        # print i
    # print "_______________________________________________________________"
    # print about
    # print "_______________________________________________________________"
    request.session['about_edit'] =about
    test_about=edit_about.objects.filter(id=1)
    if test_about:
        about_data=edit_about.objects.filter(id=1).update(data=about)
    else:
        edit_about.objects.create(data=about)
    # for a in about_data.iteritems():
    #     print a.data
    # print request.GET
    
    return render_to_response('admin/static_edit.html',
        {"about":about},
        context_instance=RequestContext(request))




@login_required(login_url='/backend/login/')
def about_static(request):

    return render_to_response('admin/about_edit.html',
        {},
        context_instance=RequestContext(request))



    

def about(request):
    '''About View'''

    user = request.user
    role_user=Userroles.objects.filter(user_id=request.user.id)
    conformation_researcher=""
    conformation_lab=""

    for role in role_user:
        usr_type=role.role_id

        if usr_type==1:
            conformation_researcher="researcher"
        elif usr_type==2:
            conformation_lab="conformation_lab"
        else:
            pass

    about="about_page"
    info=edit_about.objects.filter(id=1)
    information=None
    for i in info:
        information=i.data
    return render_to_response('new_about.html',{"information":information,"about":about,"user":user,
        'conformation_researcher':conformation_researcher,'conformation_lab':conformation_lab,},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def consulting_edit(request):
    print "consulting_edit"
    consult_page_getdata =request.GET
    print "*********************************"
    # print request.GET
    print "*********************************"
    myconsult = dict(consult_page_getdata.iterlists())
    # print myconsult
    consult_static_value=None
    for key,value in  myconsult.items():
        consult_static_value=value  
        # print checkd_value_list  
    consult=None    
    for i in consult_static_value:
        consult= i
    print "**********************"
    # print consult
    print "*************************"
    request.session['consult_edit'] =consult
    print request.session['consult_edit']

    return HttpResponse ("consulting_edit")

@login_required(login_url='/backend/login/')
def consulting_static(request):
    print "consulting_static"
    consult_data=request.session.get('consult_edit')
    print "(((((((((((((((((((((("
    # print consult_data
    if request.method == 'POST':
        form = about_editForm(request.POST)
        if form.is_valid():
            consult_table_data = request.POST.get("Description")
            print consult_table_data
            consult_info=edit_about.objects.filter(id=2)
            if consult_info:
                edit_about.objects.filter(id=2).update(data=consult_table_data)
            else:
                edit_about.objects.create(data=consult_table_data)
            print "valied"
            return redirect("/consulting/")
            
            

        else:
            print "not valied"
    else:
        form=about_editForm()
    return render_to_response('admin/consult_edit.html',{"form":form,"consult_data":consult_data},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def projects_edit(request):
    print "projects_edit"
    project_data=request.session.get('project_edit')
    print "(((((((((((((((((((((("
    # print project_data
    if request.method == 'POST':
        form = about_editForm(request.POST)
        if form.is_valid():
            project_table_data = request.POST.get("Description")
            print project_table_data
            project_info=edit_about.objects.filter(id=3)
            if project_info:
                edit_about.objects.filter(id=3).update(data=project_table_data)
            else:
                edit_about.objects.create(data=project_table_data)
            print "valied"
            return redirect("/projects/")
            
            

        else:
            print "not valied"
    else:
        form=about_editForm()
    return render_to_response('admin/project_edit.html',{"form":form,"project_data":project_data},
        context_instance=RequestContext(request))
    return HttpResponse ("parent_name")




@login_required(login_url='/backend/login/')
def projects_static(request):
    print "projects_static"
    project_page_getdata =request.GET
    # print project_page_getdata
    myproject = dict(project_page_getdata.iterlists())
    # print myconsult
    project_static_value=None
    for key,value in  myproject.items():
        project_static_value=value  
        # print checkd_value_list  
    project=None    
    for i in project_static_value:
        project= i
    # print "**********************"
    # print project
    # print "*************************"
    request.session['project_edit'] =project
    print request.session['project_edit']
    return HttpResponse ("projects")