from django.shortcuts import  render, redirect
from .forms import UserForm
from django.contrib import messages
from apps.sales.models import Client
from apps.supplies.models import Partner
from django.contrib.auth.models import User, Group

def signup(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			if request.POST.get('user_type') == '1':
				first_name = request.POST.get('name').split()[0]
				last_name = request.POST.get('name').replace(first_name,'')
				user = User(first_name=first_name,
					last_name=last_name,
					username=request.POST.get('email'),
					email=request.POST.get('email'),
					is_staff=True
					)
				user.set_password(request.POST.get('password1'))
				user.save()
				group = Group.objects.get(id=1)
				group.user_set.add(user.id)
				client = Client(user_id=user.id,
					address=request.POST.get('address'),
					nif=request.POST.get('nif'),
					)
				client.save()
			else:
				user = User(username=request.POST.get('email'),
					email=request.POST.get('email'),
					is_staff=True
					)
				user.set_password(request.POST.get('password1'))
				user.save()
				group = Group.objects.get(id=2)
				group.user_set.add(user.id)
				partner = Partner(user_id=user.id,
					name=request.POST.get('name'),
					phone=request.POST.get('phone'),
					address=request.POST.get('address'),
					nif=request.POST.get('nif'),
					)
				partner.save()
			messages.success(request, "Registration successful." )
		else:
			messages.error(request, "Unsuccessful registration. Invalid information.")
			return render(request=request, template_name="main/signup.html", context={"register_form":form})
	form = UserForm()
	return render(request=request, template_name="main/signup.html", context={"register_form":form})

def redirect_view(request):
    response = redirect('/pf/')
    return response