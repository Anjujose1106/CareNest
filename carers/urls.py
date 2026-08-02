from django.urls import path
from .views import home, carer_list, carer_detail, join,apply_carer, join_success, carer_dashboard, admin_dashboard, admin_applications, approve_application, reject_application, admin_bookings, confirm_booking, complete_booking, cancel_booking, admin_calendar, upload_document, admin_documents,admin_carers,admin_carer_detail, approve_document, reject_document    

urlpatterns = [
    path('', home, name='home'),
    path('carers/', carer_list, name='carer_list'),
    path('carer/<int:id>/', carer_detail, name='carer_detail'),
    path('join/', join, name='join'),
    path('join/apply/', apply_carer, name='apply_carer'),
    path('join/success/', join_success, name='join_success'),
    path('carer-dashboard/', carer_dashboard, name='carer_dashboard'),
    path(
        'upload-document/',
        upload_document,
        name='upload_document'
    ),
    path(
        'admin-dashboard/documents/',
        admin_documents,
        name='admin_documents'
    ),
    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),
    path(
        'admin-dashboard/carers/<int:carer_id>/',
        admin_carer_detail,
        name='admin_carer_detail'
    ),
    path(
        'admin-dashboard/carers/',
        admin_carers,
        name='admin_carers'
    ),
    path(
        'admin-dashboard/documents/<int:document_id>/approve/',
        approve_document,
        name='approve_document'
    ),

    path(
        'admin-dashboard/documents/<int:document_id>/reject/',
        reject_document,
        name='reject_document'
    ),

    path(
        'admin-dashboard/applications/',
        admin_applications,
        name='admin_applications'
    ),
    path(
        'admin-dashboard/applications/<int:application_id>/approve/',
        approve_application,
        name='approve_application'
    ),

    path(
        'admin-dashboard/applications/<int:application_id>/reject/',
        reject_application,
        name='reject_application'
    ),
    path(
        'admin-dashboard/bookings/',
        admin_bookings,
        name='admin_bookings'
    ),

    path(
        'admin-dashboard/bookings/<int:booking_id>/confirm/',
        confirm_booking,
        name='confirm_booking'
    ),

    path(
        'admin-dashboard/bookings/<int:booking_id>/complete/',
        complete_booking,
        name='complete_booking'
    ),

    path(
        'admin-dashboard/bookings/<int:booking_id>/cancel/',
        cancel_booking,
        name='cancel_booking'
    ),
    path(
        'admin-dashboard/calendar/',
        admin_calendar,
        name='admin_calendar'
    ),
    ]
