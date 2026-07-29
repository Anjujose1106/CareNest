from django.db import models
from carers.models import Carer


class Booking(models.Model):

    CARE_TYPES = (
        ('elderly', 'Elderly Care'),
        ('dementia', 'Dementia Care'),
        ('personal', 'Personal Care'),
        ('overnight', 'Overnight Care'),
        ('companionship', 'Companionship'),
    )

    client_name = models.CharField(max_length=100)

    client_email = models.EmailField()

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.client_name} - {self.carer}"