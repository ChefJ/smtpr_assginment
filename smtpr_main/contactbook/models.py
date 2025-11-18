from django.db import models

# Create your models here.
from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    # instead of deleting right away we hide the 'deleted' ones and detect & delete them every 24 hours

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now=True)

    labels = models.ManyToManyField(Label,
                                    related_name="contacts",
                                    blank=True)

    is_deleted = models.BooleanField(default=False)
    # instead of deleting right away we hide the 'deleted' ones and detect & delete them every 24 hours

    def __str__(self):
        return self.name
