from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Driver
from .forms import DriverForm

# Show driver registration form (only for admin)
def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = DriverForm()
        return render(request, 'driver/index.html', {'form': form})
    return redirect("http://localhost:8000/home/404")

# Handle driver registration POST request
def driver(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_superuser:
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Driver registered successfully.'
            return render(request, 'driver/index.html', {
                'form': DriverForm(),
                'success': success_message
            })
        else:
            return render(request, 'driver/index.html', {
                'form': form,
                'error': 'Form validation failed.'
            })
    return redirect("http://localhost:8000/home/404")

# View all registered drivers (only admin)
def drivers(request):
    if request.user.is_authenticated and request.user.is_superuser:
        drivers = Driver.objects.all()
        return render(request, 'driver/driverlist.html', {
            'drivers': drivers,
            'user': request.user
        })
    return redirect("http://localhost:8000/home/404")

# Delete driver (admin only)
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Driver

def delete(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        driver = get_object_or_404(Driver, id=id)

        # Delete associated user if exists
        #if hasattr(driver, 'user') and driver.user:
            #driver.user.delete()

        # Delete the driver (won't be needed if on_delete=CASCADE already)
        Driver.objects.filter(id=id).delete()

        return redirect('driver:drivers')
    return redirect("http://localhost:8000/home/404")

# Edit driver (admin only)
def edit(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        driver = get_object_or_404(Driver, id=id)
        if request.method == "POST":
            form = DriverForm(request.POST, instance=driver)
            if form.is_valid():
                form.save()
                return redirect('http://localhost:8000/driver/drivers')
        else:
            form = DriverForm(instance=driver)
            return render(request, 'driver/driverEdit.html', {
                'form': form,
                'id': id
            })
    return redirect("http://localhost:8000/home/404")
