from django.urls import path
from .views import home, carer_list, carer_detail, join,apply_carer, join_success,carer_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('carers/', carer_list, name='carer_list'),
    path('carer/<int:id>/', carer_detail, name='carer_detail'),
    path('join/', join, name='join'),
    path('join/apply/', apply_carer, name='apply_carer'),
    path('join/success/', join_success, name='join_success'),
    path('carer-dashboard/', carer_dashboard, name='carer_dashboard'),
]
