from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'client_name',
        'carer',
        'care_type',
        'booking_date',
        'start_time',
        'end_time',
        'status',
        'family',
    )

    list_filter = (
        'status',
        'care_type',
        'booking_date',
    )

    search_fields = (
        'client_name',
        'client_email',
        'carer__full_name',
    )