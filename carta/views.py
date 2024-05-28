from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import activate
from django.views.generic import TemplateView

def comensal(request):
    return render(request,'seleccionComensal.html')

def menu(request):
    return render(request,'tipoMenu.html')

def bodega(request):
    return render(request, 'bodega.html')

def buscar (request):
    return render(request, "busqueda.html") 


def menus (request):
    return render(request, "menus.html")

def cafe (request):
    return render(request, "cafeteria.html") 


