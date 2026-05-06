from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('ORGANIZER', 'Organizer'),
        ('ADMIN', 'Admin'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('REJECTED', 'Rejected'),
    )

    department = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    college_id_image = models.ImageField(upload_to='id_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
