# -*- coding: utf-8 -*-

import urllib
import requests
import json
import sys,os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../API')
from APIkey_load_yaml import load_API_KEY

class Ekitan(object):

    # コンストラクタ（初期化）
    def __init__(self, key):
        # APIアクセスキー
        self.api_key = key

    # web検索
    def norikae_search(self, s_ido=35.696031, s_keido=139.690522, t_ido=35.681298, t_keido=139.766246, keys=["Url"]):
        """
            keysには'ID','Title','Description','DisplayUrl','Url'が入りうる
        """
        # 基本になるURL
        url = 'http://go.ekitan.com/asp-servlet/TrialAPI?'

        # 各種パラメータ
        # params = {
        #     "Query": "'{0}'".format(query),
        #     "Market": "'ja-JP'"
        # }
        V="100"
        FC="Norikae"
        LKEY=self.api_key           #!API key
        DT="-1"                       #!date,半角数字8ケタ or -1当日
        # DW=-1                       #曜日、0平日、1土曜、2日曜、-1当日
        #!time
        # TM="0000"                     #!time
        now = datetime.now()
        TM=now.strftime('%H')+now.strftime('%M')  
        RP="0"                        #!優先指定,0時刻、1料金、2乗換回数
        PN="3"                        #!出力候補数、3,5,10,20
        SR="0"                        #!発着指定, TMで指定した時間に出発するのか、到着するのかだと思う
        EP="0"                        #!有料特急有無,0:なし,1:あり
        CHAR="1"                      #!文字コード、0euc-jp, 1Shift_jis
        AN="-1"                     #エリア番号。とりあえず-1でおｋ
        NF="0"                        #省略の有無、0正式名所、1略称
        # OF="0"                        #0XML or 1JSON
        OF="1"                        #0XML or 1JSON
        # AIR=0                     #航空会社優先指定、0なし、1JAL、2ANA、3SKY/ADO
        SF="10900"                    #発駅コード、地点指定の場合は10900
        ST="10901"                    #着駅コード、地点指定の場合は10901
        LATF=str(s_ido)                    #!発地点緯度、SPEC パラメータで指定した書式で記述する。
        LNGF=str(s_keido)                  #!発地点経度
        LATT=str(t_ido)                    #!着地点緯度
        LNGT=str(t_keido)                  #!着地点経度
        # MVF=                        #発地点から駅までの移動速度（m/min）,1~9000,たぶんデフォルト60
        # MVT=                        #駅から着地点までの移動速度
        # SRG=                        #探索範囲,指定地点からの駅の探索範囲（m）, デフォルト5000
        # COORD=                      #測地系指定。0 またはTKY:日本測地系、でふぉで０．１またはJGD(*6) :JGD2000(ITRF94)
        SPEC="DEGREE"                 #緯度経度書式。PART：度分秒（デフォ）、DEGREE：度小数点、SECOND：秒小数点、CSEC：1/100 秒
        # FSN=                        #探索駅数。緯度経度地点の周辺駅とみなす駅数 1~10 の間で指定。デフォ10

        # フォーマットはjsonで受け取る
        # request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        request_url = url + "V="+V + "&FC="+FC + "&LKEY="+LKEY \
                            + "&DT="+DT + "&TM="+TM + "&SR="+SR + "&EP="+EP \
                            + "&RP="+RP + "&PN="+PN + "&AN="+AN + "&NF="+NF \
                            + "&CHAR="+CHAR \
                            + "&SPEC="+SPEC \
                            + "&OF="+OF \
                            + "&SF="+SF + "&ST="+ST \
                            + "&LATF="+LATF + "&LNGF="+LNGF \
                            + "&LATT="+LATT + "&LNGT="+LNGT
                            # + "&MVF=発地点から駅への移動速度" + "&MVT=駅から着地点への移動速度"\
                            # + "&SRG=探索範囲" \

        # print("request_url",request_url)

        # 結果を格納する配列
        # results = []

        # 最大数でAPIを叩く繰り返す回数
        # repeat = k / max_num
        # repeat=int(repeat)
        # # 残り
        # remainder = k % max_num

        # 最大数でAPIを叩くのを繰り返す    
        # for i in range(repeat):
        #     result = self._search(request_url, keys)
        #     results.extend(result)

        # 残り
        # if remainder:
        #     result = self._search(request_url, remainder, skip, keys)
        #     results.extend(result)

        results = self._search(request_url, keys)
        # print(results)
        # 結果を返す
        return results



    # APIを叩く
    def _search(self, request_url, keys):
        # APIを叩くための最終的なURL
        # final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)
        # レスポンス（json化）
        # response = requests.get(requests_url, 
        #                         auth=(self.api_key, self.api_key), 
        #                         headers={'User-Agent': 'My API Robot'})
        response = requests.get(request_url)
        response = response.json()
        response_filtered = self.__response_filter(response)

        # 結果を格納する配列
        # results = []
        # 返ってきたもののうち指定された情報を取得する
        # for item in response["d"]["results"]:
        #     result = {}
        #     for key in keys:
        #         # result[key] = item[key].encode("utf-8")
        #         result[key] = item[key]
        #     results.append(result)

        # 結果を返す
        return (response, response_filtered)

    def __response_filter(self, response):
        #------------------------------------------------------------------------------------------------------------------------------------------
        condition={}

        pointFrom_latitude  =response["trainDoc"]["condition"]["pointFrom"]["coordinate"]["latitude"]["~T"]
        pointFrom_longitude =response["trainDoc"]["condition"]["pointFrom"]["coordinate"]["longitude"]["~T"]
        pointFrom={"pointFrom":{"latitude":pointFrom_latitude, "longitude":pointFrom_longitude}}

        pointTo_latitude    =response["trainDoc"]["condition"]["pointTo"]["coordinate"]["latitude"]["~T"]
        pointTo_longitude   =response["trainDoc"]["condition"]["pointTo"]["coordinate"]["longitude"]["~T"]
        pointTo={"pointTo":{"latitude":pointTo_latitude, "longitude":pointTo_longitude}}

        condition_time_hour =response["trainDoc"]["condition"]["time"]["hour"]["~T"]
        condition_time_min  =response["trainDoc"]["condition"]["time"]["min"]["~T"]
        time={"time":{"hour":condition_time_hour, "min":condition_time_min}}

        condition.update(pointFrom)
        condition.update(pointTo)
        condition.update(time)

        #------------------------------------------------------------------------------------------------------------------------------------------
        line=[]
        for lineInfo in response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"]:
            stationFrom_stationName =lineInfo["stationFrom"]["stationName"]["~T"]
            stationFrom_latitude    =lineInfo["stationFrom"]["coordinate"]["latitude"]["~T"]
            stationFrom_longitude   =lineInfo["stationFrom"]["coordinate"]["longitude"]["~T"]
            stationFrom_time_hour   =lineInfo["stationFrom"]["time"]["hour"]["~T"]
            stationFrom_time_min    =lineInfo["stationFrom"]["time"]["min"]["~T"]
            stationFrom_time={"hour":stationFrom_time_hour, "min":stationFrom_time_min}
            stationFrom = {"stationFrom":{"stationName":stationFrom_stationName, "latitude":stationFrom_latitude, "longitude":stationFrom_longitude, "time":stationFrom_time}}

            stationTo_stationName   =lineInfo["stationTo"]["stationName"]["~T"]
            stationTo_latitude      =lineInfo["stationTo"]["coordinate"]["latitude"]["~T"]
            stationTo_longitude     =lineInfo["stationTo"]["coordinate"]["longitude"]["~T"]
            stationTo_time_hour     =lineInfo["stationTo"]["time"]["hour"]["~T"]
            stationTo_time_min      =lineInfo["stationTo"]["time"]["min"]["~T"]
            stationTo_time={"hour":stationTo_time_hour, "min":stationTo_time_min}
            stationTo = {"stationTo":{"stationName":stationTo_stationName, "latitude":stationTo_latitude, "longitude":stationTo_longitude, "time":stationTo_time } }
            # stationTo_toStationHomeTime =response["trainDoc"]["routeList"]["route"][0]["stationTo"]["toStationHomeTime"]["~T"]
            # stationTo = {"stationTo":{"stationName":stationTo_stationName, "latitude":stationTo_latitude, "longitude":stationTo_longitude, "time":stationTo_time, "toStationHomeTime":stationTo_toStationHomeTime } }

            lineName_tmp = lineInfo["lineName"]["~T"]
            lineName = {"lineName" : lineName_tmp}

            lineInfo_temp={}
            lineInfo_temp.update(stationFrom)
            lineInfo_temp.update(stationTo)
            lineInfo_temp.update(lineName)
            line.append(lineInfo_temp)

        fare            =response["trainDoc"]["routeList"]["route"][0]["fare"]["~T"]
        totalTime_hour  =response["trainDoc"]["routeList"]["route"][0]["time"]["hour"]["~T"]
        totalTime_min   =response["trainDoc"]["routeList"]["route"][0]["time"]["min"]["~T"]
        totalTime       ={"hour":totalTime_hour, "min":totalTime_min}

        #------------------------------------------------------------------------------------------------------------------------------------------
        route={"lineList":line, "fare":fare, "totalTime":totalTime}
        #------------------------------------------------------------------------------------------------------------------------------------------
        results={"condition":condition, "route":route}

        return results

        # line1={}

        # stationFrom_stationName =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationFrom"]["stationName"]["~T"]
        # stationFrom_latitude    =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationFrom"]["coordinate"]["latitude"]["~T"]
        # stationFrom_longitude   =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationFrom"]["coordinate"]["longitude"]["~T"]
        # stationFrom_time_hour   =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationFrom"]["time"]["hour"]
        # stationFrom_time_min    =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationFrom"]["time"]["min"]
        # stationFrom_time={"time":{"hour":stationFrom_time_hour, "min":stationFrom_time_min}
        # stationFrom = {"stationFrom":{"stationName":stationFrom_stationName, "latitude":stationFrom_latitude, "longitude":stationFrom_longitude, "time":stationFrom_time}

        # stationTo_stationName   =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationTo"]["stationName"]["~T"]
        # stationTo_latitude      =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationTo"]["coordinate"]["latitude"]["~T"]
        # stationTo_longitude     =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationTo"]["coordinate"]["longitude"]["~T"]
        # stationTo_time_hour     =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationTo"]["time"]["hour"]
        # stationTo_time_min      =response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["stationTo"]["time"]["min"]
        # stationTo_time={"time":{"hour":stationTo_time_hour, "min":stationTo_time_min}
        # stationTo = {"stationTo":{"stationName":stationTo_stationName, "latitude":stationTo_latitude, "longitude":stationTo_longitude, "time":stationTo_time } }
        # # stationTo_toStationHomeTime =response["trainDoc"]["routeList"]["route"][0]["stationTo"]["toStationHomeTime"]["~T"]
        # # stationTo = {"stationTo":{"stationName":stationTo_stationName, "latitude":stationTo_latitude, "longitude":stationTo_longitude, "time":stationTo_time, "toStationHomeTime":stationTo_toStationHomeTime } }

        # lineName_tmp = response["trainDoc"]["routeList"]["route"][0]["lineList"]["line"][0]["lineName"]["~T"]
        # lineName = {"lineName" : lineName_tmp}

        # line1.update(stationFrom)
        # line1.update(stationTo)
        # line1.update(lineName)
        # #------------------------------------------------------------------------------------------------------------------------------------------
        # #------------------------------------------------------------------------------------------------------------------------------------------

        # fare          =response["trainDoc"]["routeList"]["fare"]["~T"]
        # totalTime_hour     =response["trainDoc"]["routeList"]["time"]["hour"]["~T"]
        # totalTime_min     =response["trainDoc"]["routeList"]["time"]["min"]["~T"]
        # totalTime     =aaaaa



#ゴミ
# def bytes2str_inResults(results, keys):
#     for i in range(len(results)):
#         for j in keys:
#             # print(isinstance(results[ i ][ j ], bytes))
#             if isinstance(results[ i ][ j ], bytes)=='True':
#                 results[ i ][ j ]=results[ i ][ j ].decode('utf-8')
#             if isinstance(results[ i ][ j ], bytes)=='True':
#                 results[ i ][ j ]=results[ i ][ j ].decode('utf-8')
#     return results

if __name__ == '__main__':
    #APIキーをロード
    # f = load_API_KEY()
    # key = f["name"=="Bing search API"]["key"]
    key = load_API_KEY("Ekitan API")
    # q = "TIS"
    ekitan = Ekitan(key)

    # keys=["Title", "Url", "Source", "Description", "Date"]
    # keys=["Title", "Url", "Source", "Date"]
    results, results_filtered = ekitan.norikae_search()
    # print(results)
    # print( json.dumps(results, indent=2) )
    
    try:
        with open("./ekitan_results/result_keiro.txt","w") as f:
            f.write(json.dumps(results, indent=2))
            print("finished.")
    except:
        print("APIkey_write_yaml ERROR.")
        sys.exit()

    try:
        with open("./ekitan_results/result_keiro_filtered.txt","w") as f:
            f.write(json.dumps(results_filtered, indent=2))
            print("finished.")
    except:
        print("APIkey_write_yaml ERROR.")
        sys.exit()


    # print("------------------------------------------------")
    # keys=["Title", "BingUrl", "ID"]
    # results = bing.related_search(q, keys)
    # print(json.dumps(results, indent=2) )

