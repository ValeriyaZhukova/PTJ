from django.conf import settings
from django.db import models
import time
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from common.models import City, Industry
from company.models import Company
from transliterate import translit, get_available_language_codes

# Create your models here.


def upload_avatar(instance, filename):
    last_dot = filename.rfind('.')
    extension = filename[last_dot:len(filename):1]
    return 'images/users/%s-%s-%s%s' % (translit(instance.user.first_name, 'ru', reversed=True),
                                        translit(instance.user.last_name, 'ru', reversed=True),
                                        time.time(), extension)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    #objects = CustomUserManager()

    phone_number = PhoneNumberField(blank=True, null=True, help_text='Contact phone number')

    is_aspirant = models.BooleanField('aspirant status', default=False)
    is_contact_person = models.BooleanField('contact person status', default=False)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(blank=True, null=True)
    citizenship = models.CharField(max_length=255)
    desired_position = models.CharField(max_length=255)
    working_experience = models.CharField(max_length=2000)
    education_degree = models.CharField(max_length=255)
    skills = models.CharField(max_length=2000)
    institution = models.CharField(max_length=500, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.FileField(upload_to=upload_avatar, blank=True, null=True, default='images/users/default-avatar.png')


class WorkList(models.Model):
    work_began = models.DateField()
    work_finished = models.DateField()
    position = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)


class Status(models.Model):
    status = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)


class EmployeeRating(models.Model):
    total_rating = models.IntegerField()
    competence = models.IntegerField(blank=True, null=True)
    effectiveness = models.IntegerField(blank=True, null=True)
    responsibility = models.IntegerField(blank=True, null=True)
    communicability = models.IntegerField(blank=True, null=True)
    hard_work = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)


class ProfileIndustries(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=False)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, blank=False, null=False)
