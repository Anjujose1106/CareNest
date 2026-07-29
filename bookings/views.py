from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
from carers.models import Carer


@login_required
def create_booking(request, carer_id):

    carer = get_object_or_404(Carer, id=carer_id)

    if request.method == "POST":

        Booking.objects.create(
            family=request.user,
            client_name=request.POST["client_name"],
            client_email=request.POST["client_email"],
            carer=carer,
            care_type=request.POST["care_type"],
            booking_date=request.POST["booking_date"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
        )

        return redirect('booking_success')

    return render(
        request,
        'bookings/create_booking.html',
        {'carer': carer}
    )
def booking_success(request):
    return render(
        request,
        'bookings/booking_success.html'
    )

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        family=request.user
    ).order_by('-created_at')

    return render(
        request,
        'bookings/my_bookings.html',
        {'bookings': bookings}
    )