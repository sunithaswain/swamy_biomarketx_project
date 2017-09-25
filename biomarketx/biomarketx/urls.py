"""biomarketx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include('biomarketxapp.urls', namespace="bioapp")),
    url(r'^accounts/', include('allauth.urls')),   
    url(r'^backend/', include('backend.urls', namespace="backend")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')), 
    # url(r'^messages/', include('django_messages.urls')),
    url(r'^__alohaeditor__/', include('aloha_editor.urls', namespace='aloha_editor')),

    #url(r'^editor/', include('demo_application.urls')),
    #url(r'^editor$', ckeditor_form_view, name='ckeditor-form'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 

