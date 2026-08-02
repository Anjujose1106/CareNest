from django.db import models
from django.contrib.auth.models import User

def document_upload_path(instance, filename):

    extension = filename.split('.')[-1]

    carer_name = instance.carer.full_name.replace(" ", "_")

    doc_name = instance.document_name.replace(" ", "_")

    return (
        f"carer_documents/"
        f"{carer_name}_{doc_name}.{extension}"
    )
    
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
        ('Personal Care', 'Personal Care'),
        ('Dementia Care', 'Dementia Care'),
        ('Companionship', 'Companionship'),
        ('Overnight Care', 'Overnight Care'),
        ('Respite Care', 'Respite Care'),
        ('Learning Disabilities Support', 'Learning Disabilities Support'),
        ('Autism Support', 'Autism Support'),
        ('Live-in Care', 'Live-in Care'),
        ('Mobility Support', 'Mobility Support'),
        ('Domestic Support', 'Domestic Support'),
        ('Shopping & Community Access', 'Shopping & Community Access'),
    )
   
    care_type = models.CharField(
        max_length=50,
        choices=CARE_TYPES,
        default='Personal Care'
    )

    services_offered = models.JSONField(
        default=list,
        blank=True
    )
    full_name = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True
    )

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
    
    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
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
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
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

class CarerDocument(models.Model):

    DOCUMENT_CHOICES = (
        ('DBS Certificate', 'DBS Certificate'),
        ('Right to Work', 'Right to Work'),
        ('Public Liability Insurance', 'Public Liability Insurance'),
        ('First Aid', 'First Aid'),
        ('Moving & Handling', 'Moving & Handling'),
        ('Safeguarding Adults', 'Safeguarding Adults'),
        ('Medication Administration', 'Medication Administration'),
        ('Dementia Awareness', 'Dementia Awareness'),
        ('Infection Control', 'Infection Control'),
        ('Autism Awareness', 'Autism Awareness'),
        ('Care Certificate', 'Care Certificate'),
        ('NVQ Level 2', 'NVQ Level 2'),
        ('NVQ Level 3', 'NVQ Level 3'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    

    carer = models.ForeignKey(
        Carer,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    issue_date = models.DateField(
        null=True,        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to=document_upload_path
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.carer.full_name} - {self.document_name}"
    
    