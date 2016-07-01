from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from kerotan.forms import AdressForm



def display_google_map(request):
	if request.method == 'POST':
		# form = ReportSearchForm()
		form = AdressForm(request.POST)
		# reports = Report.objects.all()
		if form.is_valid():
			print(form.cleaned_data["adress"])
			#Get route infomation by Ekitan API.


			return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
		else:
			return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))

	#作成したgoogle map?を表示

	else:
		form = AdressForm()
		#return HttpResponse('google map')
		return render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
		# return renderrender(RequestContext(request), 'kerotan/test_Gmap.html')

