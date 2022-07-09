from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Attendee(User):
    class Meta:
        proxy = True
    def __str__(self):
        return self.first_name + ' ' +self.last_name + ' (' +self.email + ')'

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    pin_code = models.CharField('Pin Code', max_length=10)
    phone = models.CharField('Contact', max_length=25, blank=True)
    web = models.URLField('Web Address', blank=True)
    email = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name 


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,related_name='manager')
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(Attendee, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).split(',', 1)[0]
        return days_till_stripped

    @property
    def Is_past(self):
        today = date.today()
        if self.event_date.date() > today:
            occurred = 'Future'
        else:
            occurred = 'Past'
        return occurred

