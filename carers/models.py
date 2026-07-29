from django.db import models


class Carer(models.Model):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    full_name = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to='carers/',
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='female'
    )

    postcode = models.CharField(max_length=20)

    experience_years = models.PositiveIntegerField()

    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    bio = models.TextField()

    dbs_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.full_name

    @property
    def average_rating(self):

        reviews = self.reviews.all()

        if not reviews:
            return 0

        total = sum(review.rating for review in reviews)

        return round(total / len(reviews), 1)