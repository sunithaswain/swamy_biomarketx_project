from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User
from .models import *

class Registrationform(forms.Form):
    error_css_class = "error"
    #first_name =forms.CharField(min_length=3,max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'first name'}))
    first_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='First Name'
    )

    last_name=forms.CharField(min_length=3,max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'last name'}))
    
    # last_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
    #     error_message = ("Last Name must be minimum 3 characters."),
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
    #     label='Last Name'
    # )

    password = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
        error_message = ("Password must be minimum 6 characters."),
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password'
    )
                                
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    # phone_number = forms.RegexField(regex=r'^((\d{1,4}[- ]\d{1,3})|(\d{2,3}))[- ](\d{3,4})[- ](\d{4})',
    #                             error_message = 
    #                             ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
    #                             widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'312-567-8912'}))
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))
    how_bio=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    #companey=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    companey = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Company Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Bio'}),
        label='Company'
    )    

    position=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))


class Lab_registrationform(forms.Form):
    error_css_class = 'error'
    
    #first_name =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font error-msg ","placeholder":'Bio'}))
    first_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='First Name'
    )

    last_name=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'Marketex'}))
    # last_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
    #     error_message = ("Last Name must be minimum 3 characters."),
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
    #     label='Last Name'
    # )
    


    #title = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'Principal Investigator'}))

    title = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Title must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
        label='Title'
    )
   
    password = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
        error_message = ("Password must be minimum 6. "),
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg input-font",}),
        label='Password'

    )
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'test@abc.com'}))
    #orgname =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'XYZ inc'}))
    orgname = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Organization Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
        label='Title'
    )

    
    #facility=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'ABC Core'}))
    facility = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Core facility must be minimum 3 characters."),
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
        label='facility'
    )
    
    #service_cap = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 3,"placeholder":'This is about Description'}))
    
    service_cap = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Lab Description must be minimum 10 characters."),
        required=True,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 3,"placeholder":'Lab Description'}),
        label='service_cap'
    )
    

    #how_bio=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'Google',}))
    how_bio = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Organization Name must be minimum 3 characters."),
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
        label='how_bio'
    )


class Loginform(forms.Form):    
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password'
    )

class Editprofileform(forms.Form):    
    first_name =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    last_name=forms.CharField(max_length=250,required="false",widget=forms.TextInput(attrs={'class': "form-control input-lg"}))
    name_org=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    phone_number = forms.RegexField(regex=r'^((\d{1,4}[- ]\d{1,3})|(\d{2,3}))[- ](\d{3,4})[- ](\d{4})',
                                error_message = 
                                ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    how_bio=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))


class Lablistingform(forms.Form):    
    Title=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    Caption = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    Desc = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg",'rows': 3,}))
    country = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    #logo= forms.FileField(widget=forms.FileInput(attrs={'class': "form-control input-lg",}))


class AddLabservicesform(forms.Form):    
    service_title=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # service_title=forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
    #     error_message = ("Provider Service Name must be minimum 6 characters."),
    #     required=True,
    #     max_length=250,
    #     widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Service'}),
    #     # label='First Name'
    # )
    service_desc = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg",'rows': 3,}))
    service_price = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    service_currency = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    service_unit = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))   
    service_url = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))

class Labreviewsform(forms.Form):    
    Desc = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg",'rows': 3,}))


class Labendorseform(forms.Form):    
    Desc = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg",'rows': 3,}))


# class EditLabform(forms.Form):    
#     orgname =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'}))
#     title = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Principal Investigator'}))
#     service_cap = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg",'rows': 3,"placeholder":'This is about Description'}))
#     logo=forms.ImageField(required=False)


class LabphotosForm(forms.ModelForm):
    class Meta:
        model = Labphotos
        fields = ('photo',)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()






# class EditLabform(forms.ModelForm):
#     class Meta:
#         model = Lab
#         fields = ('orgname','title','desc','logo')

#     def __init__(self, *args, **kwargs):
#         super(EditLabform, self).__init__(*args, **kwargs)
#         self.fields['orgname'].widget = forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'})
#         self.fields['title'].widget = forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'})
#         self.fields['orgname'].widget = forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'})
#         self.fields['orgname'].widget = forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'})
class EditResearcherForm(forms.Form):
    error_css_class = "error"
    #first_name =forms.CharField(min_length=3,max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'first name'}))
    first_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='First Name'
    )

    last_name=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'last name'}))
    
    
                               
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    # phone_number = forms.RegexField(regex=r'^((\d{1,4}[- ]\d{1,3})|(\d{2,3}))[- ](\d{3,4})[- ](\d{4})',
    #                             error_message = 
    #                             ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
    #                             widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'312-567-8912'}))
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))
    #companey=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    companey = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Company Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Bio'}),
        label='Company'
    )    

    Desc = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Lab Description must be minimum 10 characters"),
        required=False,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Researcher Description'}),
        label='service_cap'
    )
    image = forms.ImageField(required=False,)

class EditPasswordForm(forms.Form):
    password1 = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
        error_message = ("New Password must be minimum 6 characters."),
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password2'
    )
    
    password2 = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
        error_message = ("Confirm New Password must be minimum 6 characters."),
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password2'
    )

class ResearcherEducationForm(forms.Form):
    error_css_class = "error"
    #first_name =forms.CharField(min_length=3,max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'first name'}))
    institute = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Institution must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Institution'}),
        label='Institution'
    )
    degree = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Degree must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Degree'}),
        label='Degree'
    )
    field_study = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Field of Study must be minimum 3 characters"),
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Field of Study'}),
        label='Field of Study'
    )
    notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Notes'}),)
    # notes = forms.RegexField(regex=r'^[A-Za-z0-9\w  @%._-]{10,}$',
    #     error_message = ("Notes must be minimum 10 characters"),
    #     required=False,
    #     widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Notes'}),
    #     label='Notes'
    # )


class ResearcherEmploymentForm(forms.Form):
    error_css_class = "error"
    #first_name =forms.CharField(min_length=3,max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'first name'}))
    employer = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Employer must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Employer'}),
        label='Institution'
    )
    title = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Title must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Title'}),
        label='Degree'
    )
    notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Notes'}),)


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    error_css_class = "error"
    #first_name =forms.CharField(min_length=3,max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'first name'}))
    first_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='First Name'
    )

    last_name=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'last name'}))
    
    
                               
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    # phone_number = forms.RegexField(regex=r'^((\d{1,4}[- ]\d{1,3})|(\d{2,3}))[- ](\d{3,4})[- ](\d{4})',
    #                             error_message = 
    #                             ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
    #                             widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'312-567-8912'}))
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))
    #companey=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    companey = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Company Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Bio'}),
        label='Company'
    )    

    Desc = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Lab Description must be minimum 10 characters"),
        required=False,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Researcher Description'}),
        label='service_cap'
    )

class PublicationsForm(forms.Form):
    publications =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'publications'}))



class upload_image(forms.Form):
    photo = forms.ImageField()

# class UploadImageForm(forms.ModelForm):
#     class Meta:
#         model = LabProfilepic
#         fields=("model_pic",)

class UploadImage(forms.ModelForm):
    class Meta:
        model = Profilepic
        fields=("model_pic",)



class EditLabform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditLabform, self).__init__(*args, **kwargs)
        self.fields['desc'].required = False
   
    class Meta:
        model = Lab   
        fields=("orgname","title","desc","model_pic", "city","state", "country",)
        # widgets = {
        #     # 'username' : forms.TextInput(attrs = {'placeholder': 'Username'}),
        #     # 'email'    : forms.TextInput(attrs = {'placeholder': 'E-Mail'}),
        #     'model_pic' : forms.ImageField(attrs = {'required'="false",}),

        # }
    # def __init__(self, *args, **kwargs):
    #     super(EditLabform, self).__init__(*args, **kwargs)

    #     for key in self.fields:
    #         print "###"
    #         print "Edit lab form"
    #         print key
    #         self.fields[key].required = False
    # orgname =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'}))
    # title = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'Principal Investigator'}))
    # service_cap = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg",'rows': 3,"placeholder":'This is about Description'}))
    # logo=forms.ImageField(required=False)


class SearchingForm(forms.Form):   

    search_word =  forms.CharField(max_length=200)

class SendQuote_loggedinForm(forms.Form):
    error_css_class = "error"
    Desc = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Quote Description must be minimum 10 characters"),
        required=True,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Researcher Description'}),
        label='service_cap'
    )
    send_file = forms.FileField(required=False,)


class SendQuote_not_loginForm(forms.Form):
    error_css_class = "error"
    Desc = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Quote Description must be minimum 10 characters"),
        required=True,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Researcher Description'}),
        label='service_cap'
    )
    send_file = forms.FileField(required=False,)

    email = forms.EmailField(max_length=250,required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))
    password1 = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
        error_message = ("Password must be minimum 6 characters."),
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password1'
    )
  
    password2 = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{6,}$',
        error_message = ("Confirm New Password must be minimum 6 characters."),
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password2'
        )
class LabQuoteForm(forms.Form):
    error_css_class = "error"
    service_price = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    duration=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'15 Days'}))

    # notes = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
    #     error_message = ("Quote Notes must be minimum 10 characters"),
    #     required=True,
    #     widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 10,"placeholder":'Researcher Description'}),
    #     label='service_cap'
    # )
    send_file = forms.FileField(required=False,)



import datetime
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

# from django_messages.models import Message
# from django_messages.fields import CommaSeparatedUserField

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = forms.CharField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=120,required=False)
    body = forms.CharField(label=_(u"Body"),required=False,
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55','class':"note-codable",'name':"body"}))
    
        
    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
    
                
    def save(self, sender,recpt,body1, parent_msg=None):
        print "save method"
        print recpt
        # recipients = self.cleaned_data['recipient']
        recipients = []
        recipients.append(recpt)
        print "$$$$$$$$$$$$$$$"
        print recipients
        print type(recipients)
        print "####"*15
        subject = self.cleaned_data['subject']
        # body = self.cleaned_data['body']
        body = body1  
        print " before save"     
        print body      
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                subject = subject,
                body = body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = datetime.datetime.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg,})
                    notification.send([r], "messages_reply_received", {'message': msg,})
                else:
                    notification.send([sender], "messages_sent", {'message': msg,})
                    notification.send([r], "messages_received", {'message': msg,})
        return message_list

class ContactUsForm(forms.Form):
    error_css_class = "error"
    
    name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='Name'
    )    

    email=forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))

    subject = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Subject Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='SubjectName'
    )    

    message= forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Message must be minimum 10 characters"),
        required=True,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 3,"placeholder":'How Can We Help'}),
        label='service_cap'
    )



class SplRequestForm(forms.Form):
    error_css_class = "error"
    
    name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='Name'
    )    

    email=forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'test@abc.com'}))

    university = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("University Name must be minimum 3 characters"),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='University'
    )    

    desc= forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{10,}$',
        error_message = ("Description must be minimum 10 characters"),
        required=True,
        widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 3,"placeholder":'How Can We Help'}),
        label='service_cap'
    )

    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))


class WorkroomForm(forms.Form):
    description=forms.CharField(widget=forms.Textarea(attrs={'class': "form-control input-lg input-font",'rows': 3,"placeholder":'This is about Description'}))
    send_file = forms.FileField(required=False,)

class about_editForm(forms.Form): 
    # username =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))     
    Description=forms.CharField(max_length=10000)