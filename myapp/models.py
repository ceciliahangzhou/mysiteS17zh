from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    # age = models.IntegerField()
    city = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return self.firstname+' '+self.lastname

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    in_stock = models.BooleanField(default=True)
    numpages = models.IntegerField(null=True)

    def __str__(self):
        return self.title

class Student(User):
    PROVINCE_CHOICES = (
        ('AB','Alberta'), # First value is stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    age = models.IntegerField()
    class Meta:
        verbose_name="Student"
        verbose_name_plural="Students"

    def __str__(self):
        return self.first_name+' '+self.last_name

class Course(models.Model):
    course_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    textbook = models.ForeignKey(Book)
    students = models.ManyToManyField(Student,null=True, blank=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    intro_course = models.BooleanField(default=True)
    NO_PREFERENCE = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    TIME_CHOICES = (
        (0, 'No preference'),
        (1, 'Morning'),
        (2, 'Afternoon'),
        (3, 'Evening')
    )
    time = models.IntegerField(default=0, choices=TIME_CHOICES)
    num_responses = models.IntegerField(default=0)
    avg_age = models.IntegerField(default=20)

    def __str__(self):
        return str(self.id)+ ' '+ self.subject
