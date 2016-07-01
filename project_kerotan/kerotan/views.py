import os, sys

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from kerotan.forms import AdressForm

from .gmaps_geocoder.gmaps_geocoder import get_geocode


def display_google_map(request):
	if request.method == 'POST':
		# form = ReportSearchForm()
		form = AdressForm(request.POST)
		# reports = Report.objects.all()
		if form.is_valid():
			print(form.cleaned_data["adress"])
			#Get route infomation by Ekitan API.
			location = get_geocode( form.cleaned_data["adress"] )
			if location == "get_geocode ERROR.":
				sys.exit()
			else:
				return render_to_response('kerotan/test_Gmap.html', {'form':form, 'latitude':location["location"]["lat"], 'longitude':location["location"]["lng"]}, RequestContext(request))
		else:
			return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))

	#作成したgoogle map?を表示

	else:
		form = AdressForm()
		return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
		# return renderrender(RequestContext(request), 'kerotan/test_Gmap.html')

