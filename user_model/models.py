from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=30)
    password = models.CharField(max_length=20, default="Changeme@123", blank=True)
    phone_number = models.CharField(max_length=10,unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    height = models.CharField(max_length=10)  # Example: "170 cm"
    weight = models.CharField(max_length=10)  # Example: "70 kg"
    city = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True, null=True)
    genetic_predisposition = models.TextField(blank=True, null=True)
    smoking = models.TextField(blank=True, null=True)
    drinking = models.TextField(blank=True, null=True)
    sleeping_hours = models.TextField(blank=True, null=True)
    exercise_hours = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.full_name