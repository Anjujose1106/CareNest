from django.db import models
from django.contrib.auth.models import User


class Carer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carer_profile'
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    CARE_TYPES = (
        ('Dementia Care', 'Dementia Care'),
        ('Personal Care', 'Personal Care'),
        ('Companionship', 'Companionship'),
        ('Overnight Care', 'Overnight Care'),
    )
   
    care_type = models.CharField(
        max_length=50,
        choices=CARE_TYPES,
        default='Personal Care'
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



class CarerApplication(models.Model):
    
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    )

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='pending'
    )

    full_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone_number = models.CharField(max_length=20)

    postcode = models.CharField(max_length=20)

    experience_years = models.PositiveIntegerField()

    care_type = models.CharField(
        max_length=50,
        choices=Carer.CARE_TYPES
    )

    message = models.TextField(
        blank=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    
    def __str__(self):
        return self.full_name

class Availability(models.Model):

    DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    carer = models.ForeignKey(
        Carer,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )

    
    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.carer.full_name} - {self.date} ({self.start_time} - {self.end_time})"
