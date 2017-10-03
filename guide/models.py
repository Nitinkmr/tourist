# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class State(models.Model):
	name = models.CharField(max_length=40,unique=True,default="")
	
	def __str__(self):
	       return self.name

class City(models.Model):
	name = models.CharField(max_length=100)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	class Meta:
        	unique_together = (("name", "state"),)

	def __str__(self):
       		return self.name

class touristSpot(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	duration = models.IntegerField()
	description = models.TextField()

	class Meta:
       	 unique_together = (("name", "city"),)

	def __str__(self):
		return self.name