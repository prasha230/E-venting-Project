from django import forms
from django.forms import ModelForm
from .models import Venue,Event

class VenueForm(ModelForm):
    class Meta:
        model=Venue
        fields=('name','address','pin_code','phone','web','email','venue_image')
        labels={
            'name':'',
            'address':'',
            'pin_code':'',
            'phone':'',
            'web':'',
            'email':'',
            'venue_image':'',
        }
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'pin_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pin Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Website'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'})
        }

#Admin Event Form
class EventFormAdmin(ModelForm):
    class Meta:
        model=Event
        fields=('name','event_date','venue','manager','attendees','description')
        labels={
            'name' : '',
            'event_date' : 'YYYY-MM-DD HH:MM:SS',
            'venue' : 'Venue',
            'manager' : 'Manager',
            'attendees' : 'Attendees',
            'description' : '',
        }
        widgets={
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date' : forms.DateInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'venue' : forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
            'manager' : forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
            'attendees' : forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description','rows':5,'columns':15})
        }

#User Event Form
class EventForm(ModelForm):
    class Meta:
        model=Event
        fields=('name','event_date','venue','attendees','description')
        labels={
            'name' : '',
            'event_date' : 'YYYY-MM-DD HH:MM:SS',
            'venue' : 'Venue',
            'attendees' : 'Attendees',
            'description' : '',
        }
        widgets={
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date' : forms.DateInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'venue' : forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
            'attendees' : forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description','rows':5,'columns':15})
        }