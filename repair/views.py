from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Repair
from .forms import RepairForm
from account.models import UserProfile  # adjust if needed

def is_driver(user):
    try:
        return UserProfile.objects.get(user=user).role == 'driver'
    except UserProfile.DoesNotExist:
        return False

def is_driver_or_admin(user):
    return user.is_authenticated and (user.is_superuser or is_driver(user))

# Show empty form
def index(request):
    if is_driver_or_admin(request.user):
        form = RepairForm()
        return render(request, 'repair/index.html', {'form': form})
    return redirect('/home/404')


# Submit repair form
def repair(request):
    if is_driver_or_admin(request.user):
        if request.method == 'POST':
            form = RepairForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.registeredUser = request.user
                instance.save()
                return render(request, 'repair/index.html', {
                    'form': RepairForm(),
                    'success': 'Issue Registered'
                })
        return render(request, 'repair/index.html', {
            'form': RepairForm(),
            'error': 'Something went wrong error'
        })
    return redirect('/home/404')


# View all repair issues
def issues(request):
    if is_driver_or_admin(request.user):
        repairsList = Repair.objects.all()
        return render(request, 'repair/issues.html', {'repairsList': repairsList})
    return redirect('/home/404')


# Toggle repair status
def update(request, id):
    if is_driver_or_admin(request.user):
        repair = get_object_or_404(Repair, id=id)
        repair.status = "NS" if repair.status == "S" else "S"
        repair.save()
        return redirect('/repair/issues')
    return redirect('/home/404')


# Edit repair issue
def edit(request, id):
    if is_driver_or_admin(request.user):
        repair = get_object_or_404(Repair, id=id)
        if request.method == "POST":
            form = RepairForm(request.POST, instance=repair)
            if form.is_valid():
                form.save()
                return redirect('/repair/issues')
        else:
            form = RepairForm(instance=repair)
            return render(request, 'repair/repairEdit.html', {'form': form, 'id': id})
    return redirect('/home/404')
