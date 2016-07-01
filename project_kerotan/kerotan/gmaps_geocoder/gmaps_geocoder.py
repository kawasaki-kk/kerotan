import googlemaps
import sys, os
import pprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../API')
from APIkey_load_yaml import load_API_KEY

def __result_filtering(geocode_result):
	#formatted_adress='Japan'なら、不正な住所入力などでアドレスが取れてない。
	#エラーを返す。
	if geocode_result[0]["formatted_address"] == 'Japan':
		return "get_geocode ERROR."
	else:
		#緯度と経度の情報だけ返す。
		#結果は複数返ってきてるが、一番目の結果だけreturn.	
		return {"formatted_address":geocode_result[0]["formatted_address"], "location":geocode_result[0]["geometry"]["location"]}
	# latitude 	= geocode_result["geometry"]["location"]["lat"]
	# longitude 	= geocode_result["geometry"]["location"]["lng"]


def get_geocode(adress="〒160-0023 東京都新宿区 西新宿８丁目１７−１"):
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


if __name__ == '__main__':
	pprint.pprint( get_geocode("abc") )