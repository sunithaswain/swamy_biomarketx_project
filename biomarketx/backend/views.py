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
from django.contrib import messages
from biomarketxapp.models import *
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
    user = Users.objects.all().order_by('id')


    user1 = Users.objects.all().order_by('user_id').reverse()
    for i in user1:
        print "&&&&&&&&&&&"
        print i.user_id

    # filter(client=client_id).order_by('-check_in')

    print user
    print type(user)

    # user.desc()


    return render_to_response('admin/users_all.html',
        {'users': user1},
        context_instance=RequestContext(request))

@login_required(login_url='/backend/login/')
def edit_users(request,u_id):
    print "Hai"
    print u_id

    users = Users.objects.filter(id=u_id)

    user_id = None
    print user_id
    for u in users:
        user_id = u.user_id
    print user_id
    print users

    auth_users = User.objects.filter(id=user_id)
    print "^^^^^^^^^^^^^^"
    print auth_users


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
    # username1 = ""
    # active_status = ""

    users_id = None
    users_uname = ""
    users_email = ""
    users_fname = ""
    users_lname = ""
    users_active = ""

    # print "^^^^^^^^^^^^^^^^^"
    # print users
    # print "**********************"

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
        f_name = user.fname
        l_name = user.lname
        # phone = user.phone
        # know = user.how_bio
        # org = user.name_org
        active_status = user.is_active
        print "$$$$$$$$$$$$$$$$"
        print active_status
        print ""
    # data = Users.objects.filter(username=username)

    # print "{{{{{{{{{{{{{{{{{{{"
    # print data
    # for d in data:
    #     users_id = d.id
    #     users_uname = d.username
    #     users_email = d.email
    #     users_fname = d.fname
    #     users_lname = d.lname
    #     users_active = d.is_active

    # print "}}}}}}}}}}}}}}"
    # print users_id
    # print "before if"
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
            if active_status=="Active":
                print "this is vinod true"
                User.objects.filter(id=user_id).update(is_active=1)
                Users.objects.filter(id=u_id).update(is_active=1)
            else:
                print "this is vinod false"
                User.objects.filter(id=user_id).update(is_active=0)
                Users.objects.filter(id=u_id).update(is_active=0)


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

            User.objects.filter(id=user_id).update(email=mail,username=username,
                first_name=first_name,last_name=last_name)

            Users.objects.filter(id=u_id).update(fname=first_name,
                lname=last_name,email=mail,username=username)       

            messages.success(request, (u"User updated successfully.."))
            return redirect("/backend/users/")
    else:
        print "else"
        form = UserForm()

    # return HttpResponse("ji")

    return render_to_response('admin/users_all_edit.html',
        {"form":form,"username":username, "email":email, "f_name":f_name, "l_name":l_name,
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
    messages.success(request, (u"User has been deleted .."))
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
    # lab_users = Users.objects.filter(role_id=2).latest('created_at')

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
    error_message=""
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
    print "********************"

    for user in users:
        print "after 1st for"
        user_details = User.objects.filter(id=user.user_id)
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
        print name_org
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
                User.objects.filter(id=u_id).update(is_active=1)
                Users.objects.filter(id=l_id).update(is_active=1)
            else:
                print "this is vinod false"
                User.objects.filter(id=u_id).update(is_active=0)
                Users.objects.filter(id=l_id).update(is_active=0)


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

            Users.objects.filter(id=l_id).update(fname=first_name,
                lname=last_name,email=mail,how_bio=how_bio,
                name_org=name_org,phone=phone_num,username=username)       

            User.objects.filter(id=u_id).update(email=mail,username=username)
            # success_message = "Thank you for your request. A lab listing specialist will contact you shortly."
            messages.success(request, (u"provider updated successfully.."))
            return redirect("/backend/providers/")
            #return HttpResponseRedirect() lab_users/edit
    else:
        print "else"
        form = LabUserForm()

    # return render_to_response('admin/users_labusers_edit.html',
    #     {"form":form, "l_id":l_id,},
    #     context_instance=RequestContext(request))

    return render_to_response('admin/users_labusers_edit.html',
        {"form":form,
        "username":username, 
        "email":email, 
        "f_name":f_name, 
        "l_name":l_name, 
        "phone":phone,
        "know":know, 
        "name_org":name_org,
        "l_id":l_id,
        "active_status":active_status,
        'error_message':error_message,},
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
    messages.success(request, (u"Lab user has been deleted .."))
    return redirect("/backend/providers/")

   



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

    users = Users.objects.filter(id=r_id)

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
        user_details = User.objects.filter(id=user.user_id)
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
                User.objects.filter(id=u_id).update(is_active=1)
                Users.objects.filter(id=r_id).update(is_active=1)
            else:
                print "this is vinod false"
                User.objects.filter(id=u_id).update(is_active=0)
                Users.objects.filter(id=r_id).update(is_active=0)

            Users.objects.filter(id=r_id).update(fname=first_name,
                lname=last_name,email=mail,how_bio=how_bio,
                name_org=name_org,phone=phone_num,username=username)       

            User.objects.filter(id=u_id).update(email=mail,username=username)
           
            messages.success(request, (u"Buyer updated successfully.."))
            return redirect("/backend/buyers/")
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
    messages.success(request, (u"Researcher has been deleted .."))
    return redirect("/backend/buyers/")  
      
@login_required(login_url='/backend/login/')
def admin_logout(request):
    print "logout"
    logout(request)
    return redirect('/backend/')
    # print "logout"
    # if request.user.is_superuser:
    #     print "logout"
    #     logout(request)
    #     return redirect('/backend/')
    # else:
    #     print "else"
    #     pass
    # print "end"
    # return redirect('/backend/')   
    
#     print "&&&&&&&&&&&&&&&&&&&"
#     return HttpResponse("logout")
#     return redirect("/")

@login_required(login_url='/backend/login/')
def admin_profile(request):
    print "admin_profile"

    # return HttpResponse("good")
    return render_to_response('admin/pages-user-profile.html',
        {},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def admin_services(request):
    print "admin_services"
    service=[]
    service=Services.objects.filter(pid=0)
    service_parent=[]
    for i in service:
        # print "(*$$$$$$$"
        # print i.id
        # print "(T^^^^%"
        parent_details=[]
        parent_details.append(i.name)
        parent_details.append(i.id)
        # print i.name
        # print i.id
        service_child=Services.objects.filter(pid=i.id)
        child=[]
        for j in service_child:
            # print j.pid
            # print j.id
            child.append(j.name)
            # child.append(j.id)
        #     print j.name
        # print child
        # print type(child)
        # print "*************"
        print len(child)
        parent_details.append(len(child))
        parent_details.append(child)
        service_parent.append(parent_details)

        # print "**************"
    print service_parent

    # return HttpResponse("admin_services")
    return render_to_response('admin/services_all.html',
        {"service_parent":service_parent},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def admin_subservices(request,u_id):
    print u_id
    print "admin_sub_services"
    service=Services.objects.filter(id=u_id)
    # service_name=[]
    for s in service:
        print s.name
    service_name=s.name
    sub=Services.objects.filter(pid=u_id)
    sub_service=[]
    for i in sub:
        sub_list=[]
        print i.name
        print i.id
        sub_list.append(i.name)
        sub_list.append(i.id)
        child=[]
        service_child=Services.objects.filter(pid=i.id)
        for j in service_child:
            # print j.id
            child.append(j.id)
        print len(child)
        sub_list.append(len(child))
        sub_service.append(sub_list)

       
        # print i.name
        # print i.id
    print sub_service
    # return HttpResponse("admin_services")
    return render_to_response('admin/services_sub.html',
        {"sub_service":sub_service,"service_name":service_name,"u_id":u_id},
        context_instance=RequestContext(request))




@login_required(login_url='/backend/login/')
def admin_subservices_two(request,u_id,s_id):
    print "admin_subservices_two"
    print ")))))))))))))"
    print u_id
    print s_id
    service_parent=Services.objects.filter(id=s_id)
    for s in service_parent:
        parent_name=s.name
        print s.name
        print s.id
        print s.pid
    print parent_name
    print "))))))))))))))))))"
    print "admin_sub_services"
    service=Services.objects.filter(id=u_id)
    # service_name=[]
    service_name=None
    for s in service:
        # print s.name
        service_name=s.name
    print "************"
    print service_name
    print "**************"
    sub=Services.objects.filter(pid=u_id)
    sub_service=[]
    for i in sub:
        sub_list=[]
        print i.name
        print i.id
        sub_list.append(i.name)
        sub_list.append(i.id)
        child=[]
        service_child=Services.objects.filter(pid=i.id)
        for j in service_child:
            # print j.id
            child.append(j.id)
        print len(child)
        sub_list.append(len(child))
        sub_service.append(sub_list)

       
        # print i.name
        # print i.id
    print sub_service
    
    print s_id
    print u_id
    # return HttpResponse("admin_services")
    return render_to_response('admin/services_sub_two.html',
        {"sub_service":sub_service,"service_name":service_name,"u_id":u_id,"s_id":s_id,"parent_name":parent_name},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def admin_subservices_three(request,u_id,s_id,p_id):
    print "admin_subservices_three"
    print "**************"
    print u_id
    print s_id
    print p_id
    print "*************"
    print "admin_sub_services"
    service_parent=Services.objects.filter(id=p_id)
    for s in service_parent:
        parent_name=s.name
        print s.name
        print s.id
        print s.pid
    print parent_name
    service_sub_parent=Services.objects.filter(id=s_id)
    for sub in service_sub_parent:
        sub_parent_name=sub.name
        print sub.name
        print sub.id
        print sub.pid
    print sub_parent_name

    service=Services.objects.filter(id=u_id)
    # service_name=[]
    for s in service:
        print s.name
    service_name=s.name
    sub=Services.objects.filter(pid=u_id)
    sub_service=[]
    for i in sub:
        sub_list=[]
        print i.name
        print i.id
        sub_list.append(i.name)
        sub_list.append(i.id)
        child=[]
        service_child=Services.objects.filter(pid=i.id)
        for j in service_child:
            # print j.id
            child.append(j.id)
        print len(child)
        sub_list.append(len(child))
        sub_service.append(sub_list)

       
        # print i.name
        # print i.id
    print sub_service
    
    print s_id
    print u_id
    print p_id
    # return HttpResponse("admin_services")
    return render_to_response('admin/services_sub_three.html',
        {"sub_service":sub_service,"service_name":service_name,"u_id":u_id,"s_id":s_id,"p_id":p_id,"parent_name":parent_name,"sub_parent_name":sub_parent_name},
        context_instance=RequestContext(request))










@login_required(login_url='/backend/login/')
def admin_addservices(request):
    print "admin_addservices"
    if request.method == 'POST':
        form=Add_ParentServieForm(request.POST)
        if form.is_valid():
        # print form
            service = request.POST.get('service_name')
            print service
            add=Services.objects.create(pid=0,name=service,status=1)
            # return HttpResponse ("successfully")
            messages.success(request, (u"New service added successfully.."))
            return redirect("/backend/services")
        else:
            print "not valid"
        # 

        # return render_to_response('admin/services_all.html',
        # {},
        # context_instance=RequestContext(request))

    else:
        form = Add_ParentServieForm()
    
    return render_to_response('admin/add-parent-service.html',
        {'form':form},
        context_instance=RequestContext(request))





@login_required(login_url='/backend/login/')
def admin_services_edit(request,u_id):
    print "admin_services_edit"
    print u_id
    edit=Services.objects.filter(id=u_id)
    for i in edit:
        print i.name
        print i.pid
        print i.id
        service_name=i.name
    #     service_id=i.id
    # print service_id

    if request.method == 'POST':
        form=Add_ParentServieForm(request.POST)
        # print form
        if form.is_valid():
            service = request.POST.get('service_name')
            print service
            print "valid"
            Services.objects.filter(id=u_id).update(name=service)
            # return HttpResponse("successfully")
            # for j in edit_service:
            #     print j.name
            # update(name=service)

            messages.success(request, (u"Service updated successfully.."))
            return redirect("/backend/services")
        else:
            print "not valid"
        
    else:
        form=Add_ParentServieForm()

    return render_to_response('admin/edit_parent-sevice.html',
        {"form":form,"service_name":service_name},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def admin_services_two_edit(request,u_id,s_id):
    print "admin_services_two_edit"
    print "*********"
    print u_id
    print s_id
    # return HttpResponse("admin_services") 
    edit=Services.objects.filter(id=u_id)
    for i in edit:
        print i.name
        print i.pid
        print i.id
        service_name=i.name
    #     service_id=i.id
    # print service_id

    if request.method == 'POST':
        form=Add_ParentServieForm(request.POST)
        # print form
        if form.is_valid():
            service = request.POST.get('service_name')
            print service
            print "valid"
            Services.objects.filter(id=u_id).update(name=service)
            # return HttpResponse("successfully")
            # for j in edit_service:
            #     print j.name
            # update(name=service)

            messages.success(request, (u"Service updated successfully.."))
            return redirect("/backend/services/%s/"%s_id)
        else:
            print "not valid"
        
    else:
        form=Add_ParentServieForm()

    return render_to_response('admin/edit-sub-service_one.html',
        {"form":form,"service_name":service_name,"s_id":s_id},
        context_instance=RequestContext(request))



@login_required(login_url='/backend/login/')
def admin_services_three_edit(request,u_id,s_id,p_id):
    print "admin_services_three_edit"
    print "*********"
    print u_id
    print s_id
    print p_id
    # return HttpResponse("admin_services") 
    edit=Services.objects.filter(id=u_id)
    for i in edit:
        print i.name
        print i.pid
        print i.id
        service_name=i.name
    #     service_id=i.id
    # print service_id

    if request.method == 'POST':
        form=Add_ParentServieForm(request.POST)
        # print form
        if form.is_valid():
            service = request.POST.get('service_name')
            print service
            print "valid"
            Services.objects.filter(id=u_id).update(name=service)
            # return HttpResponse("successfully")
            # for j in edit_service:
            #     print j.name
            # update(name=service)

            messages.success(request, (u"Service updated successfully.."))
            return redirect("/backend/services/%s/sub/%s"%(p_id,s_id))
        else:
            print "not valid"
        
    else:
        form=Add_ParentServieForm()

    return render_to_response('admin/edit-sub-service_two.html',
        {"form":form,"service_name":service_name,"p_id":p_id,"s_id":s_id},
        context_instance=RequestContext(request))






@login_required(login_url='/backend/login/')
def admin_services_del(request,u_id):
    print "admin_services_del"

    # print "shjsahgsjagk"
    print "&&&&&&&&&&&&&&&&&&&&&&&&&&"
    print u_id
    print "service deleted"
    total_id=[]
    del_service=Services.objects.filter(id=u_id)
    del_id1=None
    for i in del_service:
        del_id1=i.id
        total_id.append(del_id1)
    print "11111111111111"
    print del_id1
    print "11111111111111"
    del_service1=Services.objects.filter(pid=del_id1)
    del_id2=[]
    if del_service1:
        for j in del_service1:
            print "JJJJJJJJJJJJJJJ"
            print "id",j.id
            del_id2.append(j.id)
            total_id.append(j.id)
            print "name",j.pid
    print "222222222222222"
    print del_id2
    print "22222222222222"
    del_id3=[]
    # del_id4=[]
    if del_id2:
        for k in del_id2:
            
            del_service2=Services.objects.filter(pid=k)
            print "DDDDDDDDDDDDDDDDDDDD"
            print del_service2
            
            if del_service2:
                # del_id5=[]
                for l in del_service2:
                    
                    print l.id
                    print l.pid
                    # del_id5.append(l.id)
                    del_id3.append(l.id)
                    total_id.append(l.id)  
    del_id4=[]  
    if del_id3:
        
        for m in del_id3:
            del_service3=Services.objects.filter(pid=m)
            if del_service3:
                for n in del_service3:
                    print "OOOOOOOOOOOOO"
                    print n.id
                    print n.pid
                    del_id4.append(n.id)
                    total_id.append(n.id)
                    print ")))))))))))))))))"
    del_id5=[]
    if del_id4:
        
        for p in del_id4:
            del_service4=Services.objects.filter(pid=p)
            if del_service4:
                for q in del_service4:
                    print "QQQQQQQQQQQQQQQ"
                    print q.id
                    print q.pid
                    total_id.append(q.id)
                    del_id5.append(q.id)
    del_id6=[]
    if del_id5:
        for s in del_id5:
            del_service5=Services.objects.filter(pid=s)
            if del_service5:
                for t in del_service5:
                    print t.pid
                    print t.id
                    total_id.append(t.id)
                    del_id6.append(t.id)

    print "************"
    print del_id1
    print del_id2
    print del_id3
    print del_id4
    print del_id5
    print del_id6
    print total_id
    print "**************"
    print del_id1
    delete_records_parent=Services.objects.filter(id=del_id1).delete()
    for id in total_id:
        print id
        delete_records=Services.objects.filter(pid=id).delete()

        # for y in delete_records:
        #     print "OOOOOOOOOOOOOOO"
        #     print y.id
        #     print y.pid
        #     print y.name
        # delete_records.delete()
#     total_list=[]
#     total_list.append(del_id1)
#     total_list.append(del_id2)
#     total_list.append(del_id3)
#     total_list.append(del_id4)
#     total_list.append(del_id5)
#     total_list.append(del_id6)
#     print total_list

# #     c=del_id1+del_id2
# #     print c
# #     from itertools import chain
# # # x = [["a","b"], ["c"]]
# #     y = list(chain(total_list))
# #     print "UUUUUUUUUUUUU"
# #     print y
# #     print "UUUUUUUUUUUUUU"
#     e=del_id1.extend(del_id2)
#     print e
    # d=list(iterFlatten(total_list))
    # print d
#     import itertools
#     a = [["a","b"], ["c"]]
#     print list(itertools.chain(*a))
#     import itertools
# # a = [1,2]
# # b = ['a','b']
# #c = list(reduce(operator.add,zip(a,b))) # slow.
#     c = list(itertools.chain.from_iterable(zip(del_id1,del_id2))) # better.
#     print c

        # else:
        #     print "not"
        # print "DDDDDDDDDDDDDDDDDDDD"

    #         del_id4.append(l.id)
    #     print del_id4

    # del_id3=[]
    # for k in del_id2:
    #     del_id4=[]
    #     del_service2=Services.objects.filter(pid=k)
    #     for l in del_service2:
    #         # del_id5=[]
    #         print "pid",l.pid
    #         print "id",l.id
    #         print "name",l.name
    #         del_id4.append(l.id)
    #     del_id3.append(del_id4)
    # # del_id3.append(del_id4)
    # print "LLLLLLLLLLLLLLLLL"
    # print del_id3
    # print "LLLLLLLLLLLLLLLLL"

    # print "PPPPPPPPPPPPPPPPPPPPPPPPP"
    # del_service.delete()
    # return HttpResponse ("Service deleted")
    messages.success(request, (u"Service deleted successfully.."))
    return redirect("/backend/services")


@login_required(login_url='/backend/login/')
def admin_add_subservices(request,u_id):
    print "admin_add_subservices"
    print "&&&&&&&&&&&&&&&"
    print u_id
    print "&&&&&&&&&&&&&&"
    print "admin_add_subservices"
    s_name=Services.objects.filter(id=u_id)
    service_name=[]
    for s in s_name:
        print s.name
        print "************************"
        print s.pid
        print "**************************"
        service_name.append(s.name)
    print service_name
    print s.pid
    s_pid=None

    services=Services.objects.filter(pid=s.pid)
    service=[]

    for i in services:
        s_id=[]
        # print i.name
        s_id.append(i.id)
        s_id.append(i.name)
        service.append(s_id)
    print "WWWWWWWWWWWWWWW"
    print service
    print "WWWWWWWWWWWWWWWW"
    # s_value=[]
    if request.method == 'POST':
        print request.POST
        print "post"
        form=Add_ParentServieForm(request.POST)
        print form
        if form.is_valid():
            service_id = request.POST.get('service1')
            print service_id
            service_pid=Services.objects.filter(name=service_id)

            for i in service_pid:
                print "RETRTEWTETE"
                print i.id
                print i.name
                s_pid=i.id
                print s_id
                print "FDFSFDFSAF"
            print "((((((((((((((((((((((("
            print s_pid
            print "(((((((((((((((((((((("
            # s_value.append(service_value)
            service_name = request.POST.get('service_name')
            print service_name
            s=Services.objects.create(pid=s_pid,name=service_name,status=1)
            print s
            # print s_value
            print "*************"
            print s_pid
            print "**************"
            messages.success(request, (u"Sub service added successfully.."))
            return redirect("/backend/services/%s"%s_pid)
        else:
            print "not valid"
    else:
        form=Add_ParentServieForm()



    # return HttpResponse ("sub services")
    print "*&&&&&&&&&&&&"
    print s_pid
    print "**************"
    return render_to_response('admin/add-sub-service.html',
        {"service":service,"service_name":service_name,"form":form,"u_id":u_id},
        context_instance=RequestContext(request))


# @login_required(login_url='/backend/login/')
# def admin_add_subservices_two(request,u_id,s_id):

#     print "&&&&&&&&&&&&&&&"
#     print u_id
#     print s_id
#     print "&&&&&&&&&&&&&&"
#     print "admin_add_subservices"
#     s_name=Services.objects.filter(id=u_id)
#     service_name=[]
#     for s in s_name:
#         print s.name
#         print "************************"
#         print s.pid
#         print "**************************"
#         service_name.append(s.name)
#     print service_name
#     print s.pid
#     s_pid=None

#     services=Services.objects.filter(pid=s.pid)
#     service=[]

#     for i in services:
#         s_id=[]
#         # print i.name
#         s_id.append(i.id)
#         s_id.append(i.name)
#         service.append(s_id)
#     print "WWWWWWWWWWWWWWW"
#     print service
#     print "WWWWWWWWWWWWWWWW"
#     # s_value=[]
#     if request.method == 'POST':
#         print request.POST
#         print "post"
#         form=Add_ParentServieForm(request.POST)
#         print form
#         if form.is_valid():
#             service_id = request.POST.get('service1')
#             print service_id
#             service_pid=Services.objects.filter(name=service_id)

#             for i in service_pid:
#                 print "RETRTEWTETE"
#                 print i.id
#                 print i.name
#                 s_pid=i.id
#                 print s_id
#                 print "FDFSFDFSAF"
#             print "((((((((((((((((((((((("
#             print s_pid
#             print "(((((((((((((((((((((("
#             # s_value.append(service_value)
#             service_name = request.POST.get('service_name')
#             print service_name
#             s=Services.objects.create(pid=s_pid,name=service_name,status=1)
#             print s
#             # print s_value
#             print "*************"
#             print s_pid
#             print s_id
#             print u_id
#             print "**************"
#             print "IRI"
#             messages.success(request, (u"Sub service added successfully.."))
#             return redirect("/backend/services/2/sub/30/")
#         else:
#             print "not valid"
#     else:
#         form=Add_ParentServieForm()



#     return HttpResponse ("sub services")
#     # print "*&&&&&&&&&&&&"
#     # print s_pid
#     # print "**************"
#     # return render_to_response('admin/add-sub-service.html',
#     #     {"service":service,"service_name":service_name,"form":form,"u_id":u_id},
#     #     context_instance=RequestContext(request))






@login_required(login_url='/backend/login/')
def admin_add_subservices_two(request,u_id,s_id):
    print "admin_add_subservices_two"
    print "&&&&&&&&&&&&&&&"
    print u_id
    print s_id
    print "&&&&&&&&&&&&&&"
    print "admin_add_subservices"
    s_name=Services.objects.filter(id=u_id)
    service_name=[]
    for s in s_name:
        print s.name
        print "************************"
        print s.pid
        print "**************************"
        service_name.append(s.name)
    print service_name
    print s.pid
    s_pid=None
    services=Services.objects.filter(pid=s.pid)
    service=[]

    for i in services:
        service_id=[]
        # print i.name
        service_id.append(i.id)
        service_id.append(i.name)
        service.append(service_id)
    print service
    # s_value=[]
    print u_id
    print s_id
    if request.method == 'POST':

        print request.POST
        print "post"
        form=Add_ParentServieForm(request.POST)
        print form
        if form.is_valid():
            service_id = request.POST.get('service1')
            print service_id
            service_pid=Services.objects.filter(name=service_id)

            for i in service_pid:
                print "RETRTEWTETE"
                print i.id
                print i.name
                s_pid=i.id
                print s_id
                print "FDFSFDFSAF"
            print "((((((((((((((((((((((("
            print s_pid
            print "(((((((((((((((((((((("
            # s_value.append(service_value)
            service_name = request.POST.get('service_name')
            print service_name
            s=Services.objects.create(pid=s_pid,name=service_name,status=1)
            print s
            # print s_value
            print "*************"
            print s_pid
            print s_id
            print u_id
            print "**************"
            messages.success(request, (u"Sub service added successfully.."))
            return redirect("/backend/services/%s/sub/%s/"%(s_id,s_pid))

        else:
            print "not valid"
    else:
        form=Add_ParentServieForm()


    # return HttpResponse ("sub services")
    print "((((((((((((((()_____________________-"
    print u_id
    print s_id
    return render_to_response('admin/add-sub-service_two.html',
        {"service":service,"service_name":service_name,"form":form,"s_id":s_id,"u_id":u_id},
        context_instance=RequestContext(request))








@login_required(login_url='/backend/login/')
def admin_add_subservices_three(request,u_id,s_id,p_id):
    print "admin_add_subservices_three"
    print "*(((((((((("
    print s_id
    print u_id
    print p_id
    print "&&&&&&&&&&&&&&&"
   
    print "&&&&&&&&&&&&&&"
    print "admin_add_subservices"
    s_name=Services.objects.filter(id=p_id)
    service_name=[]
    for s in s_name:
        print s.name
        print "************************"
        print s.pid
        print "**************************"
        service_name.append(s.name)
    print service_name
    print s.pid

    services=Services.objects.filter(pid=u_id)
    service=[]

    for i in services:
        service_id=[]
        # print i.name
        service_id.append(i.id)
        service_id.append(i.name)
        service.append(service_id)
    print service
    # s_value=[]
    print u_id
    print s_id
    if request.method == 'POST':

        print request.POST
        print "post"
        form=Add_ParentServieForm(request.POST)
        print form
        if form.is_valid():
            service_id = request.POST.get('service1')
            print service_id
            service_pid=Services.objects.filter(name=service_id)

            for i in service_pid:
                print "RETRTEWTETE"
                print i.id
                print i.name
                s_pid=i.id
                print s_id
                print "FDFSFDFSAF"
            print "((((((((((((((((((((((("
            print s_pid
            print "(((((((((((((((((((((("
            # s_value.append(service_value)
            service_name = request.POST.get('service_name')
            print service_name
            s=Services.objects.create(pid=s_pid,name=service_name,status=1)
            print s
            # print s_value
            print "*************"
            print s_pid
            print s_id
            print u_id
            print "**************"
            messages.success(request, (u"Sub service added successfully.."))
            return redirect("/backend/services/%s/sub/%s/"%(s_id,s_pid))

        else:
            print "not valid"
    else:
        form=Add_ParentServieForm()


    # return HttpResponse ("sub services")
    print u_id
    print s_id
    print "**********"
    print service_name
    print "***************"
    return render_to_response('admin/add-sub-service_three.html',
        {"service":service,"service_name":service_name,"form":form,"s_id":s_id,"p_id":p_id,"u_id":u_id},
        context_instance=RequestContext(request))

























@login_required(login_url='/backend/login/')
def admin_subservices_edit(request,u_id):
    print "admin_subservices_edit"
    print u_id
    edit=Services.objects.filter(id=u_id)
    for i in edit:
        print i.name
        s_pid=i.pid
        print i.pid
        print i.id
        service_name=i.name

    if request.method == 'POST':
        form=Add_ParentServieForm(request.POST)
        # print form
        if form.is_valid():
            service = request.POST.get('service_name')
            print service
            print "valid"
            Services.objects.filter(id=u_id).update(name=service)
            # return HttpResponse("successfully")
            # for j in edit_service:
            #     print j.name
            # update(name=service)
            print s_pid
            messages.success(request, (u"Sub service updated successfully.."))
            return redirect("/backend/services/sub/%s"%s_pid)
        else:
            print "not valid"
        
    else:
        form=Add_ParentServieForm()
    return render_to_response('admin/edit-sub-service.html',
        {"form":form,"service_name":service_name},
        context_instance=RequestContext(request))


@login_required(login_url='/backend/login/')
def admin_subservices_del(request,u_id):
    print "shjsahgsjagk"
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print u_id
    print "service deleted"
    # del_service=Services.objects.filter(id=u_id)
    # del_service.delete()
    return redirect("/")
    print "firaitvfktjie"
    # return HttpResponse ("Service deleted")
    messages.success(request, (u"Service deleted successfully.."))
    return redirect("/backend/services")








@login_required(login_url='/backend/login/')
def addservices(request):

    return HttpResponse("service added successfully")




