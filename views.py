from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import DechetForm
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

    matter = "metal"#IA 
    context['matter'] = matter

    #JSON
    with open("reconnaissanceDechet/json/trash.json", 'r', encoding='utf-8') as f:
        dataTrash = json.load(f)
    with open("reconnaissanceDechet/json/fact"+matter+".json", 'r', encoding='utf-8') as f:
        dataFact = json.load(f)

    context["trash"] = dataTrash[matter]
    context["fact"] = dataFact[str(random.randint(0,4))]

    return render(request, "resultatReconnaissanceDechet/resultatReconnaissanceDechet.html", context)
