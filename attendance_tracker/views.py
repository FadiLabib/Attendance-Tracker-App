from django.shortcuts import render, redirect, get_object_or_404
from attendance_tracker.models import UserProfile
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from attendance_tracker.models import StudentBasic, StudentGrLevel, StudentCntInf, Events, Counter, StudentAttn
from attendance_tracker.decorators import user_is_ultimate, user_is_professional, user_is_standard
from bootstrap_datepicker_plus import DatePickerInput
from attendance_tracker.forms import EventsUpdateForm, UltimateEventsUpdateForm, AttendanceForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django import forms
from dal import autocomplete
from django.db.models import Q

def home(request):
	context = {
		'title': 'Home',
	}
	return render(request, 'attendance_tracker/home.html', context)

def standardclasslist(request):
	context = {
		'title': 'Current Students',
		'contacts': StudentGrLevel.objects.filter(student__archived=False, grade__in=request.user.active_grades())
	}
	return render(request, 'attendance_tracker/clslist.html', context)

def expandedclasslist(request):
	context = {
		'title': 'Current Students',
		'contacts': StudentCntInf.objects.filter(student_grade__student__archived=False, student_grade__grade__in=request.user.active_grades())
	}
	return render(request, 'attendance_tracker/expclslist.html', context)

# https://stackoverflow.com/questions/47789661/how-can-i-combine-two-views-and-two-forms-into-one-single-template/47862064
class SEventsCreateView(CreateView):
	model = Events
	fields = ['event_date', 'event_day', 'event_sect', 'event_type']

	def get_context_data(self, *args, **kwargs):
		context = super(SEventsCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Event'
		return context

	def get_form(self):
		form = super().get_form()
		form.fields['event_date'].widget = DatePickerInput()
		form.fields['event_day'].widget = forms.HiddenInput()
		return form

	def form_valid(self, form):
		form.instance.user = self.request.user
		current_counter = Counter.objects.get(counter_name='event_id').counter_value 
		form.instance.event_id = current_counter
		counter_update = Counter.objects.get(counter_name="event_id")
		counter_update.counter_value= current_counter + 1
		counter_update.save()
		response = super(SEventsCreateView, self).form_valid(form)
		c_event_id = self.object.event_id
		student_list = StudentGrLevel.objects.filter(student__archived=False, grade__in=self.object.user.active_grades())
		for member in student_list:
			member_id = member.student.id_num
			c_member = StudentGrLevel.objects.get(student=StudentBasic.objects.get(id_num=member_id))
			event = Events.objects.get(event_id=c_event_id)
			record = StudentAttn(event_idn=event, student_idn=c_member, present=False)
			record.save()
		return response

class AssigneesAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = UserProfile.objects.filter(is_superuser=False, is_staff=False).order_by('email')

		if self.q:
			qs = qs.filter(email__startswith=self.q)

		return qs

class UEventsCreateView(CreateView):
	model = Events
	autocomplete_fields = ('assignees')
	fields = ['event_date', 'event_day', 'event_sect', 'event_type', 'assignees', 'assigned_date']
	template_name_suffix = "_u_create_event_form"

	def get_context_data(self, *args, **kwargs):
		context = super(UEventsCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Event'
		return context

	def get_form(self):
		form = super().get_form()
		form.fields['event_date'].widget = DatePickerInput()
		form.fields['event_day'].widget = forms.HiddenInput()
		form.fields['assignees'].widget = autocomplete.Select2Multiple(url='assignees-autocomplete')
		form.fields['assignees'].help_text = "Enter the email(s) for users to which you want to assign this event"
		form.fields['assigned_date'].widget = forms.HiddenInput()
		return form

	def form_valid(self, form):
		form.instance.user = self.request.user
		current_counter = Counter.objects.get(counter_name='event_id').counter_value 
		form.instance.event_id = current_counter
		counter_update = Counter.objects.get(counter_name="event_id")
		counter_update.counter_value= current_counter + 1
		counter_update.save()
		response = super(UEventsCreateView, self).form_valid(form)
		c_event_id = self.object.event_id
		student_list = StudentGrLevel.objects.filter(student__archived=False, grade__in=self.object.user.active_grades())
		for member in student_list:
			member_id = member.student.id_num
			c_member = StudentGrLevel.objects.get(student=StudentBasic.objects.get(id_num=member_id))
			event = Events.objects.get(event_id=c_event_id)
			record = StudentAttn(event_idn=event, student_idn=c_member, present=False)
			record.save()
		return response

	# When event is created, go to the ultimate version of events list
	def get_success_url(self):
		return reverse('u-event-list')

class SEventsUpdateView(UserPassesTestMixin, UpdateView):
	model = Events
	form_class = EventsUpdateForm
	template_name_suffix = "_update_form"

	def get_context_data(self, *args, **kwargs):
		context = super(SEventsUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Event'
		return context

	def get_form(self):
		form = super().get_form()
		form.fields['event_date'].widget = DatePickerInput()
		form.fields['event_day'].widget.attrs['readonly'] = True
		return form

	def form_valid(self, form):
		form.instance.user = self.request.user
		response = super(SEventsUpdateView, self).form_valid(form)
		return response

	#This is imported from UserPassesTestMixin and allows us to add more restrictions 
	#Here only an ultimate user or the user who created the event is able to update it
	def test_func(self):
		event = self.get_object()
		#last check is a many to many field to check for membership you have to call .all() on the ManyToMany field
		if ((self.request.user.is_ultimate()) or (self.request.user == event.user) or (self.request.user in event.assignees.all())):
			return True
		return False

class UEventsUpdateView(UserPassesTestMixin, UpdateView):
	model = Events
	form_class = UltimateEventsUpdateForm
	template_name_suffix = "_u_update_event_form"

	def get_context_data(self, *args, **kwargs):
		context = super(UEventsUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Event'
		return context

	def get_form(self):
		form = super().get_form()
		form.fields['event_date'].widget = DatePickerInput()
		form.fields['event_day'].widget.attrs['readonly'] = True
		form.fields['assignees'].widget = autocomplete.Select2Multiple(url='assignees-autocomplete')
		#loads in already assigned users
		form.fields['assignees'].queryset = UserProfile.objects.all()
		form.fields['assignees'].help_text = "Enter the email(s) for users to which you want to assign this event"
		form.fields['assigned_date'].widget = forms.HiddenInput()
		return form

	def form_valid(self, form):
		form.instance.user = self.request.user
		response = super(UEventsUpdateView, self).form_valid(form)
		return response

	#This is imported from UserPassesTestMixin and allows us to add more restrictions 
	#Here only an ultimate user or the user who created the event is able to update it
	def test_func(self):
		event = self.get_object()
		#last check is a many to many field to check for membership you have to call .all() on the ManyToMany field
		if ((self.request.user.is_ultimate()) or (self.request.user == event.user) or (self.request.user in event.assignees.all())):
			return True
		return False

	# When event is created, go to the ultimate version of events list
	def get_success_url(self):
		return reverse('u-event-list')

class SEventsListView(ListView):
	model = Events
	context_object_name = 'events'
	ordering = ['-event_date']

	def get_context_data(self, *args, **kwargs):
		context = super(SEventsListView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Created Events'
		return context

class UEventsListView(ListView):
	model = Events
	context_object_name = 'events'
	template_name_suffix = '_u_list'
	ordering = ['-event_date']

	def get_context_data(self, *args, **kwargs):
		context = super(UEventsListView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Created Events'
		return context

class SEventsByUserListView(ListView):
	model = Events
	template_name = "attendance_tracker/user_events.html"
	context_object_name = 'events'

	def get_queryset(self):
		current_user = get_object_or_404(UserProfile, email=self.kwargs['email'])
		return Events.objects.filter(Q(user=current_user) | Q(assignees=current_user))

	def get_context_data(self, *args, **kwargs):
		context = super(SEventsByUserListView, self).get_context_data(*args, **kwargs)
		context['title'] = 'My Created Events'
		context['current_user'] = get_object_or_404(UserProfile, email=self.kwargs['email'])
		return context

class UEventsByUserListView(ListView):
	model = Events
	template_name = "attendance_tracker/u_user_events.html"
	context_object_name = 'events'

	def get_queryset(self):
		current_user = get_object_or_404(UserProfile, email=self.kwargs['email'])
		return Events.objects.filter(Q(user=current_user) | Q(assignees=current_user))

	def get_context_data(self, *args, **kwargs):
		context = super(UEventsByUserListView, self).get_context_data(*args, **kwargs)
		context['title'] = 'My Created Events'
		context['current_user'] = get_object_or_404(UserProfile, email=self.kwargs['email'])
		return context

class SEventsDetailView(DetailView):
	model = Events

	def get_context_data(self, **kwargs):
		context = super(SEventsDetailView, self).get_context_data(**kwargs)
		c_event_id = self.object.event_id
		event = Events.objects.get(event_id=c_event_id)
		context['event_student_list'] = StudentAttn.objects.filter(event_idn=event)
		context['long_title'] = str(self.object.event_date) + " - " + self.object.event_day + " " + self.object.event_sect + " - " + self.object.event_type
		return context

class UEventsDetailView(DetailView):
	model = Events
	template_name_suffix = '_u_detail'

	def get_context_data(self, **kwargs):
		context = super(UEventsDetailView, self).get_context_data(**kwargs)
		c_event_id = self.object.event_id
		event = Events.objects.get(event_id=c_event_id)
		context['event_student_list'] = StudentAttn.objects.filter(event_idn=event)
		context['long_title'] = str(self.object.event_date) + " - " + self.object.event_day + " " + self.object.event_sect + " - " + self.object.event_type
		return context

class SEventsDeleteView(UserPassesTestMixin, DeleteView):
	model = Events
	success_url = '/events/'

	def get_context_data(self, *args, **kwargs):
		context = super(SEventsDeleteView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete Event'
		return context

	def test_func(self):
		event = self.get_object()
		if ((self.request.user.is_ultimate()) or (self.request.user == event.user) or (self.request.user in event.assignees.all())):
			return True
		return False

class UEventsDeleteView(UserPassesTestMixin, DeleteView):
	model = Events
	template_name_suffix = '_u_confirm_delete'
	success_url = '/u_events/'

	def get_context_data(self, *args, **kwargs):
		context = super(UEventsDeleteView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete Event'
		return context

	def test_func(self):
		event = self.get_object()
		if ((self.request.user.is_ultimate()) or (self.request.user == event.user) or (self.request.user in event.assignees.all())):
			return True
		return False

class STakeAttendanceView(UserPassesTestMixin, UpdateView):
	model = Events
	fields = []
	template_name_suffix = "_take_attendance"

	def get_success_url(self):
		return reverse('s-take-attendance', kwargs={'pk':self.object.event_id}) 

	def get_context_data(self, **kwargs):
		context = super(STakeAttendanceView, self).get_context_data(**kwargs)
		c_event_id = self.object.event_id
		event = Events.objects.get(event_id=c_event_id)
		context['event_student_list'] = StudentAttn.objects.filter(event_idn=event)
		context['long_title'] = str(self.object.event_date) + " - " + self.object.event_day + " " + self.object.event_sect + " - " + self.object.event_type
		return context

	def form_valid(self, form):
		response = super(STakeAttendanceView, self).form_valid(form)
		# list of student ids who are present
		id_list  = self.request.POST.getlist('present')
		# intialize the present field for all students in the event to False
		c_event_id = self.object.event_id
		event = Events.objects.get(event_id=c_event_id)
		event_student_list = StudentAttn.objects.filter(event_idn=event)
		for student in event_student_list:
			record = StudentAttn.objects.get(event_idn=event, student_idn=student.student_idn)
			record.present = False
			record.save()
		# update the ones on the id_list to have their present field set to True
		for student_id in id_list:
			student_object = StudentGrLevel.objects.get(student=StudentBasic.objects.get(id_num=student_id))
			update_record = StudentAttn.objects.get(event_idn=event, student_idn=student_object)
			update_record.present = True
			update_record.save()
		return response

	def test_func(self):
		event = self.get_object()
		if ((self.request.user.is_ultimate()) or (self.request.user == event.user) or (self.request.user in event.assignees.all())):
			return True
		return False

class UTakeAttendanceView(UserPassesTestMixin, UpdateView):
	model = Events
	fields = []
	template_name_suffix = "_u_take_attendance"

	def get_success_url(self):
		return reverse('u-take-attendance', kwargs={'pk':self.object.event_id}) 

	def get_context_data(self, **kwargs):
		context = super(UTakeAttendanceView, self).get_context_data(**kwargs)
		c_event_id = self.object.event_id
		event = Events.objects.get(event_id=c_event_id)
		context['event_student_list'] = StudentAttn.objects.filter(event_idn=event)
		context['long_title'] = str(self.object.event_date) + " - " + self.object.event_day + " " + self.object.event_sect + " - " + self.object.event_type
		return context

	def form_valid(self, form):
		response = super(UTakeAttendanceView, self).form_valid(form)
		# list of student ids who are present
		id_list  = self.request.POST.getlist('present')
		# intialize the present field for all students in the event to False
		c_event_id = self.object.event_id
		event = Events.objects.get(event_id=c_event_id)
		event_student_list = StudentAttn.objects.filter(event_idn=event)
		for student in event_student_list:
			record = StudentAttn.objects.get(event_idn=event, student_idn=student.student_idn)
			record.present = False
			record.save()
		# update the ones on the id_list to have their present field set to True
		for student_id in id_list:
			student_object = StudentGrLevel.objects.get(student=StudentBasic.objects.get(id_num=student_id))
			update_record = StudentAttn.objects.get(event_idn=event, student_idn=student_object)
			update_record.present = True
			update_record.save()
		return response

	def test_func(self):
		event = self.get_object()
		if ((self.request.user.is_ultimate()) or (self.request.user == event.user) or (self.request.user in event.assignees.all())):
			return True
		return False

def about(request):
	context = {
		'title': 'About'
	}
	return render(request, 'attendance_tracker/about.html', {'title': 'About'})