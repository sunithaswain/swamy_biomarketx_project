from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User


class AdminLoginform(forms.Form):    
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "form-control input-lg",}),
        label='Password'
    )

# class LabUserForm(forms.Form):
# 	name = forms.TextInput


class UserForm(forms.Form): 
    # username =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))     
    first_name =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    last_name=forms.CharField(max_length=250,required="false",widget=forms.TextInput(attrs={'class': "form-control input-lg"}))
    # name_org=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',error_message = 
    #                             ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
    #                             widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # how_bio=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    #active_status = forms.BooleanField()

class LabUserForm(forms.Form): 
    error_css_class = 'error'
    # username =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))    	
    # first_name =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # last_name=forms.CharField(max_length=250,required="false",widget=forms.TextInput(attrs={'class': "form-control input-lg"}))
    # name_org=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',error_message = 
    #                             ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
    #                             widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # name_org =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'XYZ inc'}))
    # how_bio=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    #active_status = forms.BooleanField()

    
    #first_name =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font error-msg ","placeholder":'Bio'}))
    first_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='First Name'
    )

    last_name=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'Marketex'}))  
   
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'test@abc.com'}))
    #orgname =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'XYZ inc'}))
    name_org = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Organization Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
        label='Title'
    )    
   

class ResearcherForm(forms.Form): 
    # # username =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))     
    # first_name =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # last_name=forms.CharField(max_length=250,required="false",widget=forms.TextInput(attrs={'class': "form-control input-lg"}))
    # name_org=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',error_message = 
    #                             ("Phone number must be entered in the format: '312-567-8912 (US) or 55-11-3312-3412 (Int'l)'"),
    #                             widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # how_bio=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg",}))
    # active_status = forms.BooleanField()
    first_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("First Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'abc'}),
        label='First Name'
    )

    last_name=forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'Marketex'}))  
   
    phone_number = forms.RegexField(regex=r'^(([1-9]{1})[0-9]{9})$',
                                error_message = ("Phone number must be 10 digits."),
                                widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'123-456-8911',"max-length" :10}))

    email = forms.EmailField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'test@abc.com'}))
    #orgname =forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control input-lg input-font","placeholder":'XYZ inc'}))
    name_org = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{3,}$',
        error_message = ("Organization Name must be minimum 3 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'xyz'}),
        label='Title'
    )    




class Add_ParentServieForm(forms.Form): 
    service_name = forms.RegexField(regex=r'^[A-Za-z0-9\w @%._-]{4,}$',
        error_message = ("Service Name must be minimum 4 characters."),
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control input-lg","placeholder":'biom'}),
        label='service name'
    )