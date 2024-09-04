from django.utils.translation import activate
from django.shortcuts import render, redirect

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            activate(language) # type: ignore
    return redirect(request.POST.get('next', '/'))