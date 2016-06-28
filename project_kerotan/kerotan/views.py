from django.shortcuts import render
from django.http import HttpResponse


def display_google_map(request):
    #作成したgoogle map?を表示

    #return HttpResponse('google map')
    return render(request, 'kerotan/test_Gmap.html')

