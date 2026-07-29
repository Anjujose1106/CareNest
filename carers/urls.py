from django.urls import path
from .views import home, carer_list, carer_detail, join

urlpatterns = [
    path('', home, name='home'),
    path('carers/', carer_list, name='carer_list'),
    path('carer/<int:id>/', carer_detail, name='carer_detail'),
    path('join/', join, name='join'),
]
