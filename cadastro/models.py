from django.db import models

class Person(models.Model):
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
    
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.first_name
