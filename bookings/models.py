from django.db import models
from carers.models import Carer
from django.contrib.auth.models import User


class Booking(models.Model):

    CARE_TYPES = (
        ('elderly', 'Elderly Care'),
        ('dementia', 'Dementia Care'),
        ('personal', 'Personal Care'),
        ('overnight', 'Overnight Care'),
        ('companionship', 'Companionship'),
    )
    family = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    client_name = models.CharField(max_length=100)

    client_email = models.EmailField()

    client_phone = models.CharField(
        max_length=20,
        blank=True
    )

    client_address = models.TextField(
        blank=True
    )

    client_postcode = models.CharField(
        max_length=20,
        blank=True
    )

    carer = models.ForeignKey(
        Carer,
        on_delete=models.CASCADE
    )

    care_type = models.CharField(
        max_length=50,
        choices=CARE_TYPES
    )

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    )

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.client_name} - {self.carer}"