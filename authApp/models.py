from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ACKNOWLEDGE_LEVEL_CHOICES = [
        ('Beginner', 'Principiante'),
        ('Intermediate', 'Intermedio'),
        ('Advanced', 'Avanzado'),
    ]
    ROLE_CHOICES = [
        ('Student', 'Estudiante'),
        ('Teacher', 'Profesor'),
    ]
    INSTRUMENT_CHOICES = [
        ('Piano', 'Piano'),
        ('Guitar', 'Guitarra'),
        ('Violin', 'Violín'),
        ('Drums', 'Batería'),
        ('Flute', 'Flauta'),
        ('Saxophone', 'Saxofón'),
        ('Trumpet', 'Trompeta'),
        ('Bass', 'Bajo'),
        ('Cello', 'Violonchelo'),
        ('Clarinet', 'Clarinete'),
    ]

    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    acknowledge_level = models.CharField(max_length=20, choices=ACKNOWLEDGE_LEVEL_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    instrument = models.CharField(max_length=20, choices=INSTRUMENT_CHOICES, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.role if self.role else 'No role assigned'}"
