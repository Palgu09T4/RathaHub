from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Book
from driver.models import Driver
from .forms import BookForm
import geopy.distance
import geopy.geocoders
from django.conf import settings
from django.core.mail import EmailMessage
from decimal import Decimal
import stripe
import uuid
from account.models import UserProfile  # Ensure this import matches your project

stripe.api_key = settings.STRIPE_SECRET_KEY  # Set your Stripe secret key from settings

def index(request):
    if request.user.is_authenticated:
        form = BookForm()
        return render(request, 'booking/index.html', {'form': form})
    return redirect("http://localhost:8000/home/404")

def pay(request):
    if request.user.is_authenticated:
        return render(request, 'booking/payment.html')
    return redirect("http://localhost:8000/home/404")

def book(request):
    if not request.user.is_authenticated:
        return redirect("http://localhost:8000/home/404")

    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role != 'customer' and not request.user.is_superuser:
        return redirect("http://localhost:8000/home/404")

    if request.method == 'POST':
        form = BookForm(request.POST)
        print("📨 POST received!")
        print("✅ POST data:", request.POST)

        # Remove driver field from form for customers before is_valid
        if not request.user.is_superuser:
            form.fields.pop('driver', None)

        if form.is_valid():
            print("✅ Form is valid")
            instance = form.save(commit=False)
            instance.allottedUser = request.user

            source = instance.source
            destination = instance.destination

            geolocator = geopy.geocoders.Nominatim(user_agent="booking")

            try:
                loc1 = geolocator.geocode(source)
                loc2 = geolocator.geocode(destination)

                if not loc1 or not loc2:
                    raise ValueError("Invalid location data")

                distance = geopy.distance.distance(
                    (loc1.latitude, loc1.longitude),
                    (loc2.latitude, loc2.longitude)
                ).km

                instance.distance = round(distance, 2)
                instance.cost = int(instance.vehicle.cost_per_km * Decimal(str(distance)))
                instance.duration = str(round(distance / 40 * 60)) + " mins"

                # ✅ Admin manually selects driver
                if request.user.is_superuser:
                    selected_driver = form.cleaned_data.get('driver')
                    if selected_driver:
                        instance.allottedDriver = selected_driver
                        selected_driver.status = "B"
                        selected_driver.save()
                else:
                    # ✅ Auto assign for customers
                    available_drivers = Driver.objects.filter(status="NB")
                    if available_drivers.exists():
                        assigned_driver = available_drivers.first()
                        print("✅ Assigned driver:", assigned_driver)
                        instance.allottedDriver = assigned_driver
                        assigned_driver.status = "B"
                        assigned_driver.save()
                    else:
                        return render(request, 'booking/index.html', {
                            'form': form,
                            'error': 'No available drivers at the moment.'
                        })

                instance.save()

                # Stripe payment
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': instance.cost * 100,
                            'product_data': {
                                'name': f'Booking from {source} to {destination}',
                            },
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=f'http://localhost:8000/booking/payment_success/?order_id={instance.id}',
                    cancel_url='http://localhost:8000/booking/bookings',
                )

                return render(request, 'booking/payment.html', {
                    'details': instance,
                    'payment_link': session.url
                })

            except Exception as e:
                return render(request, 'booking/index.html', {
                    'form': form,
                    'error': f"Location lookup or payment setup failed: {str(e)}"
                })

        else:
            # 🔴 Form is invalid – show errors in form and custom message
            print("❌ Form is invalid. Errors:", form.errors)
            return render(request, 'booking/index.html', {
                'form': form,
                'error': 'Please correct the highlighted errors below.'
            })

    # GET method
    form = BookForm()
    if not request.user.is_superuser:
        form.fields.pop('driver', None)
    return render(request, 'booking/index.html', {'form': form})


def payment_success(request):
    order_id = request.GET.get('order_id')

    if order_id:
        try:
            booking = Book.objects.get(id=order_id)
            booking.status = 'Paid'
            booking.save()
            return render(request, 'booking/success.html', {
                'booking': booking,
                'message': 'Payment successful!'
            })
        except Book.DoesNotExist:
            return render(request, 'booking/success.html', {
                'message': f'Booking with order ID {order_id} not found.'
            })
    else:
        return render(request, 'booking/success.html', {
            'message': 'No order ID received in the callback.'
        })

def booking(request):
    if not request.user.is_authenticated:
        return redirect("http://localhost:8000/home/404")

    bookings = Book.objects.all()

    # Expire old bookings
    for booking in bookings:
        if booking.status == "B" and timezone.now() > booking.endDate:
            vehicle = booking.vehicle
            vehicle.status = "NB"
            vehicle.save()
            booking.status = "E"
            driver = booking.allottedDriver
            booking.allottedDriver = None
            driver.status = "NB"
            booking.save()
            driver.save()
        elif booking.status == "NB" and timezone.now() > booking.endDate:
            booking.status = "E"
            booking.save()

    # ✅ Superuser check first to avoid UserProfile error
    if request.user.is_superuser:
        return render(request, 'booking/bookinglist.html', {
            'bookings': bookings,
            'user': request.user
        })

    # ⛔ Don't fetch UserProfile before this
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect("http://localhost:8000/home/404")

    # Role-based filters
    if user_profile.role == 'customer':
        user_bookings = Book.objects.filter(allottedUser=request.user)
        return render(request, 'booking/bookinglist.html', {
            'bookings': user_bookings,
            'user': request.user
        })
    elif user_profile.role == 'driver':
        try:
            driver_instance = Driver.objects.get(user=request.user)
            driver_bookings = Book.objects.filter(allottedDriver=driver_instance)
        except Driver.DoesNotExist:
            driver_bookings = []  # Empty list if driver record not found
        return render(request, 'booking/bookinglist.html', {
            'bookings': driver_bookings,
            'user': request.user
        })
    return redirect("http://localhost:8000/home/404")

def delete(request, id):
    if request.user.is_authenticated:
        booking = get_object_or_404(Book, id=id)
        booking.delete()
        return redirect('http://localhost:8000/booking/bookings')
    return redirect("http://localhost:8000/home/404")

def change(request, id):
    if request.user.is_authenticated:
        booking = get_object_or_404(Book, id=id)
        vehicle = booking.vehicle

        if booking.status == "B":
            vehicle.status = "NB"
            driver = booking.allottedDriver
            driver.status = "NB"
            vehicle.save()
            driver.save()
            booking.status = "NB"
            booking.allottedDriver = None
            booking.save()
        else:
            drivers = Driver.objects.filter(status="NB")
            if drivers.exists():
                for driver in drivers:
                    if vehicle.status == "B":
                        return redirect('http://localhost:8000/booking/bookings')
                    booking.status = "B"
                    vehicle.status = "B"
                    vehicle.save()
                    booking.allottedDriver = driver
                    driver.status = "B"
                    driver.save()

                    msg = EmailMessage(
                        'Your Booking Has Been Confirmed',
                        f"Your booking is confirmed. Driver: {driver.firstName} {driver.lastName}, Contact: {driver.phoneNumber}",
                        'noreply@roadlink.com',
                        [booking.allottedUser.email],
                    )
                    msg.send()
                    booking.save()
                    break
            else:
                return redirect('http://localhost:8000/booking/bookings')
        return redirect('http://localhost:8000/booking/bookings')
    return redirect("http://localhost:8000/home/404")
