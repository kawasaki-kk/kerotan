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
			"幕張メッセ":"〒261-0023 千葉市美浜区中瀬2-1",
			"新宿駅":"〒160-0023 東京都新宿区西新宿１丁目１−３",
			"東京駅":"〒100-0005 東京都千代田区丸の内1 丁目 呑んき１丸の内北口店 9",
			"大阪駅":"大阪府大阪市北区梅田３丁目１−１"}
		company_overview={
			"TIS":"TIS株式会社（初代）は、1971年（昭和46年）4月、三和銀行および三和グループを中心に大阪市東区（現在の大阪市中央区）に\
株式会社東洋情報システム（資本金6億円）として設立された。現在の法人は、2016年（平成28年）7月にITホールディングス株式会社がTIS株式会社（初代）を\
吸収合併し、商号変更したものである。三和グループに属する企業で構成されるみどり会の会員企業でもある。\
JCBを中心としたクレジットカード会社の基幹システムなどに強みを持ち、国内シェアは5割弱で首位。",
			"幕張メッセ":"幕張メッセのメッセとは、ドイツ語の'見本市'の意味を指す'Messe'に由来する。1989年（平成元年）10月9日に開業した。\
現在は、東京国際展示場（東京ビッグサイト、東西合計）に次ぐ国内2番目の規模となっている。運営会社は、1986年（昭和61年）4月30日に設立され、\
2005年（平成17年）7月1日に社名を株式会社日本コンベンションセンター（Nippon Convention Center）から株式会社幕張メッセに変更した。\
当館の整備費は増設分を合わせると約558億円を投じており、年間の維持管理費が約20億円掛かるとされており、千葉県と千葉市の公費による一部負担が続いている。\
しかし、都心から近い東京国際展示場開業の影響を受け、2011年（平成23年）に東京モーターショーが東京ビッグサイトへ移るなど利用は伸び悩み、\
2013年（平成23年）度の稼働率は約40%となり、横浜市のパシフィコ横浜の稼働率の約70%を大きく下回っている。",
			"新宿駅":"東京の副都心・新宿に位置するターミナル駅である。1885年（明治18年）に日本鉄道により現在の山手線が開業したのが当駅の始まりである。\
4年後の1889年（明治22年）には南豊島郡淀橋町となる。開業時から新宿を副都心にする計画が発表されるまでは当駅周辺はまだ街の外れであり利用客は少ないものだったが、\
大正期に入り次第に市街地が拡大するにつれ、多くの私鉄が乗り入れるようになる。ターミナルとなって周辺が発展するにつれて利用客は増え続け、1931年には私鉄や国鉄などを合わせた\
利用者数で日本一になった[1]。そして、1966年（昭和41年）の乗車人数では、国鉄池袋駅の41万67人を抜いて、当駅が41万69人と日本一になっている。\
さらに1960年代から当駅西側一帯で進められた新宿副都心計画によって、70年代には多くの超高層ビルが建てられ利用者の増加に拍車がかかった。\
現在ではJR・私鉄・地下鉄の多くの路線が周辺地域のベッドタウンとを結んでおり、多くのビジネス客が利用する。さらに、当駅周辺は日本最大の繁華街・歓楽街となっており、\
昼夜を問わず人の流れが絶えない。JRの駅を中心に東・西・南口、周辺の各地下鉄駅、商業施設などが通路や地下街などで広範囲に連絡している。\
一日平均乗降者数は約335万人（2013年）[3]と世界一（ギネス世界記録認定）多い駅であり、地下道などで接続する西武新宿駅まで含めると約358万人（2013年）となり、\
この数字は横浜市の人口に匹敵する。年間の乗降客数に直すと約13億人となりインドの人口をも上回る規模となる。",
			"東京駅":"東京の表玄関とも言うべきターミナル駅で、特に東海道新幹線と東北新幹線の起点となっており、全国の新幹線網における最大の拠点となっている。\
また、東海道本線や東北本線など主要幹線の起点駅でもある。当駅から乗り換えなしで実に33都道府県[1]と結んでおり、1日当たりの列車発着本数は約3000本という日本を代表する\
ターミナル駅の一つである。プラットホームの数は日本一多く、在来線が地上5面10線と地下4面8線の合計9面18線、新幹線が地上5面10線、地下鉄は地下1面2線を有しており、\
面積は東京ドーム約3.6個分に相当する。赤レンガ造りの丸の内口駅舎は辰野金吾らが設計したもので、1914年に竣工、2003年に国の重要文化財に指定されている。\
「関東の駅百選」認定駅でもある。",
			"大阪駅":"大阪府の代表駅（府庁所在地駅）として第1回近畿の駅百選にも選定されている西日本最大の駅。駅長が配置された直営駅であり、\
管理駅として東海道本線の塚本駅を管轄している。JRの特定都区市内制度における「大阪市内」に属する駅であり、運賃計算の中心駅となる。また、アーバンネットワークの運行の要衝となる駅で、\
運行系統の軸をなしている。大阪市街の北玄関である梅田に位置し、駅前や駅の東側・南側を中心に繁華街が広がっている。\
東京・山陽・九州方面への長距離列車については、1964年開業の新大阪駅を発着する東海道・山陽新幹線に地位を譲ったものの、当駅は現在でも北陸方面との特急の始発・終着駅であり、\
新快速を始めとする京阪神の都市間連絡列車や、北近畿・山陰方面との特急、東京駅発着の寝台特急などの在来線特急も発着している。\
かつては東北・北海道方面に向かう夜行列車も発着していたが、2015年3月のダイヤ改正で寝台特急トワイライトエクスプレスが廃止されたことで東北・北海道方面を行き来する夜行列車は全て消滅した。\
これによって大阪駅を起点、終点とする夜行列車は全て消滅した。ただし、トワイライトエクスプレスは同年5月16日(土)に山陽方面のツアー列車として復活した。\
貨物列車は北方貨物線および梅田貨物線（いずれも通称）を利用するため大阪駅を通過しない。"}



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
				news = bing.web_search(query, 5, keys)
				print("news", json.dumps(news, indent=2) )
			
			except:
				print("I'm in except")
				# Get geocode by Google Maps API.
				# そのまま住所からgeocodeを取得
				geocode = {}
				geocode.update({ "start" : get_geocode( form.cleaned_data["start_address"] )["location"] })
				geocode.update({ "arriv" : get_geocode( form.cleaned_data["arriv_address"] )["location"] })
				print("geocode",geocode)

			#この辺の処理は適当。後でコード整理する。
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

