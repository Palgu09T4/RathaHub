from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django.contrib.auth import login,logout
from account.forms import RegistrationForm,editForm
from driver.models import Driver
from account.models import UserProfile
from django.contrib.auth.models import User
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            email = form.cleaned_data.get('email')

            if role == 'driver':
                try:
                    # Check if Driver with email exists and is not already linked
                    driver = Driver.objects.get(email__iexact=email, user__isnull=True)

                except Driver.DoesNotExist:
                    form.add_error(None, "You're not approved by admin. Please contact support.")
                    return render(request, 'account/signup.html', {'form': form})

            # ✅ Create user
            user = form.save()

            # ✅ Create user profile
            UserProfile.objects.get_or_create(user=user, defaults={'role': role})

            if role == 'driver':
                # ✅ Link Driver object to new user
                driver.user = user
                driver.save()

            return redirect('account:login')
    else:
        form = RegistrationForm()
    return render(request, 'account/signup.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('account:profile')
    else:
        form=AuthenticationForm()
    return render(request,'account/login.html',{'form': form})

def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('account:login')

def profileView(request):
    if request.user.is_authenticated:
        user=request.user
        print(user)
        print("Get")
        form=editForm(instance=user)
        args = { 'user' : request.user,'form' : form}
        print(form)
        return render(request,'account/profile.html',args)
    else:
        return redirect("http://localhost:8000/home/404")

def editView(request):
    if request.method == "POST":
        print("POST")
        form=editForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')