from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.contrib.auth import authenticate, login, logout

from django.http import Http404, JsonResponse
from django.shortcuts import get_list_or_404, render, get_object_or_404

from django.core import serializers
from django.urls import reverse

from .forms import SignupForm, LoginForm, PartnerProfileForm
from django.contrib.auth.models import User
from .models import Account, Partner, PB_Service

# Create your views here.

def index(request):
	note = "Welcome to Pointbook"
	context = {'note': note}
	return render(request, 'pointbookmain/index.html', context)

	# foos = Partner.objects.filter(pk=1)
	# data = serializers.serialize('json', foos)
	# # latest_partners_list = Partner.objects.order_by('-created_on')[:5]
	# # context = {'latest_partners_list' : latest_partners_list}
	# # return render(request, 'pointbookmain/index.html', context)
	# return HttpResponse(data, content_type='application/json')

def sign_up(request):
	if request.method == "POST":
		signup_form= SignupForm(request.POST)

		if signup_form.is_valid():
			#RETRIEVE DATA FROM FORM
			username = signup_form.cleaned_data['username']
			password = signup_form.cleaned_data['password']
			email = signup_form.cleaned_data['email']
			first_name = signup_form.cleaned_data['first_name']
			last_name = signup_form.cleaned_data['last_name']
			is_partner = signup_form.cleaned_data['is_partner']
			
			#CREATES THE USER
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			
			user_account = User.objects.get(username=username)
			account = Account(user=user_account, is_partner=is_partner)
			user.save()
			account.save()
			
			return HttpResponseRedirect('/index')
	else:
		signup_form = SignupForm()
	
	context = {'signup_form': signup_form}
	return render(request, 'pointbookmain/signup.html', context)

def log_in(request):
	message = ''
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		
		if login_form.is_valid():
			#Clean Data
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			
			#AuthenticateUser
			user = authenticate(username=username, password=password)
			
			#Check if user was found
			if user is not None:
				#Check if user is active
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/index')
				else:
					message = 'User is not active'
			else:
			# Anonymous User = no user was found
				message = 'The username and/or password were inaappropriate.'
	else:
		login_form = LoginForm() #Instantiates Empty Form
	
	context = {'login_form': login_form, 'message': message}
	return render(request, 'pointbookmain/login.html', context)

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/index')

def partner_profile(request, partner_id):
	partners = get_list_or_404(Partner, pk=partner_id)
	context = {'partners': partners}
	return render(request, 'pointbookmain/partner_profile.html', context)

def partner_list(request):
	partners = Partner.objects.all()
	context = {'partners': partners}		
	return render(request, 'pointbookmain/partner_list.html', context)

def partner_profile_edit(request, partner_id):
	instance = Partner.objects.get(pk=partner_id)
	if request.method == "POST":
		partner_profile_form = PartnerProfileForm(request.POST or None, instance=instance)

		if partner_profile_form.is_valid():
			partner_profile_form.save()
			return HttpResponseRedirect('/index/')
	else:
		partner_profile_form = PartnerProfileForm(instance=instance)

	context = {'partner_profile_form': partner_profile_form}
	return render(request, 'pointbookmain/partner_profile_edit.html', context)

def partner_profile_delete(request, partner_id):
	partner = Partner.objects.get(pk=partner_id)
	partner.delete()
	return HttpResponse('deleted')

def service_list(request):
	services = PB_Service.objects.all()
	data = serializers.serialize('json', services)
	return HttpResponse(data, content_type='application/json')
