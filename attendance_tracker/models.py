from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from attendance_tracker.managers import CustomUserManager

LICENSES = [('NoLi', 'No License'), ('Standard','Standard License'), ('Professional','Professional License'),('Ultimate','Ultimate License')]
SECTION = [('Morning','Morning'), ('Afternoon','Afternoon'), ('Evening','Evening')]
ACTIVITY = [('Liturgy','Liturgy'), ('Bible Study','Bible Study'), ('Sunday School', 'Sunday School'), ('Field Trip', 'Field Trip'), ('Mahragan', 'Mahragan'), ('GameDay', 'Game Day'), ('Theater', 'Theater'), ('Choir', 'Choir'), ('Hymns', 'Hymns'), ('Coptic', 'Coptic'), ('Filming', 'Filming'), ('Performance', 'Performance'), ('Practice', 'Practice'), ('Scout-Boys', 'Scout - Boys'), ('Scout-Girls', 'Scout - Girls'), ('Scount-Gen', 'Scout General'), ('Sports', 'Sports'), ('Club', 'Club'), ('Holy Week','Holy Week'), ('Special Church Event','Special Church Event'), ('Other', 'Other')]

class UserProfile(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	is_one = models.BooleanField('1st Grade', default=False)
	is_two = models.BooleanField('2nd Grade', default=False)
	is_three = models.BooleanField('3rd Grade', default=False)
	is_four = models.BooleanField('4th Grade', default=False)
	is_five = models.BooleanField('5th Grade', default=False)
	is_six = models.BooleanField('6th Grade', default=False)
	is_seven = models.BooleanField('7th Grade', default=False)
	is_eight = models.BooleanField('8th Grade', default=False)
	is_nine = models.BooleanField('9th Grade', default=False)
	is_ten = models.BooleanField('10th Grade', default=False)
	is_eleven = models.BooleanField('11th Grade', default=False)
	is_tewelve = models.BooleanField('12th Grade', default=False)
	is_beyond = models.BooleanField('College and Graduates', default=False) 
	license = models.CharField(blank=False, max_length=13, choices=LICENSES)

	def is_none(self):
		if self.license == 'NoLi':
			return True
			
	def is_standard(self):
		if self.license == 'Standard':
			return True

	def is_professional(self):
		if self.license == 'Professional':
			return True

	def is_ultimate(self):
		if self.license == 'Ultimate':
			return True

	def set_license(self, license):
		self.license = license

	def active_grades(self):
		grades = []
		if self.is_one == True:
			grades.append(1)
		if self.is_two == True:
			grades.append(2)
		if self.is_three == True:
			grades.append(3)
		if self.is_four == True:
			grades.append(4)
		if self.is_five == True:
			grades.append(5)
		if self.is_six == True:
			grades.append(6)
		if self.is_seven == True:
			grades.append(7)
		if self.is_eight == True:
			grades.append(8)
		if self.is_nine == True:
			grades.append(9)
		if self.is_ten == True:
			grades.append(10)
		if self.is_eleven == True:
			grades.append(11)
		if self.is_tewelve == True:
			grades.append(12)
		if self.is_beyond == True:
			grades.append(13)
		return grades


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()

class Counter(models.Model):
	counter_name = models.CharField(blank=False, max_length=21)
	counter_value = models.IntegerField(blank=False)

class StudentBasic(models.Model):
	id_num = models.IntegerField(primary_key=True)
	first_name = models.CharField(blank=False, max_length=21)
	last_name = models.CharField(blank=False, max_length=21)
	dob = models.DateField(blank=False)
	archived = models.BooleanField(default=False)

class StudentGrLevel(models.Model):
	student = models.OneToOneField(StudentBasic, on_delete=models.CASCADE, primary_key=True)
	grade = models.IntegerField(blank=False)

class StudentCntInf(models.Model):
	student_grade = models.OneToOneField(StudentGrLevel, on_delete=models.CASCADE, primary_key=True)
	address = models.CharField(blank=True, max_length=225, default='No Address Exists')
	city = models.CharField(blank=False, max_length=48)
	state = models.CharField(blank=False, max_length=2)
	zipcode = models.CharField(blank=False, max_length=5)
	personal_cell = models.CharField(blank=True, max_length=17, default='No Phone Number')
	father_cell = models.CharField(blank=True, max_length=17, default='No Phone Number')
	mother_cell = models.CharField(blank=True, max_length=17, default='No Phone Number')
	parent_email = models.EmailField(blank=True, max_length=254, help_text='Parent email', default='temp-dne@temp.com')
	student_email = models.EmailField(blank=True, max_length=254, help_text='Student email', default='temp-dne@temp.com')

class Events(models.Model):
	event_id = models.IntegerField(primary_key=True)
	event_date = models.DateField(blank=False)
	event_day = models.CharField(blank=False, max_length=20, null = True, default="Day of Week")
	event_sect = models.CharField(blank=False, max_length=20, choices=SECTION, default="Morning")
	event_type = models.CharField(blank=False, max_length=70, choices=ACTIVITY, default="Sunday School")
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='user')
	assignees = models.ManyToManyField(UserProfile, related_name='assignees')
	assigned_date = models.DateField(blank=True, default=timezone.now)

	def get_absolute_url(self):
		return reverse('s-event-list')

	def save(self, *args, **kwargs):
		if self.event_date: 
			self.event_day = self.event_date.strftime("%A")
		self.assigned_date = timezone.now()
		super(Events, self).save(*args, **kwargs)

	@property
	def WeekDay(self):
		if self.event_date:
			return self.event_date.strftime("%A")
		return "No Day"

	

class StudentAttn(models.Model):
	student_idn = models.ForeignKey(StudentGrLevel, on_delete=models.CASCADE)
	event_idn = models.ForeignKey(Events, on_delete=models.CASCADE, default=0)
	present = models.BooleanField(blank=False, default=False)