from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from biomarketxapp.views import login
from .forms import *
from biomarketxapp.models import Users

from django.contrib.auth.decorators import login_required

# from django.contrib.auth.mixins import LoginRequiredMixin

# class MyView(LoginRequiredMixin, View):
#     login_url = '/backend/login/'
#     redirect_field_name = 'redirect_to'


# Create your views here.

import sys
sys.setrecursionlimit(100)
def main(request):
    print "main"
    user = request.user
    print "####################"
    print user
    print "*******"*20
    print user.is_superuser
    print "&&&&&&&&&&&&"

    if user.is_superuser:
        print "satisfied"
        return redirect("/backend/index/")
        # return render_to_response('admin/index.html',{"user":user,},context_instance=RequestContext(request))
    else:
        print "not ok"
        return redirect("/backend/login/")
        # return render_to_response('admin/login.html',context_instance=RequestContext(request))      

    # return HttpResponse(" this is main page")
    
    # if user.is_superuser
    # if req.usr=="admin"
    #     return HttpResponse("")
    #     redirect("/home")
    # else:9701128707
    #     redirct("/login")

@login_required(login_url='/backend/login/')
def admin_index(request):

    print "index page"

    users = User.objects.count()
    print "auth users"
    print users

    all_users = Users.objects.count()
    print "all"
    print all_users

    lab_users = Users.objects.filter(role_id=2).count()
    print "labs "
    print lab_users
    lab_deactivate = Users.objects.filter(role_id=2,is_active=0).count()
    print "deactivatelabs "
    print lab_deactivate    

    researchers = Users.objects.filter(role_id=1).count()
    print "researchers"
    print researchers

    return render_to_response('admin/dash.html',
        {"all":all_users, "labs":lab_users, "researchers":researchers,
        "lab_deactivate":lab_deactivate,},
        context_instance=RequestContext(request))
        
    # return HttpResponse(" this is admin dashboard page")

# def dash(request):
#     return render_to_response('admin/dash.html',context_instance=RequestContext(request))

def admin_login(request):
    login_view="This is login view" 
    error_message=""
    print "login"
    if request.method == 'POST':
        print "post"
        form = AdminLoginform(request.POST)
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print user
        print email
        if form.is_valid():
            print "form valid"
            if user:
                print "valid"
                auth_login(request, user)
                return redirect("/backend/")
            else:
                print "else block"
                error_message ="Email and Password did not match."
    else:
        form = AdminLoginform()
    print "form return"
    
    return render(request, 'admin/login.html', {'form':form,'error_message':error_message})
    # return render(request, 'login.html', {'form':form,
    #     'login_view':login_view,'error_message':error_message})
    # return redirect("/backend/login/")
    # return HttpResponse("login")

@login_required(login_url='/backend/login/')
def users(request):
    print "All users"
    users = " "
    user = Users.objects.all()

    print user


    return render_to_response('admin/users_all.html',
        {'users': user},
        context_instance=RequestContext(request))

@login_required(login_url='/backend/login/')
def edit_users(request,u_id):
    print "Hai"
    print u_id
    users = User.objects.filter(id=u_id)
    username = ""
    email = ""
    f_name = ""
    l_name = ""
    phone = ""
    know = ""
    org = ""
    # u_id = None
    data = []
    # active_status = None
    username1 = ""
    active_status = ""

    users_id = None
    users_uname = ""
    users_email = ""
    users_fname = ""
    users_lname = ""
    users_active = ""

    print "^^^^^^^^^^^^^^^^^"
    print users
    print "**********************"

    for user in users:
        # print "after 1st for"
        # user_details = User.objects.filter(id=user.user_id)
        # print user_details
        # for u in user_details:
        #     print "inner for"
        #     username1 = u.username
        #     uu_id = u.id
            # active = u.is_active
        username = user.username
        email = user.email
        f_name = user.first_name
        l_name = user.last_name
        # phone = user.phone
        # know = user.how_bio
        # org = user.name_org
        active_status = user.is_active
        print "$$$$$$$$$$$$$$$$"
        print active_status
        print ""
    data = Users.objects.filter(user_id=u_id)

    print "{{{{{{{{{{{{{{{{{{{"
    print data
    for d in data:
        users_id = d.id
        users_uname = d.username
        users_email = d.email
        users_fname = d.fname
        users_lname = d.lname
        users_active = d.is_active

    print "}}}}}}}}}}}}}}"
    print users_id
    print "before if"
    if request.method == 'POST':
        print "post method"
        form = UserForm(request.POST)
        # print form
        if form.is_valid():
            print "valid"
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            mail = request.POST.get("email")         
            # phone_num=request.POST.get("phone_number")
            # how_bio=request.POST.get("how_bio")
            # name_org=request.POST.get("name_org")
            active_status=request.POST.get("active_status")
            
            print '***********************'
            print active_status
            print '***********************'
            print 'this is vinod'
            if active_status=="True":
                print "this is vinod true"
                User.objects.filter(id=u_id).update(is_active=1)
                Users.objects.filter(id=users_id).update(is_active=1)
            else:
                print "this is vinod false"
                User.objects.filter(id=u_id).update(is_active=0)
                Users.objects.filter(id=users_id).update(is_active=0)


            print active_status
            # if active_status==True:
            #     print 'print active_status True'
            #     active_status1 = active_status
            #     u1 = User.objects.filter(id=u_id).update(is_active=1)
            #     u1.save()
            #     u2 = Users.objects.filter(id=l_id).update(is_active=1)
            #     u2.save()
            #     active_status1 = active_status
            # elif active_status==False:
            #     print 'print active_status False'
            #     u1 = User.objects.filter(id=u_id).update(is_active=0)
            #     u1.save()
            #     u2 = Users.objects.filter(id=l_id).update(is_active=0)
            #     u2.save()
            #     active_status1 = active_status
            # else:
            #     pass

            User.objects.filter(id=u_id).update(email=mail,username=username,
                first_name=first_name,last_name=last_name)

            Users.objects.filter(id=users_id).update(fname=first_name,
                lname=last_name,email=mail,username=username)       

            
            return redirect("/backend/users/")
    else:
        print "else"
        form = UserForm()

    return render_to_response('admin/users_all_edit.html',
        {"form":form,"username":users_uname, "email":email, "f_name":users_fname, "l_name":users_fname,
        "u_id":u_id,"active_status":active_status},
        context_instance=RequestContext(request))

@login_required(login_url='/backend/login/')
def del_users(request,u_id):
    print "delete"
    print u_id
    # uid = None
    # users_id = None
    # username = ""
    # users_name= ""
    # users = User.objects.filter(id=u_id)
    # # for user in users:
    # #     username = user.username
    # #     print "user name"
    # #     print username

    # data = Users.objects.filter(user_id=u_id)

    # for d in data:
    #     users_id = d.id
    #     print "data user id"
    #     print users_id
    # print "$$$$$$$$$$$$$$$$$$$$$4"
    # print l_id
    # print "***************"
    # print uid
    
    result1=Users.objects.filter(user_id=u_id).delete()
    # result1=Users.objects.filter(user_id=u_id)
    print"users**********"
    print result1
    result =User.objects.filter(id=u_id).delete()
    # result =User.objects.filter(id=u_id)
    print "user---------"
    print result

    # return HttpResponse("delete")
    return redirect("/backend/users/")

@login_required(login_url='/backend/login/')
def labusers(request):
    print "lab users"
    users = " "
    username = ""
    active_status = None
    created = ""
    email = ""
    name = ""
    lab_users = Users.objects.filter(role_id=2).all()

    deactive_labusers = Users.objects.filter(role_id=2,is_active=0).all()
    deactive_labusers_count = Users.objects.filter(role_id=2,is_active=0).count()
    print "^^^^^^^^^^^^^^^^^^^^"
    print deactive_labusers
    print deactive_labusers_count
    print "^^^^^^^^^^^^^^^^^^^^^6"
    # print lab_user
    for l in lab_users:
        print l.id
        print "&&&&&&&&&&&&&&"
        print l.user_id
        print l.username
        print l.created_at
        print l.email
        print l.is_active
        print "dsfdafa"
        print l.name_org
        name = l.fname + ''+ l.lname
        # email = labusers_list.append(l.email)
        # created = labusers_list.append(l.email)

        # user = User.objects.filter(id=l.user_id)
        # print user 
        # print type(user)
        # for u in user :
        #     print u.username
        #     username = u.username
        #     username1 = labusers_list.append(username)
        #     print u.is_active
        #     active = u.is_active
        #     active1 = labusers_list.append(active)

    # print labusers_list
    # user = User.objects.filter(user=lab_user)

    # print user


    return render_to_response('admin/users_labusers.html',
        {'users': lab_users, "name":name,"deactive_labusers":deactive_labusers,
        "count":deactive_labusers_count},
        context_instance=RequestContext(request))
        
@login_required(login_url='/backend/login/')
def edit_labusers(request,l_id):
    print "Hai"
    print l_id
    users = Users.objects.filter(id=l_id)
    username = ""
    email = ""
    f_name = ""
    l_name = ""
    phone = ""
    know = ""
    name_org = ""
    u_id = None
    # active_status = None
    username1 = ""
    active_status = ""

    print "^^^^^^^^^^^^^^^^^"
    print users
    print "**********************"

    for user in users:
        print "after 1st for"
        user_details = User.objects.filter(id=l_id)
        print user_details
        for u in user_details:
            print "inner for"
            username1 = u.username
            u_id = u.id
            # active = u.is_active
        username = user.username
        email = user.email
        f_name = user.fname
        l_name = user.lname
        phone = user.phone
        know = user.how_bio
        name_org = user.name_org
        active_status = user.is_active
        print "$$$$$$$$$$$$$$$$"
        print active_status
        print ""
    print "before if"
    if request.method == 'POST':
        print "post method"
        form = LabUserForm(request.POST)
        # print form
        if form.is_valid():
            print "valid"
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            mail = request.POST.get("email")         
            phone_num=request.POST.get("phone_number")
            how_bio=request.POST.get("how_bio")
            name_org=request.POST.get("name_org")
            active_status=request.POST.get("active_status")
            
            print '***********************'
            print active_status
            print '***********************'
            print 'this is vinod'
            if active_status=="Active":
                print "this is vinod true"
                User.objects.filter(id=l_id).update(is_active=1)
                Users.objects.filter(user_id=l_id).update(is_active=1)
            else:
                print "this is vinod false"
                User.objects.filter(id=l_id).update(is_active=0)
                Users.objects.filter(user_id=l_id).update(is_active=0)


            print active_status
            # if active_status==True:
            #     print 'print active_status True'
            #     active_status1 = active_status
            #     u1 = User.objects.filter(id=u_id).update(is_active=1)
            #     u1.save()
            #     u2 = Users.objects.filter(id=l_id).update(is_active=1)
            #     u2.save()
            #     active_status1 = active_status
            # elif active_status==False:
            #     print 'print active_status False'
            #     u1 = User.objects.filter(id=u_id).update(is_active=0)
            #     u1.save()
            #     u2 = Users.objects.filter(id=l_id).update(is_active=0)
            #     u2.save()
            #     active_status1 = active_status
            # else:
            #     pass

            Users.objects.filter(user_id=l_id).update(fname=first_name,
                lname=last_name,email=mail,how_bio=how_bio,
                name_org=name_org,phone=phone_num,username=username)       

            User.objects.filter(id=l_id).update(email=mail,username=username)
            return redirect("/backend/lab_users/")
    else:
        print "else"
        form = LabUserForm()

    return render_to_response('admin/users_labusers_edit.html',
        {"form":form,"username":username, "email":email, "f_name":f_name, "l_name":l_name, "phone":phone,
        "know":know, "name_org":name_org,"l_id":l_id,"active_status":active_status},
        context_instance=RequestContext(request)) 

@login_required(login_url='/backend/login/')
def del_labusers(request,l_id):
    print "delete"
    print l_id
    uid = None
    users = Users.objects.filter(user_id=l_id)
    for user in users:
        uid = user.user_id


    print "$$$$$$$$$$$$$$$$$$$$$4"
    print l_id
    print "***************"
    print uid
    Users.objects.filter(user_id=l_id)
    User.objects.filter(id=uid)
    # return HttpResponse("delete")
    return redirect("/backend/lab_users/")

   



@login_required(login_url='/backend/login/')
def researchers(request):
    print "lab users"
    users = " "
    username = ""
    active = ""
    researcher = Users.objects.filter(role_id=1)
    for l in researcher:
        print l.id
        print "&&&&&&&&&&&&&&"
        print l.user_id
        user = User.objects.filter(id=l.user_id)
        print user 
        print type(user)
        for u in user :
            print u.username
            username = u.username
            print u.is_active
            active = u.is_active


    # user = User.objects.filter(user=lab_user)

    # print user


    return render_to_response('admin/users_researchers.html',
        {'users': researcher, "active": active, "username": username},
        context_instance=RequestContext(request))

@login_required(login_url='/backend/login/')
def edit_researchers(request,r_id):

    print "Hai"
    print r_id

    users = Users.objects.filter(user_id=r_id)

    username = ""
    email = ""
    f_name = ""
    l_name = ""
    phone = ""
    know = ""
    org = ""
    u_id = None
    active_status = ""
    username1 = ""


    print users

    for user in users:
        user_details = User.objects.filter(id=r_id)
        print user_details
        for u in user_details:
            username1 = u.username
            u_id = u.id
            # active = u.is_active
        username = user.username
        email = user.email
        f_name = user.fname
        l_name = user.lname
        phone = user.phone
        know = user.how_bio
        org = user.name_org
        active_status = user.is_active
        print active_status
    print "before if"
    if request.method == 'POST':
        print "post method"
        form = ResearcherForm(request.POST)

        # print form
        if form.is_valid():
            print "valid"
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            mail = request.POST.get("email")         
            phone_num=request.POST.get("phone_number")
            how_bio=request.POST.get("how_bio")
            name_org=request.POST.get("name_org")
            active_status=request.POST.get("active_status")
            print active_status

            if active_status=="Active":
                print "this is vinod true"
                User.objects.filter(id=r_id).update(is_active=1)
                Users.objects.filter(user_id=r_id).update(is_active=1)
            else:
                print "this is vinod false"
                User.objects.filter(id=r_id).update(is_active=0)
                Users.objects.filter(user_id=r_id).update(is_active=0)

            Users.objects.filter(user_id=r_id).update(fname=first_name,
                lname=last_name,email=mail,how_bio=how_bio,
                name_org=name_org,phone=phone_num,username=username)       

            User.objects.filter(id=r_id).update(email=mail,username=username)
           

            return redirect("/backend/researchers/")
    else:
        print "else"
        form = ResearcherForm()

    return render_to_response('admin/users_researchers_edit.html',
        {"form":form,"username":username, "email":email, "f_name":f_name, "l_name":l_name, "phone":phone,
        "know":know, "org":org,"r_id":r_id,"active_status":active_status},
        context_instance=RequestContext(request))

@login_required(login_url='/backend/login/')
def del_researchers(request,r_id):
    print "delete"
    print r_id
    uid = None
    users = Users.objects.filter(id=r_id)
    for user in users:
        uid = user.user_id


    print "$$$$$$$$$$$$$$$$$$$$$4"
    print r_id
    print "***************"
    print uid
    Users.objects.filter(id=r_id).delete()
    User.objects.filter(id=uid).delete()
    # return HttpResponse("delete")
    return redirect("/backend/researchers/")  
      
@login_required(login_url='/backend/login/')
def admin_logout(request):
    print "logout"
    logout(request)
    return redirect('/backend/')
    
#     print "&&&&&&&&&&&&&&&&&&&"
#     return HttpResponse("logout")
#     return redirect("/")

