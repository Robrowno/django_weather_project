from django.shortcuts import render


def home(request):
    """Render home.html template"""
    context = {}
    return render(request, 'weatherApp/home.html', context)


