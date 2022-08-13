from django.db import models
from userapp.models import User


class Gender:
    choices = (('male', 'Male'), ('female', 'Female'))


class Animal(models.Model):
    Seller = models.ForeignKey(User, on_delete=models.PROTECT)
    Species_Name = models.CharField(max_length=50)
    Breed = models.CharField(max_length=50)
    Sex = models.CharField(choices=Gender.choices)
    Age = models.PositiveIntegerField()
    Price = models.PositiveIntegerField()
    Animal_Image = models.ImageField(upload_to='/animals/')
    Animal_Clip = models.FileField(upload_to='/animals_clips/')


