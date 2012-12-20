from datetime import date, datetime, time, timedelta
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from lunch.eat import models

def home(request):
    c = {}
    c["meal"] = models.Meal.current()
    if c["meal"]:
        c["who"] = request.session.get('who', '')
        c["preferred_for_place"] = request.session.get('favourite_' + str(c["meal"].place.id), None)
    c.update(csrf(request))
    return render_to_response("eat/index.html", c, context_instance=RequestContext(request))

def manage(request):
    c = {}
    c["meal"] = models.Meal.most_recent()
    c["places"] = models.Place.objects.all().order_by("name")
    c.update(csrf(request))
    return render_to_response("eat/manage.html", c, context_instance=RequestContext(request))

def new_meal(request):
    if models.Meal.current():
        raise "Already got a meal on the go" # FIXME

    where = None
    if request.POST["where"] == "new":
        p = models.Place(name = request.POST["new_where_name"], url = request.POST["new_where_url"], logo = request.POST["new_where_logo"])
        p.save()
        where = p.id
    else:
        where = int(request.POST["where"])
    pass

    # Find next instance of closing time
    timeparts = [int(i) for i in request.POST["closing_time"].split(":")]
    c = datetime.combine(date.today(), time(*timeparts))
    if c < datetime.now():
        c = c + timedelta(days=1)

    m = models.Meal(place=models.Place.objects.get(pk=where), closing_at=c)
    m.save()

    return HttpResponseRedirect("/")

def delete_choice(request):
    if not models.Meal.current():
        raise "Sorry, too late" # FIXME

    c = models.Choice.objects.get(pk=int(request.GET["choice_id"]))
    c.deleted = True
    c.save()

    return HttpResponseRedirect("/")

def add_choice(request):
    m = models.Meal.current()
    if not m:
        raise "Sorry, too late" # FIXME

    if request.POST["choice_option"] == "new":
        o = models.Option(place=m.place, name=request.POST["choice_option_new"])
	try:
            o.save()
	except IntegrityError:
            # Concurrently saved by someone else?
            o = models.Option.objects.get(name=request.POST["choice_option_new"], place=m.place)
            if o is None:
                raise
    else:
        o = models.Option.objects.get(pk=int(request.POST["choice_option"]))

    c = models.Choice(option=o, who=request.POST["choice_name"], meal=m, customisation=request.POST["choice_customisation"])
    c.save()

    request.session['who'] = c.who
    request.session['favourite_' + str(m.place.id)] = o.id

    return HttpResponseRedirect("/")
