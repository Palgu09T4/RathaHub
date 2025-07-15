from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse
from booking.models import Book

def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        bookinglist = Book.objects.filter(status="B")
        totdistance = sum([b.distance for b in bookinglist])
        totcost = sum([b.cost for b in bookinglist])
        return render(request, 'report/index.html', {
            'bookinglist': bookinglist,
            'totdistance': totdistance,
            'totcost': totcost
        })
    return redirect("http://localhost:8000/home/404")


def change(request):
    if request.user.is_authenticated and request.user.is_superuser:
        bookinglist = Book.objects.filter(status="B")
        totdistance = sum([b.distance for b in bookinglist])
        totcost = sum([b.cost for b in bookinglist])
        
        msg = EmailMessage(
            'Your Travel Report',
            '<html>...<td> {} Km</td>...<td> Rs {}</td>...</html>'.format(totdistance, totcost),
            'noreply@roadlink.com',
            [request.user.email],
        )
        msg.content_subtype = "html"
        msg.send()

        return redirect('http://localhost:8000/report')
    return redirect("http://localhost:8000/home/404")
