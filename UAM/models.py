import datetime
import pytz
from django.utils import timezone
from django.db import models
from attendance_tracker.models import UserProfile

class Subscription(models.Model):
	user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
	begun = models.DateTimeField(default=timezone.now)
	modified = models.DateTimeField(default=timezone.now)
	expired = models.DateTimeField(default=timezone.now)
	subscribed = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		self.expired = self.begun+datetime.timedelta(days=30)

		if(self.modified >= self.expired):
			self.subscribed = False
		else:
			self.subscribed = True

		return super(Subscription, self).save(*args, **kwargs)
