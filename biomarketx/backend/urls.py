from django.conf.urls import url
from . import views

urlpatterns = [
    
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.main, name='main'),
    url(r'^login/$', views.admin_login, name='admin_login'),
    url(r'^logout/$', views.admin_logout, name='admin_logout'),
    url(r'^profile/$', views.admin_profile, name='admin_profile'),
    url(r'^users/$', views.users, name='users'),
    url(r'^index/$', views.admin_index, name='admin_index'),
    url(r'^providers/$', views.labusers, name='labusers'),
    url(r'^buyers/$', views.researchers, name='researchers'),
    url(r'^providers/edit/(?P<l_id>[A-Za-z0-9\w@%._-]+)/$', views.edit_labusers, name='edit_labusers'),
    url(r'^users/edit/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.edit_users, name='edit_users'),
    url(r'^users/del/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.del_users, name='del_users'),
    url(r'^providers/del/(?P<l_id>[A-Za-z0-9\w@%._-]+)/$', views.del_labusers, name='del_labusers'),
    url(r'^buyers/edit/(?P<r_id>[A-Za-z0-9\w@%._-]+)/$', views.edit_researchers, name='edit_researchers'),
    url(r'^buyers/del/(?P<r_id>[A-Za-z0-9\w@%._-]+)/$', views.del_researchers, name='del_researchers'),
    url(r'^services/$', views.admin_services, name='admin_services'),
    url(r'^services/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_subservices, name='admin_subservices'),
    url(r'^service/add/$', views.admin_addservices, name='admin_addservices'),
    url(r'^addservices/$', views.addservices, name='addservices'),
    url(r'^service/edit/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_services_edit, name='admin_services_edit'),
    url(r'^service/del/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_services_del, name='admin_services_del'),
    url(r'^service/(?P<u_id>[A-Za-z0-9\w@%._-]+)/add/$', views.admin_add_subservices, name='admin_add_subservices'),
    url(r'^service/sub/edit/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_subservices_edit, name='admin_subservices_edit'),
    url(r'^service/sub/del/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_subservices_del, name='admin_subservices_del'),
    # url(r'^admin_subservices_two/$', views.admin_subservices_two, name='admin_subservices_two'),
    url(r'^services/(?P<s_id>[A-Za-z0-9\w@%._-]+)/sub/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_subservices_two, name='admin_subservices_two'),
    url(r'^services/(?P<p_id>[A-Za-z0-9\w@%._-]+)/sub/(?P<s_id>[A-Za-z0-9\w@%._-]+)/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_subservices_three, name='admin_subservices_three'),
    url(r'^service/add/(?P<s_id>[A-Za-z0-9\w@%._-]+)/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_add_subservices_two, name='admin_add_subservices_two'),
    url(r'^service/add/(?P<s_id>[A-Za-z0-9\w@%._-]+)/(?P<u_id>[A-Za-z0-9\w@%._-]+)/(?P<p_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_add_subservices_three, name='admin_add_subservices_three'),
    url(r'^service/edition/(?P<s_id>[A-Za-z0-9\w@%._-]+)/(?P<u_id>[A-Za-z0-9\w@%._-]+)$', views.admin_services_two_edit, name='admin_services_two_edit'),
    url(r'^service/editions/(?P<p_id>[A-Za-z0-9\w@%._-]+)/(?P<s_id>[A-Za-z0-9\w@%._-]+)/(?P<u_id>[A-Za-z0-9\w@%._-]+)/$', views.admin_services_three_edit, name='admin_services_three_edit'),


]




