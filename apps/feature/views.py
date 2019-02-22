from django.shortcuts import render, redirect
from apps.feature.models import Item
from apps.log_reg.models import User, Trip
from django.contrib import messages


# Create your views here.
def index(request):
        if 'logged_in_user_id' in request.session:
                user_signed_in = User.objects.get(id=request.session['logged_in_user_id'])
                context = {
                        "all_my_trips": Trip.objects.filter(event_owner=user_signed_in),
                        "others_trips": Trip.objects.exclude(event_attendees=user_signed_in),
                        "trips_joined": user_signed_in.eventes_attending.all()
                }
                return render(request, "feature/index.html", context)
        else:
                return redirect("/")

def user_add_item(request):
        if request.method == "POST":
                errors = Trip.objects.basic_validator(request.POST)
                if len(errors):
                        for tag, error in errors.items():
                                messages.error(request, error, extra_tags=tag)
                        return redirect("/trips/new")
                else:        
                        print("*"*100)
                        print("ADD")
                        print(request.POST)
                        # user_adding_new_item = User.objects.get(id=int(request.POST['user_creating_trip_id']))
                        user_adding_new_item = User.objects.get(id=int(request.session['logged_in_user_id']))
                        # print(user_adding_new_item.first_name*100)
                        Trip.objects.create(
                                desti=request.POST['dest'],
                                start=request.POST['start'],
                                end=request.POST['end'],
                                plan=request.POST['plan'],
                                event_owner=user_adding_new_item,
                        )
                        return redirect("/dashboard")

def user_edit_item(request):
        if request.method == "POST":
                errors = Trip.objects.basic_validator(request.POST)
                if len(errors):
                        for tag, error in errors.items():
                                messages.error(request, error, extra_tags=tag)
                        return redirect("/trips/edit/" + request.POST['trip_id'])
                else:
                        print("*"*100)
                        print("EDIT")
                        print(request.POST)
                        trip_to_edit = Trip.objects.get(id=int(request.POST['trip_id']))
                        if trip_to_edit.event_owner.id == request.session['logged_in_user_id']:
                                trip_to_edit.desti = request.POST['dest']
                                trip_to_edit.start = request.POST['start']
                                trip_to_edit.end = request.POST['end']
                                trip_to_edit.plan = request.POST['plan']
                                trip_to_edit.save()
                        # return redirect("/dashboard")
                        return redirect("/")

def user_delete_item(request, trip_id):
        if 'logged_in_user_id' in request.session:
                print("*"*100)
                print("DELETE")
                print(trip_id)
                # print(request.POST)
                trip_to_delete = Trip.objects.get(id=trip_id)
                if trip_to_delete.event_owner.id == request.session['logged_in_user_id']:
                        trip_to_delete.delete()
                return redirect("/dashboard")
        else:
                return redirect("/")




