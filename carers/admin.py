from django.contrib import admin
from .models import Carer, CarerApplication
from .models import Availability
from .models import CarerDocument

admin.site.register(Availability)

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
        'status',
        'submitted_at',
    )

    list_filter = (
        'care_type',
        'status',
        'submitted_at',
    )

    search_fields = (
        'full_name',
        'email',
        'phone_number',
        'postcode',
    )

@admin.register(CarerDocument)
class CarerDocumentAdmin(admin.ModelAdmin):

    list_display = (
        'carer',
        'document_name',
        'status',
        'uploaded_at',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'carer__full_name',
        'document_name',
    )  