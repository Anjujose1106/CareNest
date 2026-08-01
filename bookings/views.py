from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
from carers.models import Carer
from carers.models import Availability
from datetime import datetime
import calendar
from datetime import date


@login_required
def create_booking(request, carer_id):

    carer = get_object_or_404(Carer, id=carer_id)

    availabilities = Availability.objects.filter(
            carer=carer
    ).order_by('date')

    availability_map = {}

    for availability in availabilities:

        availability_map[
            availability.date.strftime('%Y-%m-%d')
        ] = {
            'start': availability.start_time.strftime('%H:%M'),
            'end': availability.end_time.strftime('%H:%M')
        }
    booked_dates = []

    bookings = Booking.objects.filter(
        carer=carer
    ).exclude(status='cancelled')

    for booking in bookings:
        booked_dates.append(
            booking.booking_date.strftime('%Y-%m-%d')
        )

    print("BOOKINGS:", bookings)
    print("BOOKED DATES:", booked_dates)
   

    today = date.today()

    month = request.GET.get('month', today.month)
    year = request.GET.get('year', today.year)

    if month is None:
        month = today.month
    if year is None:
        year = today.year
    month = int(month)
    year = int(year)

    if month>12:
        month = 1
        year += 1
    if month<1:
        month = 12
        year -= 1
    
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    if request.method == "POST":

        booking_date = request.POST["booking_date"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]

        availability = Availability.objects.filter(
            carer=carer,
            date=booking_date
        ).first()

        if availability is None:

            return render(
                request,
                'bookings/create_booking.html',
                {
                    'carer': carer,
                    'error': 'This carer is not available on the selected date.'
                }
            )

        requested_start = datetime.strptime(
            start_time,
            "%H:%M"
        ).time()

        requested_end = datetime.strptime(
            end_time,
            "%H:%M"
        ).time()

        if (
            requested_start < availability.start_time
            or
            requested_end > availability.end_time
        ):

            return render(
                request,
                'bookings/create_booking.html',
                {
                    'carer': carer,
                    'error': 'Selected time is outside the carer availability.'
                }
            )

        existing_bookings = Booking.objects.filter(
            carer=carer,
            booking_date=booking_date
        ).exclude(status='cancelled')

        for booking in existing_bookings:

            if (
                requested_start < booking.end_time
                and
                requested_end > booking.start_time
            ):
        
        

                return render(
                    request,
                    'bookings/create_booking.html',
                    {
                        'carer': carer,
                        'error': 'Carer already has a booking during this time.'
                    }
                )

        Booking.objects.create(
            family=request.user,
            client_name=request.POST["client_name"],
            client_email=request.POST["client_email"],
            carer=carer,
            care_type=request.POST["care_type"],
            booked_dates=booked_dates,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
        )

        return redirect('booking_success')
   

    return render(
        request,
        'bookings/create_booking.html',
        {
            'carer': carer,
            'availabilities': availabilities,
            'availability_map': availability_map,
            'month': month,
            'year': year,
            'calendar': cal,
            'month_name': month_name,
            'booked_dates': booked_dates
        }
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