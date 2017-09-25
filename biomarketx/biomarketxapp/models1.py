from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


# Create your models here.
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = False
# Create your models here.
class Userroles(models.Model):
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    roll_name=models.CharField(max_length=250)
    status =models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Users(models.Model):
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    fname = models.CharField(max_length=250)
    lname = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=15)
    how_bio = models.CharField(max_length=250,blank=True)
    name_org = models.CharField(max_length=250,blank=True)
    username = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      get_latest_by = 'created_at'

class Researcher_more_info(models.Model):
    user_id = models.IntegerField()
    desc=models.TextField()
    publications=models.CharField(max_length=250)
    model_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

class Researcher_education(models.Model):
    user_id = models.IntegerField()
    institute=models.CharField(max_length=250,blank=True)
    degree=models.CharField(max_length=250,blank=True)
    field_study=models.CharField(max_length=250,blank=True)
    study_start=models.CharField(max_length=250,blank=True)
    study_stop=models.CharField(max_length=250,blank=True)
    study_continue=models.CharField(max_length=250,blank=True)
    notes=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


class Researcher_emplyment(models.Model):
    user_id = models.IntegerField()
    employer=models.CharField(max_length=250,blank=True)
    title=models.CharField(max_length=250,blank=True)
    study_start=models.CharField(max_length=250,blank=True)
    study_stop=models.CharField(max_length=250,blank=True)
    study_continue=models.CharField(max_length=250,blank=True)
    month_start=models.CharField(max_length=250,blank=True)
    month_stop=models.CharField(max_length=250,blank=True)
    notes=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


class Researcher_publications(models.Model):
    user_id = models.IntegerField()
    title=models.CharField(max_length=500,blank=True)
    scientist_name=models.CharField(max_length=250,blank=True)
    used_for=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


class Publications(models.Model):
    title=models.CharField(max_length=500,blank=True)
    scientist_name=models.CharField(max_length=250,blank=True)
    used_for=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Services(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=300)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField()

class Lab(models.Model):
    #user = models.ForeignKey(Users)
    user_id = models.IntegerField()
    service_id = models.IntegerField(null=True)
    title = models.CharField(max_length=500,blank=True)
    caption = models.CharField(max_length=250,blank=True)
    orgname =models.CharField(max_length=250,blank=True)
    typeorg=models.CharField(max_length=250,blank=True)
    core_facility = models.CharField(max_length=250,blank=True)
    desc = models.TextField()
    # logo = models.ImageField(null=True, blank=True,upload_to="/media")
    model_pic = models.ImageField(upload_to="images", null=True, blank=True)
    city=models.CharField(max_length=250,blank=True)
    state=models.CharField(max_length=250,blank=True)
    country = models.CharField(max_length=250,blank=True)
    # labservices_id = models.IntegerField()
    # labendorse_id = models.IntegerField()
    # labreviews_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LabServices(models.Model):
    #lab_id = models.ForeignKey(Lab)
    #service_id = models.ForeignKey(Service)
    lab_id = models.IntegerField()
    title = models.CharField(max_length=500,blank=True)
    price = models.FloatField()
    currency = models.CharField(max_length=500,blank=True)
    unit = models.CharField(max_length=500,blank=True)
    desc = models.TextField()
    url=models.CharField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LabEndorse(models.Model):
    #lab_id = models.ForeignKey(Lab)
    #service_id = models.ForeignKey(Service)
    lab_id = models.IntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LabReviews(models.Model):
    #lab_id = models.ForeignKey(Lab)
    #service_id = models.ForeignKey(Service)
    lab_id = models.IntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LabMembers(models.Model):
    lab = models.ForeignKey(Lab)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Countries(models.Model):
    country_name = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)

class Notifications(models.Model):
    user_id = models.ForeignKey(Users)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Experiment(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    experiment=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Lab_type(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    lab_type=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Parent_organization(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    organization=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class species(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    species=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Certifications(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    certifications=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Equipment(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    equipment=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reagents(models.Model):
    user_id = models.ForeignKey(Users)
    lab_id = models.ForeignKey(Lab)
    reagents=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Labphotos(models.Model):
    # user_id = models.IntegerField()
    # lab_id = models.IntegerField()
    photo = models.FileField(upload_to="Lab-photos")


class Profilepic(models.Model):
    user_id=models.IntegerField(null=True)
    model_pic = models.ImageField(upload_to = 'pic_folder/', null=True, blank=True)



class Labkeywords(models.Model):
    lab_keywords=models.TextField(max_length=250)

class Book(models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField()

class Quotes(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    sid=models.CharField(max_length=250,blank=True)
    researcher_id=models.IntegerField()
    researcher_name=models.CharField(max_length=250,blank=True)
    lab_id=models.IntegerField()
    service_id=models.IntegerField(null=True)
    service_name=models.CharField(max_length=250,blank=True)
    desc=models.TextField()
    notes=models.TextField()
    price=models.FloatField(null=True)
    duration=models.CharField(max_length=250,blank=True)
    memo=models.CharField(max_length=250,blank=True)
    status_id=models.IntegerField()    
    sent_by=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quotes_msgs(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    quote_id=models.IntegerField()
    body=models.TextField()
    msg_status=models.CharField(max_length=250)#new,trash,sent
    sender_id=models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quote_files(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    quote_id=models.IntegerField()
    filename=models.FileField(upload_to="quotes")
    sent_by=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quote_payments(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    quote_id=models.IntegerField()
    amount=models.FloatField()
    customer=models.CharField(max_length=250,blank=True)
    charge_id=models.CharField(max_length=250,blank=True)
    status=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Quote_status(models.Model):
    quote_id=models.IntegerField(null=True)#AUTO_INCREMENT
    name=models.CharField(max_length=250)
    description=models.CharField(max_length=500)
    status_id=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Orders(models.Model):
    # id=models.IntegerField()#AUTO_INCREMENT
    sid=models.CharField(max_length=250,blank=True)
    researcher_id=models.IntegerField()
    researcher_name=models.CharField(max_length=250,blank=True)
    lab_id=models.IntegerField()
    service_id=models.IntegerField(null=True)
    service_name=models.CharField(max_length=250,blank=True)
    desc=models.TextField()
    notes=models.TextField()
    price=models.FloatField(null=True)
    duration=models.CharField(max_length=250,blank=True)
    memo=models.CharField(max_length=250,blank=True)
    status_id=models.IntegerField()    
    sent_by=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order_msgs(models.Model):
    # id=models.IntegerField()#AUTO_INCREMENT
    order_id=models.IntegerField()
    body=models.TextField()
    msg_status=models.CharField(max_length=250)#new,trash,sent
    sender_id=models.IntegerField()

class order_files(models.Model):
    # id=models.IntegerField()#AUTO_INCREMENT
    order_id=models.IntegerField()
    filename=models.FileField(upload_to="quotes")
    sent_by=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class order_payments(models.Model):
    # id=models.IntegerField()#AUTO_INCREMENT
    order_id=models.IntegerField()
    amount=models.FloatField()
    status=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class order_status(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    order_id=models.IntegerField(null=True)#AUTO_INCREMENT
    name=models.CharField(max_length=250)
    description=models.CharField(max_length=500)
    status_id=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ContactUS(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    name=models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    subject=models.CharField(max_length=250)
    messages=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SplRequest(models.Model):
    #id=models.IntegerField()#AUTO_INCREMENT
    contact_via=models.CharField(max_length=250,blank=True)
    name=models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    university=models.CharField(max_length=250)
    desc=models.TextField()
    phone_number=models.CharField(max_length=15,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """

        print "inbox"
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
            buyer_display_status__isnull=True,
        )

    def inbox_for_provider(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """

        print "inbox"
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
            provider_display_status__isnull=True,
        )
    

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        print "outbox"
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        print "trash"
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


class Message(models.Model):
    """
    A private message from user to user
    """
    subject = models.CharField(_("Subject"), max_length=120)
    body = models.TextField(_("Body"))
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name=_("Sender"))
    recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', null=True, blank=True, verbose_name=_("Recipient"))
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"))
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender_deleted_at = models.IntegerField(_("Sender deleted at"), null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)
    # trash_status = models.IntegerField(_("trash_status"),null=True)
    provider_sent_status = models.IntegerField(_("provider_sent_status"),null=True)
    buyer_display_status = models.IntegerField(_("buyer_display_status"),null=True)
    provider_display_status = models.IntegerField(_("provider_display_status"),null=True)
    
    objects = MessageManager()
    
    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True
        
    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False
    
    def __unicode__(self):
        return self.subject
    
    def get_absolute_url(self):
        return ('messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs) 
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        
def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()

# fallback for email notification if django-notification could not be found
# if "notification" not in settings.INSTALLED_APPS:
#     from django_messages.utils import new_message_email
#     signals.post_save.connect(new_message_email, sender=Message)


class Workroom(models.Model):
    description=models.TextField()
    user_id=models.IntegerField(null=True)
    user_role=models.CharField(max_length=250,blank=True)
    order_id=models.IntegerField(null=True)
    name=models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class workroom_files(models.Model):
    order_id=models.IntegerField(null=True)
    workroom_id=models.IntegerField(null=True)
    filename=models.FileField(upload_to="quotes")

class edit_about(models.Model):
    # id=models.IntegerField()#AUTO_INCREMENT
    # order_id=models.IntegerField()
    data=models.TextField()