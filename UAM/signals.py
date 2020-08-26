import datetime
import pytz
from django.db.models.signals import post_save
from django_registration.signals import user_activated
from django.contrib.auth.signals import user_logged_in, user_logged_out
from attendance_tracker.models import UserProfile
from django.dispatch import receiver
from UAM.models import Subscription

# post_save documentation https://docs.djangoproject.com/en/3.0/ref/signals/
@receiver(post_save, sender=UserProfile)
def initiate_subscription(sender, instance, created, **kwargs):
	if created:
		Subscription.objects.create(user=instance, begun=instance.date_joined, subscribed=True)

# Saves the Subscription opject that was created above
@receiver(post_save, sender=UserProfile)
def save_subscription(sender, instance, **kwargs):
	instance.subscription.save()

# user_logged_in documentation https://docs.djangoproject.com/en/3.0/ref/contrib/auth/
@receiver(user_logged_in, sender=UserProfile)
def update_modified_date_login(sender, user, request, **kwargs):
	temp = Subscription.objects.get(user=user)
	temp.modified = pytz.UTC.localize(datetime.datetime.now())
	temp.save()
	if(temp.subscribed == False):
		temp.user.set_license('NoLi')
		temp.user.save() 

#user_logged_out documentation https://docs.djangoproject.com/en/3.0/ref/contrib/auth/ 
@receiver(user_logged_out, sender=UserProfile)
def update_modified_date_logout(sender, user, request, **kwargs):
	temp = Subscription.objects.get(user=user)
	temp.modified = pytz.UTC.localize(datetime.datetime.now())
	temp.save()
	if(temp.subscribed == False):
		temp.user.set_license('NoLi')
		temp.user.save() 




