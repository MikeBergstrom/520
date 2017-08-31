# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import googlemaps
from datetime import datetime
from .models import Trip
from ..login.models import User
# Create your views here.
gmaps = googlemaps.Client(key="AIzaSyCE5rc8HduPNe5ZN5B6yLPQYMPmZ1jYTcw")
gkey = "AIzaSyCE5rc8HduPNe5ZN5B6yLPQYMPmZ1jYTcw"

def index(request):
    # Trip.objects.all().delete()
    if not 'id' in request.session:
        request.session.id = 0
        return render(request, 'first/index.html')
    else:
        saved_routes = Trip.objects.filter(creator__id=request.session['id'])
        context = {'saved_routes':saved_routes}
        return render(request, 'first/index.html', context)

def process(request):
    if 'route_choice' in request.POST:
        curr_user = User.objects.get(id=request.session['id'])
        print curr_user.mpg
        route = Trip.objects.get(name=request.POST['route_choice'])
        start = route.origin
        end = route.destination
        mpg = int(curr_user.mpg)
        cost =int(curr_user.cost)
    else:
        start = request.POST['start']
        end = request.POST['end']
        mpg = int(request.POST['mpg'])
        cost = int(request.POST['cost'])

    request.session['start'] = start
    print request.session['start']
    request.session['end'] = end
    request.session['mpg'] = mpg
    request.session['cost'] = cost
    direction_results = gmaps.directions(start,end, mode="driving", departure_time="now", avoid="tolls")
    toll_direction_results = gmaps.directions(start,end, mode="driving", departure_time="now")
    summary =  direction_results[0]['summary']
    distance = direction_results[0]['legs'][0]['distance']['text']
    duration =  direction_results[0]['legs'][0]['duration_in_traffic']['text']
    tsummary =  toll_direction_results[0]['summary']
    tdistance = toll_direction_results[0]['legs'][0]['distance']['text']
    tduration =  toll_direction_results[0]['legs'][0]['duration_in_traffic']['text']
    distance_diff = round(((direction_results[0]['legs'][0]['distance']['value'] - toll_direction_results[0]['legs'][0]['distance']['value'])/1609.34),2)
    time_diff = (direction_results[0]['legs'][0]['duration_in_traffic']['value']-toll_direction_results[0]['legs'][0]['duration_in_traffic']['value'])/60
    gas_saving = round((distance_diff/mpg * 3),2)
    toll = get_toll()
    net_cost = (toll - gas_saving)
    min_per = cost/5
    actual_per = round(time_diff/net_cost, 2)
    status = "should"
    if actual_per < min_per:
        status = "should not"
    # print direction_results
    # print toll_direction_results
    toll_routes = []
    for item in toll_direction_results[0]['legs'][0]['steps']:
        if "toll" in item['html_instructions']:
            print item['html_instructions']
            print item['start_location']
            toll_lat = item['start_location']['lat']
            toll_lng = item['start_location']['lng']
            reverse = gmaps.reverse_geocode((toll_lat,toll_lng))
            toll_routes.append(reverse[0]['address_components'][0]['long_name'])
            print toll_routes, "routes"
    context = {'summary':summary,
            'distance':distance,
            'duration':duration,
            'tsummary':tsummary,
            'tdistance':tdistance,
            'tduration':tduration,
            'time_diff': time_diff,
            'distance_diff': distance_diff,
            'start':start,
            'end': end,
            'toll_routes':toll_routes,
            'gas_saving':gas_saving,
            'toll':toll,
            'net_cost':net_cost,
            'status':status,
            'min_per':min_per,
            'actual_per':actual_per,
            'gkey': gkey
            }
    # print toll_direction_results[0]['legs'][0]['steps']
    if 'save_route' in request.POST:
        print "is checked"
        Trip.objects.add(request.POST, request.session['id'])
    return render(request, 'first/results.html', context)

def get_toll():
    now = datetime.now()
    print now.hour, "nour"
    if now.hour < 5:
        return 1.25
    if now.hour < 6:
        return 2.00
    if now.hour < 7:
        return 3.40
    if now.hour < 9:
        return 4.30
    if now.hour < 10:
        return 3.40
    if now.hour < 14:
        return 2.70
    if now.hour < 15:
        return 3.40
    if now.hour < 18:
        return 4.30
    if now.hour < 19:
        return 3.40
    if now.hour < 21:
        return 2.00
    if now.hour < 23:
        return 2.00
    else:
        return 1.25     
