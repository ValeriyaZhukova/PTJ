from django.db import models
import time
from common.models import City, Industry
from django.conf import settings


# Create your models here.


def upload_company_image(instance, filename):
    last_dot = filename.rfind('.')
    extension = filename[last_dot:len(filename):1]
    return 'images/companies/%s-%s%s' % (instance.name, time.time(), extension)


class Company(models.Model):
    name = models.CharField(max_length=255)
    bin = models.CharField(max_length=12)
    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    website = models.URLField(max_length=200)
    image = models.FileField(upload_to=upload_company_image, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    contact_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)


class CompanyRating(models.Model):
    total_rating = models.IntegerField()
    salary = models.IntegerField(blank=True, null=True)
    conditions = models.IntegerField(blank=True, null=True)
    atmosphere = models.IntegerField(blank=True, null=True)
    interesting_job = models.IntegerField(blank=True, null=True)
    reputation = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)


class Comments(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    salary = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=255)
    required_experience = models.CharField(max_length=255)
    duties = models.CharField(max_length=2000)
    requirements = models.CharField(max_length=2000)
    conditions = models.CharField(max_length=2000)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)


class VacancyIndustries(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, blank=False, null=False)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, blank=False, null=False)


class AppliedVacancies(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, blank=False, null=False)


class FavoriteVacancies(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, blank=False, null=False)
