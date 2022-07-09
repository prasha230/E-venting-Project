# from urllib import request
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib import messages
from members.forms import RegisterUserForm
from django.contrib.auth import authenticate, login

def update_profile(request):
    user=User.objects.get(pk=request.user.id)
    form=RegisterUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        username=form.cleaned_data['username']
        password=form.cleaned_data['password1']
        user=authenticate(username=username,password=password)
        login(request,user)
        messages.success(request,'Profile Updated Successfully')
        return redirect('my-profile')
    return render(request,'events/update_profile.html',{'form':form})

def my_profile(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        events=Event.objects.filter(manager=request.user.id).order_by('event_date')
        venues=Venue.objects.filter(owner=request.user.id)
        return render(request,'events/my_profile.html',{'events':events,'venues':venues})
    else:
        messages.success(request, ("You aren't authorized to view this page"))
        return redirect('home')

def show_event(request, event_id):
    event=Event.objects.get(pk=event_id)
    return render(request,'events/show_event.html',{'event':event})

def venue_events(request,venue_id):
    venue=Venue.objects.get(id=venue_id)
    events = venue.event_set.all()
    if events:
        return render(request,'events/venue_events.html',{'venue':venue,'events':events})
    else:
        messages.success(
            request, ("No events at "+venue.name+"!!"))
        return redirect('admin-approval')

def admin_approval(request):
    venue_list = Venue.objects.all()

    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            # unchecking everything before checking the new list
            event_list.update(approved=False)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(
                request, ('Event List Approval had been updated!'))
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html', {
                'event_list': event_list,
                'event_count':event_count,
                'venue_count':venue_count,
                'user_count':user_count,
                'venue_list':venue_list})
    else:
        messages.success(
            request, ('You are not authorised to view this page!!'))
        return redirect('home')
    return render(request, 'events/admin_approval.html')


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me).order_by('-event_date')
        return render(request, 'events/my_events.html', {'events': events})
    else:
        messages.success(request, ("You aren't authorized to view this page"))
        return redirect('home')


def venue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 12)
    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.pin_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email)
        lines.append(' ')
        lines.append(' ')
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='venues.pdf')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    venues = Venue.objects.all().order_by('name')
    writer = csv.writer(response)
    writer.writerow(['Venue Name', 'Address', 'Pin Code',
                    'Phone', 'Website', 'Email'])
    for venue in venues:
        writer.writerow([venue, venue.address, venue.pin_code,
                        venue.phone, venue.web, venue.email])
    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        owner=User.objects.get(pk=venue.owner)
        lines.append(
            f'{venue}\n{venue.address}\n{venue.pin_code}\n{venue.phone}\n{venue.web}\n{venue.email}\n{owner}\n{owner.email}\n\n\n\n\n\n')
    response.writelines(lines)
    return response


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.manager == request.user:
        event.delete()
        messages.success(request, ('Event Deleted!!'))
        return redirect('list-events')
    else:
        messages.success(
            request, ("You're not authorized to delete that event!!"))
        return redirect('list-events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if request.user.is_authenticated and request.user.id==venue.owner:
        venue.delete()
    else:
        messages.success(request,"You're not authorized to delete that event!!")
    return redirect('list-venues')


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {'event': event, 'form': form})


def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                if request.POST['invite']:
                    id_list = request.POST.getlist('attendees')
                    for a in id_list:
                        print(User.objects.get(pk=a).email)             #send invite emails from here
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just going to the page, Not Submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            if request.POST.get('invite'):
                print("it worked, invited")
            submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,
                     request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html', {})


def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched, 'events': events})
    else:
        return render(request, 'events/search_events.html', {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner
    })


def list_venues(request):
    p = Paginator(Venue.objects.all().order_by('name'), 8)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a'*venues.paginator.num_pages
    return render(request, 'events/venue.html', {
        'venues': venues,
        'nums': nums
    })


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def all_events(request):
    p = Paginator(Event.objects.filter(approved=True).order_by('-event_date'), 8)
    page = request.GET.get('page')
    event_list = p.get_page(page)
    nums = 'a'*event_list.paginator.num_pages
    return render(request, 'events/event_list.html', {
        'event_list': event_list,
        'nums':nums
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    if request.user.is_authenticated:
        name = User.objects.get(pk=request.user.id).first_name
    else:
        name = 'Guest User'
    month = month.capitalize()
    month_number = int(list(calendar.month_name).index(month))

    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year
    time = now.strftime('%I:%M %p')

    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number
    ).order_by('event_date')
    return render(request, 'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        "event_list": event_list,
    })