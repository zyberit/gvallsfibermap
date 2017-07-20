# -*- coding: utf-8 -*-

'''
Created on 7 apr. 2017

@author: perhk
'''

import json, csv

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

gcash = {}
def fill_gcash():
    reader = csv.DictReader(open(BASE_DIR+"/geocodecash.csv"))
    for row in reader:
        gcash[row['Adress']] = [row['Lat'],row['Lon']]

def get_gcode(adress):
    if adress in gcash:
        return gcash[adress][0],gcash[adress][1]
    else:
        return 0,0

mcash = []
def fill_mcash():
    avdelningar = {"Sagodjuren":"Spårare","Husdjuren":"Spårare","Gosedjuren":"Spårare","Nya spårare att fördela":"Spårare","Fabeldjuren":"Upptäckare","Skogsdjuren":"Upptäckare","Urdjuren":"Äventyrare","Rovdjuren":"Äventyrare","Slow Fox":"Utmanare","Rover":"Rover","Övriga ledare":"Ledare"}
    if len(gcash) == 0:
        fill_gcash()
    reader = csv.DictReader(open(BASE_DIR+"/medlemslista.csv"))
    for row in reader:
        avd = row['Avdelning']
        if avd in avdelningar: 
            namn = row['Förnamn']+" "+row['Efternamn']
            if row['Födselsdatum'][0:4] < "1992":
                grupp = "Ledare"
            else:
                grupp = avdelningar[avd]
            adr = row['Adress']+", "+row['Postnr']+" "+row['Postort']+", "+row['Land']
            lat,lon = get_gcode(adr)
            mcash.append({"namn":namn,"grupp":grupp,"avdelning":avd,"position":(lat,lon)})

def index(request):
    if len(mcash) == 0:
        fill_mcash()
    return render(request, 'index.html')

def karta(request):
    if 'grupp' in request.GET:
        avd=request.GET['grupp']
    else:
        avd = ""

    return render(request, 'karta.html', {"grupp":avd})


def places(request):
    grupp=request.GET['grupp']
    lat1=request.GET['lat1']
    lon1=request.GET['lon1']
    lat2=request.GET['lat2']
    lon2=request.GET['lon2']
    ret = []
    for m in mcash:
        if grupp == m['grupp']:
            lat,lon = m['position']
            if lat < lat1 and lat >lat2 and lon < lon1 and lon > lon2:
                ret.append({"namn":m['namn'],"avdelning":m['avdelning'],"position":[lat,lon]})
    return HttpResponse(json.dumps(ret), content_type='application/json')
