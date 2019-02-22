from __future__ import unicode_literals
from django.db import models
import re
import datetime

# Create your models here.
class UserManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be more than 2 characters long"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be more than 2 characters long"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email needs to be a valid email"
        if User.objects.filter(email=postData['email']).count() >= 1:
            errors["email"] = "Not a unique email"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be more than 2 characters long"
        if postData['cpassword'] != postData['password']:
            errors["cpassword"] = "Passwords needs to match"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["login_email"] = "Email needs to be a valid email"
        if len(postData['password']) < 1:
            errors["login_password"] = "Password should be more than 2 characters long"
        if User.objects.filter(email=postData['email']).count() < 1:
            errors["duplicate_email"] = "Not a user"
        return errors

class TripManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        print(postData['end'])
        if len(postData['dest']) < 3:
            errors["dest"] = "A trip destination must consist of at least 3 characters!"
        if len(postData['plan']) < 3:
            errors["plan"] = "A trip plan must consist of at least 3 characters!"
        if len(postData['start']) < 1:
            errors["start"] = "A trip plan must have a start date"
        if len(postData['end']) < 1:
            errors["end"] = "A trip plan must have an end date"
        now = datetime.datetime.now()
        date_format = "%Y-%m-%d"
        start = datetime.datetime.strptime(postData['start'], date_format)
        end = datetime.datetime.strptime(postData['end'], date_format)
        if start < now:
            errors["start"] = "need to start an event later on in the future"
        if end < now:
            errors["end"] = "can't end an even in the past"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    desti = models.CharField(max_length=45)
    start = models.DateTimeField()
    end = models.DateTimeField()
    plan = models.TextField()
    event_owner = models.ForeignKey(User, related_name="trips_owned")
    event_attendees = models.ManyToManyField(User, related_name="eventes_attending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()