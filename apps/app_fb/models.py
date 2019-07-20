from django.db import models
from apps.helpers import stringify_obj, key_formatter
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.timezone import now
from datetime import date, datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def registration_valid(self, request):
        for key, val in request.POST.items():
            if len(val) < 2:
                if key is not "confirm":
                    messages.error(request, f"{key_formatter(key)} must be more than 2 characters.")
        
        if request.POST['password'] != request.POST['confirm']:
            messages.error(request, "Passwords must match.")
        
        if User.objects.filter(email = request.POST['email']):
            messages.error(request, "Email taken.")
        
        if not EMAIL_REGEX.match(request.POST['email']): 
            messages.error(request, "Invalid email address!")
        
        today = date.today() 
        bday = int(request.POST['dateofbirth'][:4])
        
        if today.year - bday < 12: 
            messages.error(request, "You are too young for an account")
        

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 70)
    birthdate = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager() # old objects extended to have added functionality
    
    def __repr__(self):
        return stringify_obj(self)

    def __str__(self):
        return stringify_obj(self)

class Book(models.Model):
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 500)
    # the user who uploaded a given book
    uploaded_by = models.ForeignKey(User, related_name = "books_uploaded")
    # a list of users who like a given book
    users_who_like = models.ManyToManyField(User, related_name = "liked_books")
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return stringify_obj(self)

    def __str__(self):
        return stringify_obj(self)

    
