from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import DechetForm, AjoutPointMapForm
from .predict import reconnaissance
import base64
from base64 import b64encode
import json
import random

def reconnaissanceDechet(request):
    if request.method == 'POST':
        form = DechetForm(request.POST, request.FILES)
        if form.is_valid():
            cleanedForm = form.cleaned_data.get('image')
            dataImage = cleanedForm.read()
            encoded = b64encode(dataImage).decode()

            return resultatReconnaissanceDechet(request, encoded)
        else:
            return HttpResponse('ERREUR')

    else:
        form = DechetForm()

    context = {}
    context['form'] = DechetForm()

    return render(request, "reconnaissanceDechet/reconnaissanceDechet.html", context)

def resultatReconnaissanceDechet(request, img):
    context = {}

    #Creation du jpeg/ conversion binaire
    decodeit = open('reconnaissanceDechet/img/trans.jpeg', 'wb')
    decodeit.write(base64.b64decode((img)))
    decodeit.close()

    reconnaissance("reconnaissanceDechet/img/trans.jpeg")

    #matter = "metal"#IA 
    list = {
        1 : {
            "matter": "plastic",
            "percent": 90
        },
        2 : {
            "matter": "metal",
            "percent": 87
        }
    }
    firstMatter = list[1]["matter"]
    context["matter"] = list[1]["matter"]

    texte = json.dumps(list)
    context["list"] = texte
  
    #JSON
    with open("reconnaissanceDechet/json/trash.json", 'r', encoding='utf-8') as f:
        dataTrash = json.load(f)
    with open("reconnaissanceDechet/json/fact"+firstMatter+".json", 'r', encoding='utf-8') as f:
        dataFact = json.load(f)

    context["trash"] = dataTrash[firstMatter]
    context["fact"] = dataFact[str(random.randint(0,4))]
    
    return render(request, "resultatReconnaissanceDechet/resultatReconnaissanceDechet.html", context)

def ajoutPointMap(request):
    if request.method == 'POST':
        form = AjoutPointMapForm(request.POST, request.FILES)
        testPost = request.POST
        if form.is_valid():
            cleanedForm = form.cleaned_data

            context = {}
            context["description"] = cleanedForm.get('description')
            context["latitude"] = str(cleanedForm.get('latitude'))
            context["longitude"] = str(cleanedForm.get('longitude'))

            return confirmationAjoutPointMap(request, context)
        else:
            return HttpResponse('ERREUR')
    else:
        form = AjoutPointMapForm()

    context = {}
    context['form'] = AjoutPointMapForm()

    return render(request, "ajoutPointMap/ajoutPointMap.html", context)

def confirmationAjoutPointMap(request, data):

    json_data = []

    with open('reconnaissanceDechet/json/marker.json') as json_file:
        json_data = json.load(json_file)

    json_data.append(data)

    with open('reconnaissanceDechet/json/marker.json', 'w') as outfile:
        outfile.write(json.dumps(json_data))

    context = {}
    return render(request, "confirmationAjoutPointMap/confirmationAjoutPointMap.html", context)

def map(request):
    context = {}
    return render(request, "map/map.html", context)