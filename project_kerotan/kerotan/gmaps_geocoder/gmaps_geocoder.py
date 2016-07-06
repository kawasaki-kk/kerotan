# -*- coding: utf-8 -*-
import googlemaps
import sys, os
import traceback

import pprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../API')
from APIkey_load_yaml import load_API_KEY

def __result_filtering(geocode_result):
	#formatted_adress='Japan'なら、不正な住所入力などでアドレスが取れてない。
	#エラーを返す。
	if geocode_result[0]["formatted_address"] == 'Japan':
		raise Exception("Error:get_geocode. Formatted_address was 'Japan', inputed adress can't identify geocode. ")
	else:
		#整形された住所と、latとlngが含まれたlocationを返す
		#結果は複数返ってきてるが、一番目の結果だけreturn.	
		return {"formatted_address":geocode_result[0]["formatted_address"], "location":geocode_result[0]["geometry"]["location"]}
	# latitude 	= geocode_result["geometry"]["location"]["lat"]
	# longitude 	= geocode_result["geometry"]["location"]["lng"]


def get_geocode(adress="〒160-0023 東京都新宿区 西新宿８丁目１７−１"):
	try:
		#API key load.
		key=load_API_KEY("Google Maps API")
		#auth
		gmaps=googlemaps.Client(key=key)

		#search condition
		componentRestrictions={"country":'JP'}

		#search
		geocode_result = gmaps.geocode(adress, componentRestrictions)

		# pprint.pprint( geocode_result )
		# pprint.pprint( geocode_result[0]["geometry"]["location"] )

		return __result_filtering( geocode_result )

	except Exception:
		raise
	except:
		raise



if __name__ == '__main__':
	pprint.pprint( get_geocode("tis") )