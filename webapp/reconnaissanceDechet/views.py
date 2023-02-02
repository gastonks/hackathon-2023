from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import DechetForm
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