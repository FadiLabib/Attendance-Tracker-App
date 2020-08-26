from django import forms
from django.forms.widgets import CheckboxInput
from attendance_tracker.models import StudentAttn, Events

class EventsUpdateForm(forms.ModelForm):

	class Meta:
		model =  Events
		fields = ('event_date', 'event_day', 'event_sect', 'event_type')

class UltimateEventsUpdateForm(forms.ModelForm):

	class Meta:
		model =  Events
		fields = ('event_date', 'event_day', 'event_sect', 'event_type', 'assignees','assigned_date')

class AttendanceForm(forms.ModelForm):

	class Meta:
		model = StudentAttn
		fields = ('present',)