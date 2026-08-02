from django.shortcuts import render, get_object_or_404, redirect
from .models import Carer, CarerApplication, Availability, CarerDocument
from .forms import CarerApplicationForm, CarerDocumentForm, CarerSettingsForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from bookings.models import Booking
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from bookings.models import Booking
from reviews.models import Review
from datetime import date, timedelta
import calendar
from datetime import date, datetime, timedelta

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

        if "save_settings" in request.POST:

            settings_form = CarerSettingsForm(
                request.POST,
                request.FILES,
                instance=carer
            )

            print(settings_form.fields.keys())

            if settings_form.is_valid():

                settings_form.save()

                return redirect(
                    "/carer-dashboard/#settings"
                )

        if "document_name" in request.POST:

            form = CarerDocumentForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():

                document = form.save(commit=False)

                existing = CarerDocument.objects.filter(
                    carer=carer,
                    document_name=document.document_name
                ).first()

                if existing:

                    existing.issue_date = document.issue_date
                    existing.expiry_date = document.expiry_date
                    existing.file = document.file
                    existing.status = "pending"
                    existing.save()

                else:

                    document.carer = carer
                    document.save()

                return redirect("/carer-dashboard/#documents")

        else:

            status = request.POST["status"]

            if status == "unavailable":

                Availability.objects.create(
                    carer=carer,
                    date=request.POST["date"],
                    start_time="00:00",
                    end_time="00:00",
                    status=status
                )
                return redirect("/carer-dashboard/#availability")

            else:

                Availability.objects.create(
                    carer=carer,
                    date=request.POST["date"],
                    start_time=request.POST["start_time"],
                    end_time=request.POST["end_time"],
                    status=status
                )
                return redirect("/carer-dashboard/#availability")
    print("POST RECEIVED")

    availabilities = Availability.objects.filter(
       carer=carer
    ).order_by('date')

    documents = CarerDocument.objects.filter(
        carer=carer
    ).order_by('-uploaded_at')

    document_form = CarerDocumentForm()
    settings_form = CarerSettingsForm(
        instance=carer
    )

    available_dates = []
    unavailable_dates = []

    for availability in availabilities:

        date_string = availability.date.strftime('%Y-%m-%d')

        if availability.status == 'available':
            available_dates.append(date_string)

        else:
            unavailable_dates.append(date_string)

        
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
            'calendar': cal,
            'month': month,
            'year': year,
            'month_name': month_name,
            'availabilities': availabilities,
            'calendar': cal,
            'month': month,
            'year': year,
            'month_name': month_name,
            'available_dates': available_dates,
            'unavailable_dates': unavailable_dates,
            'documents': documents,
            'document_form': document_form,
            'today': date.today(),
            'settings_form': settings_form,
        }
   )

@login_required
def upload_document(request):

    carer = getattr(request.user, 'carer_profile', None)

    if carer is None:
        return render(
            request,
            'carers/not_a_carer.html'
        )

    if request.method == 'POST':

        form = CarerDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save(commit=False)
            document.carer = carer
            document.save()

            return redirect('/carer-dashboard/#documents')

    else:
        form = CarerDocumentForm()

    return render(
        request,
        'carers/upload_document.html',
        {
            'form': form
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

    pending_documents = CarerDocument.objects.filter(
        status='pending'
    ).count()

    expired_documents = CarerDocument.objects.filter(
        expiry_date__lte=date.today()
    ).count()

    documents = CarerDocument.objects.all().order_by(
        '-uploaded_at'
    )[:5]   

    return render(
        request,
        'carers/admin_dashboard.html',
        {
            'total_carers': total_carers,
            'total_families': total_families,
            'total_bookings': total_bookings,
            'pending_applications': pending_applications,
            'total_reviews': total_reviews,
            'pending_documents': pending_documents,
            'expired_documents': expired_documents,
            'documents': documents,
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

@user_passes_test(lambda u: u.is_superuser)
def admin_documents(request):

    documents = CarerDocument.objects.all().order_by(
        '-uploaded_at'
    )

    return render(
        request,
        'carers/admin_documents.html',
        {
            'documents': documents
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def admin_carers(request):

    carers = Carer.objects.all()

    return render(
        request,
        'carers/admin_carers.html',
        {
            'carers': carers
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def admin_carer_detail(request, carer_id):

    carer = get_object_or_404(
        Carer,
        id=carer_id
    )

    documents = CarerDocument.objects.filter(
    carer=carer
    )

    today = date.today()

    for document in documents:

        if document.expiry_date:

            days_left = (
                document.expiry_date - today
            ).days

            if days_left <= 0:

                document.compliance = "expired"

            elif days_left <= 30:

                document.compliance = "expiring"

            else:

                document.compliance = "valid"

        else:

            document.compliance = "unknown"

    bookings = Booking.objects.filter(
        carer=carer
    )

    return render(
        request,
        'carers/admin_carer_detail.html',
        {
            'carer': carer,
            'documents': documents,
            'bookings': bookings,
            'today': today
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def approve_document(request, document_id):

    document = get_object_or_404(
        CarerDocument,
        id=document_id
    )

    document.status = 'approved'
    document.save()

    return redirect(
        '/admin-dashboard/carers/'
        f'{document.carer.id}/'
    )

@user_passes_test(lambda u: u.is_superuser)
def reject_document(request, document_id):

    document = get_object_or_404(
        CarerDocument,
        id=document_id
    )

    document.status = 'rejected'
    document.save()

    return redirect(
        '/admin-dashboard/carers/'
        f'{document.carer.id}/'
    )