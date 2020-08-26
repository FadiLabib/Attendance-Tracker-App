from django import forms
from attendance_tracker.models import UserProfile
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import PrependedText

LICENSES = [('NoLi', 'No License'), ('Standard','Standard License'), ('Professional','Professional License'),('Ultimate','Ultimate License')]

class UserRegisterForm(RegistrationForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	is_one = forms.BooleanField(required=False)
	is_two = forms.BooleanField(required=False)
	is_three = forms.BooleanField(required=False)
	is_four = forms.BooleanField(required=False)
	is_five = forms.BooleanField(required=False)
	is_six = forms.BooleanField(required=False)
	is_seven = forms.BooleanField(required=False)
	is_eight = forms.BooleanField(required=False)
	is_nine = forms.BooleanField(required=False)
	is_ten = forms.BooleanField(required=False)
	is_eleven = forms.BooleanField(required=False)
	is_tewelve = forms.BooleanField(required=False)
	is_beyond = forms.BooleanField(required=False)
	license = forms.ChoiceField(required=True, choices=LICENSES, widget=forms.RadioSelect)

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['is_one'].label = "1st Grade"
		self.fields['is_two'].label = "2nd Grade"
		self.fields['is_three'].label = "3rd Grade"
		self.fields['is_four'].label = "4th Grade"
		self.fields['is_five'].label = "5th Grade"
		self.fields['is_six'].label = "6th Grade"
		self.fields['is_seven'].label = "7th Grade"
		self.fields['is_eight'].label = "8th Grade"
		self.fields['is_nine'].label = "9th Grade"
		self.fields['is_ten'].label = "10th Grade"
		self.fields['is_eleven'].label = "11th Grade"
		self.fields['is_tewelve'].label = "12th Grade"
		self.fields['is_beyond'].label = "College and Graduates"
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			HTML('<h4 class="mb-4">Account Information</h4>'),
			PrependedText('email', '<i class="fa fa-envelope" aria-hidden="true"></i>'),
			Row(
				Column(PrependedText('password1', '<i class="fa fa-key" aria-hidden="true"></i>'), css_class='col-6'),
				Column(PrependedText('password2', '<i class="fa fa-key" aria-hidden="true"></i>'), css_class='col-6'),
				css_class='form-row'
				),
			Row(
				Column(PrependedText('first_name', '<i class="fa fa-user-circle" aria-hidden="true"></i>'), css_class='col-6'),
				Column(PrependedText('last_name', '<i class="fa fa-user-circle" aria-hidden="true"></i>'), css_class='col-6'),
				css_class='form-row'
				),
			HTML('<br><h4 class="mb-4">Pick Grade Levels</h4>'),
			Row(
				Column('is_one', css_class='col'),
				Column('is_two', css_class='col'),
				Column('is_three', css_class='col'),
				Column('is_four', css_class='col'),
				Column('is_five', css_class='col'),
				Column('is_six', css_class='col'),
				css_class='form-row'
				),
			Row(
				Column('is_seven', css_class='col'),
				Column('is_eight', css_class='col'),
				Column('is_nine', css_class='col'),
				Column('is_ten', css_class='col'),
				Column('is_eleven', css_class='col'),
				Column('is_tewelve', css_class='col'),
				css_class='form-row'
				),
			Row(
				Column('is_beyond', css_class='col'),
				css_class='form-row'
				),
			HTML('<br><h4 class="mb-4">Pick License</h4>'),
			Row(
				Column('license', css_class='col'),
				css_class='form-row'
				),
			HTML('<p>By clicking Create Account, you agree to our Terms, Data Policy and Cookies Policy.<a class="link ml-1" href="#">Terms and Conditions</a></p>'),
			Submit('submit', 'Create Account', css_class="btn btn-success btn-block")
		)

	class Meta(RegistrationForm.Meta):
		model = UserProfile
		fields = ['email', 'password1', 'password2', 'first_name','last_name', 'is_one', 'is_two','is_three', 'is_four', 'is_five', 'is_six', 'is_seven', 'is_eight', 'is_nine', 'is_ten', 'is_eleven', 'is_tewelve', 'is_beyond', 'license']

class UserUpdateForm(forms.ModelForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	is_one = forms.BooleanField(required=False)
	is_two = forms.BooleanField(required=False)
	is_three = forms.BooleanField(required=False)
	is_four = forms.BooleanField(required=False)
	is_five = forms.BooleanField(required=False)
	is_six = forms.BooleanField(required=False)
	is_seven = forms.BooleanField(required=False)
	is_eight = forms.BooleanField(required=False)
	is_nine = forms.BooleanField(required=False)
	is_ten = forms.BooleanField(required=False)
	is_eleven = forms.BooleanField(required=False)
	is_tewelve = forms.BooleanField(required=False)
	is_beyond = forms.BooleanField(required=False)

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)
		self.fields['is_one'].label = "1st Grade"
		self.fields['is_two'].label = "2nd Grade"
		self.fields['is_three'].label = "3rd Grade"
		self.fields['is_four'].label = "4th Grade"
		self.fields['is_five'].label = "5th Grade"
		self.fields['is_six'].label = "6th Grade"
		self.fields['is_seven'].label = "7th Grade"
		self.fields['is_eight'].label = "8th Grade"
		self.fields['is_nine'].label = "9th Grade"
		self.fields['is_ten'].label = "10th Grade"
		self.fields['is_eleven'].label = "11th Grade"
		self.fields['is_tewelve'].label = "12th Grade"
		self.fields['is_beyond'].label = "College and Graduates"
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			PrependedText('email', '<i class="fa fa-envelope" aria-hidden="true"></i>'),
			HTML('<br>'),
			Row(
				Column(PrependedText('first_name', '<i class="fa fa-user-circle" aria-hidden="true"></i>'), css_class='col-6'),
				Column(PrependedText('last_name', '<i class="fa fa-user-circle" aria-hidden="true"></i>'), css_class='col-6'),
				css_class='form-row'
				),
			HTML('<br><p>Change Grade Level</p>'),
			Row(
				Column('is_one', css_class='col'),
				Column('is_two', css_class='col'),
				Column('is_three', css_class='col'),
				Column('is_four', css_class='col'),
				css_class='form-row'
				),
			Row(
				Column('is_five', css_class='col'),
				Column('is_six', css_class='col'),
				Column('is_seven', css_class='col'),
				Column('is_eight', css_class='col'),
				css_class='form-row'
				),
			Row(
				Column('is_nine', css_class='col-2'),
				Column('is_ten', css_class='col-2'),
				Column('is_eleven', css_class='col-2'),
				Column('is_tewelve', css_class='col-2'),
				Column('is_beyond', css_class='col-4'),
				css_class='form-row'
				),
			HTML('<br>'),
			Submit('submit', 'Update', css_class="btn btn-info btn-block")
		)

	class Meta:
		model = UserProfile
		fields = ['email', 'first_name','last_name', 'is_one', 'is_two','is_three', 'is_four', 'is_five', 'is_six', 'is_seven', 'is_eight', 'is_nine', 'is_ten', 'is_eleven', 'is_tewelve', 'is_beyond']

class ChangePasswordForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			PrependedText('old_password', '<i class="fa fa-key" aria-hidden="true"></i>'),
			PrependedText('new_password1', '<i class="fa fa-key" aria-hidden="true"></i>'),
			PrependedText('new_password2', '<i class="fa fa-key" aria-hidden="true"></i>'),
			HTML('<br>'),
			Submit('submit', 'Update', css_class="btn btn-info btn-block")
			)

class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			PrependedText('username', '<i class="fa fa-envelope" aria-hidden="true"></i>'),
			PrependedText('password', '<i class="fa fa-key" aria-hidden="true"></i>'),
			HTML('<br>'),
			Submit('submit', 'Login', css_class="btn btn-info btn-block")
			)

class ResetPasswordForm(PasswordResetForm):
	def __init__(self, *args, **kwargs):
		super(ResetPasswordForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			PrependedText('email', '<i class="fa fa-envelope" aria-hidden="true"></i>'),
			HTML('<br>'),
			Submit('submit', 'Request Password Reset', css_class="btn btn-info btn-block")
			)

class SetNewPasswordForm(SetPasswordForm):
	def __init__(self, *args, **kwargs):
		super(SetNewPasswordForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			PrependedText('new_password1', '<i class="fa fa-key" aria-hidden="true"></i>'),
			PrependedText('new_password2', '<i class="fa fa-key" aria-hidden="true"></i>'),
			HTML('<br>'),
			Submit('submit', 'Reset Password', css_class="btn btn-info btn-block")
			)





