from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Vehicle
from .forms import VehicleForm

# ✅ View to render add vehicle page – Admin only
def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = VehicleForm()
        return render(request, 'vehicle/index.html', {'form': form})
    return redirect("http://localhost:8000/home/404")

# ✅ Add vehicle – Admin only
def addVehicle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            form = VehicleForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.owner = request.user
                instance.save()
                success_message = 'Vehicle added successfully.'
                form = VehicleForm()
                return render(request, 'vehicle/index.html', {'form': form, 'success': success_message})
        else:
            form = VehicleForm()
            return render(request, 'vehicle/index.html', {'form': form})
    return redirect("http://localhost:8000/home/404")

# ✅ Show vehicles – Accessible by all authenticated users
def showVehicles(request):
    if request.method == 'POST' and 'searchb' in request.POST:
        search_query = request.POST.get('search_box')
        vehiclesList = Vehicle.objects.filter(registration_plate=search_query)
        return render(request, 'vehicle/vehiclelist.html', {'vehiclesList': vehiclesList})

    elif request.method == 'POST' and 'viewallb' in request.POST:
        vehiclesList = Vehicle.objects.all()
        return render(request, 'vehicle/vehiclelist.html', {'vehiclesList': vehiclesList})

    elif request.user.is_authenticated:
        if request.user.is_superuser:
            vehiclesList = Vehicle.objects.all()
        else:
            vehiclesList = Vehicle.objects.all()  # Show all vehicles to normal users too
        return render(request, 'vehicle/vehiclelist.html', {'vehiclesList': vehiclesList})

    return redirect("http://localhost:8000/home/404")

# ✅ Delete vehicle – Admin only
def delete(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicle = get_object_or_404(Vehicle, id=id)
        vehicle.delete()
        return redirect('http://localhost:8000/vehicle/vehicles')
    return redirect("http://localhost:8000/home/404")

# ✅ Edit vehicle – Admin only
def edit(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicle = get_object_or_404(Vehicle, id=id)
        if request.method == "POST":
            form = VehicleForm(request.POST, request.FILES, instance=vehicle)
            if form.is_valid():
                form.save()
                return redirect('http://localhost:8000/vehicle/vehicles')
        else:
            form = VehicleForm(instance=vehicle)
        return render(request, 'vehicle/vehicleEdit.html', {'form': form, 'id': id})
    return redirect("http://localhost:8000/home/404")
