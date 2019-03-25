# Create your views here.
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import datetime as dt
from django.contrib.auth.decorators import login_required

from .models import Neighbourhood,Business,Profile,Posts,Comments,Join
from .forms import SignupForm,AddHoodForm,AddBusinessForm,UpdateProfileForm,AddPostForm

# Create your views here.
@login_required(login_url='/accounts/login')
def index(request):
  neighbourhoods = Neighbourhood.objects.all()
  return render(request,'index.html',{"neighbourhoods":neighbourhoods})

def home(request):
  neighbourhoods = Neighbourhood.objects.filter(user=request.user)
  posts = []
  for neighbourhood in neighbourhoods:
    try:
      hoodposts = Posts.objects.filter(hood = neighbourhood)
      for post in hoodposts:
        posts.append(post)
    except:
      None

  return render(request,'home.html', {"neighbourhoods":neighbourhoods,"posts":posts})

@login_required(login_url='/accounts/login/')
def search_business(request):
  
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        businesses = Business.objects.filter(name__icontains = search_term,hood = request.user.join.hood_id.id)
        searched_businesses = Business.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html'())

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html')

@login_required(login_url='/accounts/login/')
def add_hood(request):
	if request.method == 'POST':
		form = AddHoodForm(request.POST)
		if form.is_valid():
			neighbourhood = form.save(commit = False)
			neighbourhood.user = request.user
			neighbourhood.save()
			messages.success(request, 'You Have succesfully created a hood.You may now join your neighbourhood')
			return redirect('home')

	else:
		form = AddHoodForm()
	return render(request,'add_hood.html', {'form': form})

@login_required(login_url='/accounts/login/')
def join_hood(request,hood_id):
	neighbourhood = Neighbourhood.objects.get(pk = hood_id)
	if Join.objects.filter(user_id = request.user).exists():
		
		Join.objects.filter(user_id = request.user).update(hood_id = neighbourhood)
	else:
		
		Join(user_id=request.user,hood_id = neighbourhood).save()

	messages.success(request, 'Success! You have succesfully joined this Neighbourhood ')
	return redirect('index')


@login_required(login_url='/accounts/login/')
def leave_hood(request,id):
  '''
  Views that enables users leave a neighbourhood
  '''
  Join.objects.get(id = request.user.id).delete()
  return redirect('index')

@login_required(login_url='/accounts/login/')
def add_business(request):
	if request.method == 'POST':
		form = AddBusinessForm(request.POST)
		if form.is_valid():
			business = form.save(commit = False)
			business.user = request.user
			business.save()
			messages.success(request, 'You Have succesfully created a hood.You may now join your neighbourhood')
			return redirect('added_businesses')

	else:
		form = AddBusinessForm()
		return render(request,'add_business.html')

@login_required(login_url='/accounts/login/')
def added_businesses(request):
	businesses= Business.objects.filter(user = request.user)
	return render(request,'businesses.html')

@login_required(login_url='/accounts/login/')
def profile(request):
	profile = Profile.objects.get(user = request.user)
  
	return render(request,'profile/profile.html')

@login_required(login_url='/accounts/login/')
def update_profile(request):
	profile = Profile.objects.get(user = request.user)
	if request.method == 'POST':
		form = UpdateProfileForm(request.POST,instance = profile )
		if form.is_valid():
			form.save()
			messages.success(request, 'Successful profile edit!')
			return redirect('profile')
	else:
		form = UpdateProfileForm(instance = profile )
		return render(request,'profile/update_profile.html')

@login_required(login_url='/accounts/login/')
def add_post(request):
  if Join.objects.filter(user_id=request.user).exists():
    if request.method == 'POST':
      form = AddPostForm(request.POST)
      if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.hood = request.user.join.hood_id
        post.save()
        return redirect('index')

    else:
      form = AddPostForm()
      return render(request,'add_post.html',{'form':form})
  else:
    messages.error(request,'Error!!Post can only be added after joining a neighbourhood!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def posts(request):
  posts = Posts.objects.filter(user = request.user)
  return render(request,'posts.html')


@login_required(login_url='/accounts/login/')
def search_results(request):

  if request.method == 'GET':
    search_term = request.GET.get("neighbourhood")
    print(search_term)
    searched_neighbourhoods = Neighbourhood.search_by_title(search_term)
    print(searched_neighbourhoods.name)
    message = f"{search_term}"

    return render(request, 'search.html',{"message":message,"neighbourhood": searched_neighbourhoods})

  else:
    print('meh')
    message = "You haven't searched for any neighbourhood"
    return render(request, 'search.html',{"message":message})

def delete_hood(request,hood_id):
  Neighbourhood.objects.filter(pk=hood_id).delete()
  messages.error(request,'Neighbourhood has been deleted successfully')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_post(request,post_id):
  Posts.objects.filter(pk=post_id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_business(request,business_id):
  Business.objects.filter(pk=business_id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  