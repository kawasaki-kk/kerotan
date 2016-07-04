import os, sys

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from kerotan.forms import AddressForm

from .ekitan.ekitan_api import Ekitan
from .gmaps_geocoder.gmaps_geocoder import get_geocode
from .bing_news.bing_api import Bing
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../API')
from APIkey_load_yaml import load_API_KEY

from pprint import pprint
import json

# from prettyprint import pp

def display_google_map(request):
	if request.method == 'POST':
		form = AddressForm(request.POST)
		company_address={
			"TIS":"東京都新宿区 西新宿８丁目１７−１",
			"新宿駅":"〒160-0023 東京都新宿区西新宿１丁目１−３",
			"東京駅":"〒100-0005 東京都千代田区丸の内1 丁目 呑んき１丸の内北口店 9",
			"大阪駅":"大阪府大阪市北区梅田３丁目１−１"}
		company_overview={
			"TIS":"TIS株式会社（初代）は、1971年（昭和46年）4月、三和銀行および三和グループを中心に大阪市東区（現在の大阪市中央区）に株式会社東洋情報システム（資本金6億円）として設立された。現在の法人は、2016年（平成28年）7月にITホールディングス株式会社がTIS株式会社（初代）を吸収合併し、商号変更したものである。\
三和グループに属する企業で構成されるみどり会の会員企業でもある[1]。\
JCBを中心としたクレジットカード会社の基幹システムなどに強みを持ち、国内シェアは5割弱で首位。",
			"新宿駅":"〒160-0023 東京都新宿区西新宿１丁目１−３",
			"東京駅":"〒100-0005 東京都千代田区丸の内1 丁目 呑んき１丸の内北口店 9",
			"大阪駅":"大阪府大阪市北区梅田３丁目１−１"}



		if form.is_valid():
			#Get address from 会社名 by Dictionary.
			try:
			# if 1:
				print("I'm in try")
				print("start_address",company_address[form.cleaned_data["start_address"]])
				print("arriv_address",company_address[form.cleaned_data["arriv_address"]])
				#Get geocode by Google Maps API.
				#会社名を辞書を使って住所に変換、住所からgeocodeを取得
				geocode = {}
				geocode.update({ "start" : get_geocode( company_address[form.cleaned_data["start_address"]] )["location"] })
				geocode.update({ "arriv" : get_geocode( company_address[form.cleaned_data["arriv_address"]] )["location"] })
				print("geocode finished.")

				#到着住所が会社名ならば、概要を取得
				overview = company_overview[ form.cleaned_data["arriv_address"] ]
				print("overview", overview)

				#到着住所が会社名ならば、ニュースを取得
				bing = Bing( load_API_KEY("Bing search API") )
				keys = ["Title", "Url", "Source", "Description", "Date"]
				query = form.cleaned_data["arriv_address"]
				news = bing.web_search(query, 10, keys)
				print("news", json.dumps(news, indent=2) )
			except:
				print("I'm in except")
				# Get geocode by Google Maps API.
				# そのまま住所からgeocodeを取得
				geocode = {}
				geocode.update({ "start" : get_geocode( form.cleaned_data["start_address"] )["location"] })
				geocode.update({ "arriv" : get_geocode( form.cleaned_data["arriv_address"] )["location"] })
				print("geocode",geocode)

			#エラーメッセージ送るだけで、エラー処理はやってない。。。
			if "get_geocode ERROR." in geocode.values():
				print("get_geocode ERROR.")
				ErrorMassege="住所を正しい住所を入力してください。"
				return render_to_response('kerotan/test_Gmap.html', {'form':form, 'ErrorMassage':ErrorMassege }, RequestContext(request))			
			
			#Get route infomation by Ekitan API.
			#エラー処理はやってない
			ekitan = Ekitan( load_API_KEY("Ekitan API") )
			_, results_filtered = ekitan.norikae_search( s_ido=geocode["start"]["lat"], s_keido=geocode["start"]["lng"], t_ido=geocode["arriv"]["lat"], t_keido=geocode["arriv"]["lng"],  )
			# print("results_filtered",results_filtered)

			return render_to_response('kerotan/test_Gmap.html', {
						'form':form, 'route':results_filtered, \
						'start_latitude':geocode["start"]["lat"], 'start_longitude':geocode["start"]["lng"],
						'arriv_latitude':geocode["arriv"]["lat"], 'arriv_longitude':geocode["arriv"]["lng"],
						'news':news, 'overview':overview
						}, RequestContext(request))
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

