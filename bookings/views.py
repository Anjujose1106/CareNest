from django.shortcuts import render, redirect, get_object_or_404

from .models import Booking
from carers.models import Carer


def create_booking(request, carer_id):

    carer = get_object_or_404(Carer, id=carer_id)

    if request.method == "POST":

        Booking.objects.create(
            client_name=request.POST["client_name"],
            client_email=request.POST["client_email"],
            carer=carer,
            care_type=request.POST["care_type"],
            booking_date=request.POST["booking_date"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
        )

        return redirect('/')

    return render(
        request,
        'bookings/create_booking.html',
        {'carer': carer}
    )