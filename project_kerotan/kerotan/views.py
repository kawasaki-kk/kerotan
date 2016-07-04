import os, sys

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from kerotan.forms import AddressForm

from .ekitan.ekitan_api import Ekitan
from .gmaps_geocoder.gmaps_geocoder import get_geocode
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../API')
from APIkey_load_yaml import load_API_KEY

from pprint import pprint
# from prettyprint import pp

def display_google_map(request):
	# AddressFormSet = formset_factory(AddressForm)
	if request.method == 'POST':
		# form = ReportSearchForm()
		# reports = Report.objects.all()
		form = AddressForm(request.POST)
		# formset = AddressFormSet(request.POST, request.POST)
		if form.is_valid():
		# if formset.is_valid():
			# for i in formset.cleaned_data:
			# 	print("formset.cleaned_data",i)
			# 	print("address:",i["address"])

			#Get geocode by Google Maps API.
			geocode = {}
			geocode.update({ "start" : get_geocode( form.cleaned_data["start_address"] )["location"] })
			geocode.update({ "arriv" : get_geocode( form.cleaned_data["arriv_address"] )["location"] })
			# print("geocode",geocode)
			if "get_geocode ERROR." in geocode.values():
				print("get_geocode ERROR.")
				sys.exit()
			
			else:
				#Get route infomation by Ekitan API.
				ekitan = Ekitan( load_API_KEY("Ekitan API") )
				_, results_filtered = ekitan.norikae_search( s_ido=geocode["start"]["lat"], s_keido=geocode["start"]["lng"], t_ido=geocode["arriv"]["lat"], t_keido=geocode["arriv"]["lng"],  )
				print("results_filtered",results_filtered)

				return render_to_response('kerotan/test_Gmap.html', \
					{'form':form, 'route':results_filtered,'start_latitude':geocode["start"]["lat"], 'start_longitude':geocode["start"]["lng"], 'arriv_latitude':geocode["arriv"]["lat"], 'arriv_longitude':geocode["arriv"]["lng"]}, RequestContext(request))
				# return render_to_response('kerotan/test_Gmap.html', {'formset':formset, 'latitude':location["location"]["lat"], 'longitude':location["location"]["lng"]}, RequestContext(request))
		else:
			return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
			# return render_to_response('kerotan/test_Gmap.html', {'formset':formset}, RequestContext(request))

	#作成したgoogle map?を表示

	else:
		form = AddressForm()
		# formset = AddressFormSet()
		return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
		# return render_to_response('kerotan/test_Gmap.html', {'formset':formset}, RequestContext(request))
		# return renderrender(RequestContext(request), 'kerotan/test_Gmap.html')

