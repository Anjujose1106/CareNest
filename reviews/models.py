from django.db import models
from carers.models import Carer


class Review(models.Model):

    carer = models.ForeignKey(
        Carer,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    reviewer_name = models.CharField(
        max_length=100
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.reviewer_name