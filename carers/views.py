from django.shortcuts import render, get_object_or_404, redirect
from .models import Carer, CarerApplication, Availability
from .forms import CarerApplicationForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from bookings.models import Booking
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from bookings.models import Booking
from reviews.models import Review
from datetime import date, timedelta
import calendar
from datetime import date

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
    if request.method == "POST":
        Availability.objects.create(
            carer=carer,
            date=request.POST["date"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"]
        )
    print("POST RECEIVED")

    availabilities = Availability.objects.filter(
        carer=carer
    ).order_by('date')

    
    today = date.today()

    upcoming_bookings = Booking.objects.filter(
        carer=carer,
        booking_date__gte=today
    ).order_by('booking_date', 'start_time')

    past_bookings = Booking.objects.filter(
    carer=carer,
    status='completed'
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

    today = date.today()

    month = request.GET.get("month")
    year = request.GET.get("year")

    if month is None:
        month = today.month

    if year is None:
        year = today.year

    month = int(month)
    year = int(year)

    if month > 12:
        month = 1
        year += 1

    if month < 1:
        month = 12
        year -= 1

    cal = calendar.monthcalendar(year, month)

    month_name = calendar.month_name[month]

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
            'availabilities': availabilities,
            'calendar': cal,
            'month': month,
            'year': year,
            'month_name': month_name,
        }
   )
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):

    total_carers = Carer.objects.count()

    total_families = User.objects.filter(
        is_superuser=False
    ).count()

    total_bookings = Booking.objects.count()

    pending_applications = CarerApplication.objects.filter(
        status='pending'
    ).count()

    total_reviews = Review.objects.count()

    return render(
        request,
        'carers/admin_dashboard.html',
        {
            'total_carers': total_carers,
            'total_families': total_families,
            'total_bookings': total_bookings,
            'pending_applications': pending_applications,
            'total_reviews': total_reviews,
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def admin_applications(request):

    applications = CarerApplication.objects.all().order_by('-submitted_at')

    return render(
        request,
        'carers/admin_applications.html',
        {
            'applications': applications
        }
    )
@user_passes_test(lambda u: u.is_superuser)
def approve_application(request, application_id):

    application = get_object_or_404(
        CarerApplication,
        id=application_id
    )

    application.status = 'approved'
    application.save()

    return redirect('/admin-dashboard/applications/')


@user_passes_test(lambda u: u.is_superuser)
def reject_application(request, application_id):

    application = get_object_or_404(
        CarerApplication,
        id=application_id
    )

    application.status = 'rejected'
    application.save()

    return redirect('/admin-dashboard/applications/')

@user_passes_test(lambda u: u.is_superuser)
def admin_bookings(request):

    pending_bookings = Booking.objects.filter(
        status='pending'
    ).order_by('booking_date')

    confirmed_bookings = Booking.objects.filter(
        status='confirmed'
    ).order_by('booking_date')

    completed_bookings = Booking.objects.filter(
        status='completed'
    ).order_by('-booking_date')

    cancelled_bookings = Booking.objects.filter(
        status='cancelled'
    ).order_by('-booking_date')

    return render(
        request,
        'carers/admin_bookings.html',
        {
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def confirm_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    booking.status = 'confirmed'
    booking.save()

    return redirect('/admin-dashboard/bookings/')


@user_passes_test(lambda u: u.is_superuser)
def complete_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    booking.status = 'completed'
    booking.save()

    return redirect('/admin-dashboard/bookings/')


@user_passes_test(lambda u: u.is_superuser)
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    booking.status = 'cancelled'
    booking.save()

    return redirect('/admin-dashboard/bookings/')

@user_passes_test(lambda u: u.is_superuser)
def admin_calendar(request):

    today = date.today()

    week_days = []

    for i in range(7):

        current_day = today + timedelta(days=i)

        day_bookings = Booking.objects.filter(
            booking_date=current_day
        ).order_by('start_time')

        week_days.append({
            'date': current_day,
            'bookings': day_bookings
        })

    return render(
    request,
    'carers/admin_calendar.html',
    {
        'week_days': week_days,
        'pending_count': Booking.objects.filter(status='pending').count(),
        'confirmed_count': Booking.objects.filter(status='confirmed').count(),
        'completed_count': Booking.objects.filter(status='completed').count(),
        'cancelled_count': Booking.objects.filter(status='cancelled').count(),
    }
)