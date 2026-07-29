from django.contrib import admin
from .models import Carer, CarerApplication


@admin.register(Carer)
class CarerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'care_type',
        'postcode',
        'hourly_rate',
        'dbs_verified',
    )

    list_filter = (
        'care_type',
        'dbs_verified',
        'gender',
    )

    search_fields = (
        'full_name',
        'postcode',
        'care_type',
    )


@admin.register(CarerApplication)
class CarerApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone_number',
        'postcode',
        'care_type',
        'approved',
        'submitted_at',
    )

    list_filter = (
        'care_type',
        'approved',
        'submitted_at',
    )

    search_fields = (
        'full_name',
        'email',
        'phone_number',
        'postcode',
    )