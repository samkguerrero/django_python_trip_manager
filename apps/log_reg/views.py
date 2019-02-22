from django.shortcuts import render, redirect
from .models import *
# from time import strftime, gmtime
# from dateutil import parser
from django.contrib import messages
import bcrypt

def index(request):
    if not 'failed_password' in request.session:
        request.session['failed_password'] = True
    if not 'attempted_email' in request.session:
        request.session['attempted_email'] = ""
    if 'logged_in_user_id' in request.session:
        return redirect("/dashboard")
    else:
        return render(request, "log_reg/index.html")

def show_trip(request, trip_id):
    try:
        trip_to_show = Trip.objects.get(id=trip_id)
        context = {
            "trip_id": trip_id,
            "trip_to_show": trip_to_show,
            "trip_attendees": trip_to_show.event_attendees.all()
        }
        if 'logged_in_user_id' in request.session:
            return render(request, "log_reg/show_trip.html", context)
    except:
        return redirect("/dashboard")

def new_trip(request):
    if 'logged_in_user_id' in request.session:
        return render(request, "log_reg/new_trip.html")
    else:
        return redirect("/")

def join_trip(request, trip_id):
        user_joining = User.objects.get(id=request.session['logged_in_user_id'])
        trip_bieng_joined = Trip.objects.get(id=trip_id)
        user_joining.eventes_attending.add(trip_bieng_joined)
        return redirect("/dashboard")

def cancel_trip(request, trip_id):
        user_joining = User.objects.get(id=request.session['logged_in_user_id'])
        trip_bieng_joined = Trip.objects.get(id=trip_id)
        user_joining.eventes_attending.remove(trip_bieng_joined)
        return redirect("/dashboard")

def edit_trip(request, trip_id):
    try:
        trip_to_edit = Trip.objects.get(id=trip_id)
        context = {
            "trip_id": trip_id,
            "trip_to_edit": trip_to_edit
        }
        if 'logged_in_user_id' in request.session:
            return render(request, "log_reg/edit_trip.html", context)
        else:
            return redirect("/")
    except:
        return redirect("/dashboard")

def process(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
            return redirect("/")
        else:
            new_user = User.objects.create(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                email = request.POST['email'],
                password = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt())
            )
            request.session['logged_in_user'] = request.POST['fname']
            request.session['logged_in_user_id'] = new_user.id
            request.session['log_reg'] = 'registered'
            return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect("/")

def login(request):
    if request.method == "POST":
        login_errors = User.objects.login_validator(request.POST)
        if len(login_errors):
            for tag, error in login_errors.items():
                messages.error(request, error, extra_tags=tag)
            return redirect("/")
        else:
            user_logged_in = User.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), user_logged_in.password.encode()):
                request.session['logged_in_user_fname'] = user_logged_in.first_name
                request.session['logged_in_user_id'] = user_logged_in.id
                request.session['failed_password'] = True                
                request.session['log_reg'] = 'logged in'
                return redirect("/dashboard")
            else:
                request.session['failed_password'] = False
                request.session['attempted_email'] = request.POST['email']
                return redirect("/")

def view_user(request, user_id):
    try:
        print("*"*100)
        print(User.objects.get(id=user_id))
        if User.objects.get(id=user_id):
            context = {
                "user_to_view": User.objects.get(id=user_id)
            }
            return render(request, "log_reg/users.html", context)
    except:
        return redirect("/")