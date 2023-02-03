from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import DechetForm, AjoutPointMapForm
from base64 import b64encode

def reconnaissanceDechet(request):
    if request.method == 'POST':
        form = DechetForm(request.POST, request.FILES)
        if form.is_valid():
            cleanedForm = form.cleaned_data.get('image')
            dataImage = cleanedForm.read()
            encoded = b64encode(dataImage).decode()
            mime = 'image;'
            context = {"image": "data:%sbase64,%s" % (mime, encoded)}

            return resultatReconnaissanceDechet(request, context)
        else:
            return HttpResponse('ERREUR')

    else:
        form = DechetForm()

    context = {}
    context['form'] = DechetForm()

    return render(request, "reconnaissanceDechet/reconnaissanceDechet.html", context)

def resultatReconnaissanceDechet(request, img):
    context = img
    return render(request, "resultatReconnaissanceDechet/resultatReconnaissanceDechet.html", context)

def ajoutPointMap(request):
    if request.method == 'POST':
        form = AjoutPointMapForm(request.POST, request.FILES)
        testPost = request.POST
        if form.is_valid():
            cleanedForm = form.cleaned_data

            context = {}
            context["description"] = cleanedForm.get('description')
            context["latitude"] = cleanedForm.get('latitude')
            context["longitude"] = cleanedForm.get('longitude')

            return confirmationAjoutPointMap(request, context)
        else:
            return HttpResponse('ERREUR')
    else:
        form = AjoutPointMapForm()

    context = {}
    context['form'] = AjoutPointMapForm()

    return render(request, "ajoutPointMap/ajoutPointMap.html", context)

def confirmationAjoutPointMap(request, data):
    context = data
    return render(request, "confirmationAjoutPointMap/confirmationAjoutPointMap.html", context)
