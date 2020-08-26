from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from UAM.forms import UserUpdateForm
from UAM.models import Subscription

def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)

	context = {
		'u_form': u_form,
		'subscription': Subscription.objects.get(user=request.user)
	}
	return render(request, 'UAM/profile.html', context)