# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from accounts.models import UserProfile
from accounts.forms import SignUpForm, ProfileForm
import re

""" class SignUpView(CreateView):
  template_name = 'accounts/registration.html'
  form_class = SignUpForm
  success_url = reverse_lazy('accounts:login')

  def form_valid(self, form):
    form.save()
    return super(SignUpView, self).form_valid(form) """
  
  #success_message = "Your profile was created successfully"


def signup(request):
	form = SignUpForm
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Your account is created successfully")
			return redirect('accounts:login')

	return render(request, 'accounts/sign_up.html', context={'signup_form': form})


""" def login_user(request):
	form = AuthenticationForm()
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home:home')
	return render(request, 'accounts/login.html', context={'login_form': form}) """

class LoginView(FormView):
	form_class = AuthenticationForm
	template_name = 'accounts/login.html'
	success_url = reverse_lazy('home:products')

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		next = self.request.POST['next']
		print(next)
		print(type(next))
		user = authenticate(username=username, password=password)
		if user is not None:
			login(self.request, user)
			if next != "None":
				next = re.sub(r'\s+', '', next)
				next = next[22:]
				super(LoginView, self).form_valid(form)
				return redirect(next)

		return super(LoginView, self).form_valid(form)
                
                
    	
class LogoutView(LoginRequiredMixin, FormView):
	form_class = AuthenticationForm
	#template_name = 'accounts/signup.html'

	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect('accounts:login')


""" def user_profile(request):
	profile = UserProfile.objects.get(user=request.user)
	context = {
		'profile': profile
	}
	return render(request, 'accounts/user_profile.html', context) """


def change_profile(request):
	profile = UserProfile.objects.get(user=request.user)
	form = ProfileForm(instance=profile)
	
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			form = ProfileForm(instance=profile)
	return render(request, 'accounts/user_profile.html', context={'profile_form': form})
