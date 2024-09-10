import datetime
import humanize

from PIL import Image
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels

from portal.models import  User, Category


class Company(models.Model):
    employer = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    co_introduction = models.TextField()
    logo = models.ImageField(default='default.png', upload_to='co-logo')
    link  = models.CharField(max_length=80)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)

        img = Image.open(self.logo.path)


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    created_date = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    experience_choices = (
        ('no-matter','اړین نه دی'),
        ('1-3', 'یو نه تر ۳ کاله'),
        ('3-6', 'دری نه تر ۶ کاله'),
        ('+6', 'ډیر له ۶ کاله'),
    )
    experience = models.CharField(max_length=80, choices=experience_choices)
    salary_choices = (
        ('agreement ', 'توافقی'),
        ('from 3', 'له ۳ زره'),
        ('from 5', 'له ۵ زره'),
        ('from 8', 'له ۸ زره'),
        ('from 10', 'له ۱۰ زره'),
        ('from 12', 'له ۱۲ زره'),
        ('from 15', 'له ۱۵ زره'),
    )
    salary = models.CharField(
        max_length=80, choices=salary_choices
    )
    cooperation_choices = (
        ('full-time', 'مکمل ورځ'),
        ('part-time', 'نمیه ورځ'),
        ('remote', 'ریموت'),
        ('internship', 'کار آموزی'),
    )
    cooperation_type = models.CharField(
        max_length=80, choices=cooperation_choices
    )
    job_description = models.TextField()
    skills_required = models.CharField(max_length=80)
    military_choices = (
        ('no-matter', 'اړین نه دی'),
        ('end', 'کار پای'),
    )
    military_service = models.CharField(
        max_length=80, choices=military_choices
    )
    degree_choices = (
        ('no-matter', 'اړین نه دی'),
        ('diploma', 'دیپلم'),
        ('bachelor', 'لیسانس'),
    )
    degree = models.CharField(max_length=80, choices=degree_choices)
    gender_choices = (
        ('Male', 'نر'),
        ('Female', 'ښځینه'),
        ('not-matter','اړین نه دی'),
    )
    gender = models.CharField(max_length=10, choices=gender_choices)

    def __str__(self):
        return self.title
    
    
class JobRequests(models.Model):
    employer = models.ForeignKey(Company, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume_url = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    hired = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.jobseeker} requested on {self.job}'
    
    def save(self, *args, **kwargs):
        super(JobRequests, self).save(*args, **kwargs)