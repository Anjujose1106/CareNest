from django.shortcuts import render, get_object_or_404, redirect
from .models import Carer
from .forms import CarerApplicationForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from bookings.models import Booking

def carer_list(request):

    carers = Carer.objects.all()

    postcode = request.GET.get('q')
    care_type = request.GET.get('care_type')

    if postcode:
        carers = carers.filter(
            postcode__icontains=postcode
        )

    if care_type:
        carers = carers.filter(
            care_type=care_type
        )

    return render(
        request,
        'carers/carer_list.html',
        {
            'carers': carers
        }
    )
def home(request):
    return render(
        request,
        'carers/home.html'
    )


from reviews.models import Review

def carer_detail(request, id):
    carer = get_object_or_404(Carer, id=id)

    reviews = Review.objects.filter(
        carer=carer
    )

    return render(
        request,
        'carers/carer_detail.html',
        {
            'carer': carer,
            'reviews': reviews,
        }
    )
def join(request):
    return render(
        request,
        'carers/join.html'
    )
def apply_carer(request):

    if request.method == 'POST':

        form = CarerApplicationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/join/success/')

    else:
        form = CarerApplicationForm()

    return render(
        request,
        'carers/apply_carer.html',
        {'form': form}
    )
def join_success(request):
    return render(
        request,
        'carers/join_success.html'
    )
@login_required
def carer_dashboard(request):

    carer = getattr(request.user, 'carer_profile', None)

    if carer is None:
        return render(
            request,
            'carers/not_a_carer.html'
        )

    today = date.today()

    upcoming_bookings = Booking.objects.filter(
        carer=carer,
        booking_date__gte=today
    ).order_by('booking_date', 'start_time')

    past_bookings = Booking.objects.filter(
        carer=carer,
        booking_date__lt=today
    ).order_by('-booking_date')

    total_hours = 0

    for booking in past_bookings:

        start_datetime = datetime.combine(
            booking.booking_date,
            booking.start_time
        )

        end_datetime = datetime.combine(
            booking.booking_date,
            booking.end_time
        )

        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)

        duration = end_datetime - start_datetime

        total_hours += duration.total_seconds() / 3600

    estimated_earnings = total_hours * float(carer.hourly_rate)

    next_booking = upcoming_bookings.first()

    return render(
        request,
        'carers/carer_dashboard.html',
        {
            'carer': carer,
            'next_booking': next_booking,
            'upcoming_bookings': upcoming_bookings,
            'past_bookings': past_bookings,
            'total_hours': round(total_hours, 2),
            'estimated_earnings': round(estimated_earnings, 2),
        }
    )