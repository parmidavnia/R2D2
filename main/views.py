from django.shortcuts import redirect, render


def index(request):
    return render(request, 'main/main.html')


def scoring_detail(request):
    return render(request, 'main/scoring_detail.html')


def sentimental_detail(request):
    return render(request, 'main/sentimental_detail.html')
