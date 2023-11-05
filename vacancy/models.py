from datetime import datetime, timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class VacantType(models.TextChoices):
    Permanent = 'Permanent'
    Temporary = 'Temporary'
    Internship = 'Internship'

class Education(models.TextChoices):
    No = 'No'
    Bachelors = 'Bachelors'
    Masters = 'Masters'
    Phd = 'Phd'

class Experience(models.TextChoices):
    No = 'No'
    One_year = '1 year'
    Three_years = '3 years'
    Five_years = '5 years above'

class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    email = models.EmailField()
    address = models.CharField(max_length = 100)
    vacancyType = models.CharField(
        max_length = 10,
        choices = VacantType.choices,
        default = VacantType.Permanent
    )
    education = models.CharField(
        max_length = 10,
        choices = Education.choices,
        default = Education.Bachelors
    )
    experience = models.CharField(
        max_length = 20,
        choices = Experience.choices,
        default = Experience.No
    )
    salary = models.FloatField(
        default=1,
        validators = [
            MinValueValidator(1),
            MaxValueValidator(1000000)
        ]
    )
    positions = models.IntegerField(default=1)
    last_date = models.DateTimeField(default = datetime.now() + timedelta(days=15))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)

    class Meta: 
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"


class CandidatesApplied(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resume = models.CharField(max_length=250)
    appliedAt = models.DateTimeField(auto_now_add=True)