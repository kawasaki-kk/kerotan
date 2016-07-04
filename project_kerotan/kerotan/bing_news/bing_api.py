# -*- coding: utf-8 -*-

import urllib
import requests
import json
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../API/')
from APIkey_load_yaml import load_API_KEY

class Bing(object):

    # コンストラクタ（初期化）
    def __init__(self, key):
        # APIアクセスキー
        self.api_key = key

    # web検索
    def web_search(self, query, k, keys=["Url"], skip=0):
        """
            keysには'ID','Title','Description','DisplayUrl','Url'が入りうる
        """
        # 基本になるURL
        # url = 'https://api.datamarket.azure.com/Bing/Search/Web?'
        url = 'https://api.datamarket.azure.com/Bing/Search/News?'
        # 一回で返ってくる最大数
        max_num = 50
        # 各種パラメータ
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'"
        }

        # フォーマットはjsonで受け取る
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        # print("request_url",request_url)
        # -> request_url https://api.datamarket.azure.com/Bing/Search/News?Query=%27TIS%27&Market=%27ja-JP%27&$format=json
        
        # 結果を格納する配列
        results = []

        # 最大数でAPIを叩く繰り返す回数
        repeat = k / max_num
        repeat=int(repeat)
        # 残り
        remainder = k % max_num

        # 最大数でAPIを叩くのを繰り返す    
        for i in range(repeat):
            result = self._search(request_url, max_num, skip, keys)
            results.extend(result)
            skip += max_num

        # 残り
        if remainder:
            result = self._search(request_url, remainder, skip, keys)
            results.extend(result)

        # 結果を返す
        return results

    # 関連クエリ
    def related_search(self, query, keys=["Title"]):
        """
            keysには'ID','Title','BaseUrl'が入りうる
        """
        # 基本になるURL
        url = 'https://api.datamarket.azure.com/Bing/Search/RelatedSearch?'
        # 各種パラメータ
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'"
        }

        # フォーマットはjsonで受け取る
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"

        results = self._search(request_url, 50, 0, keys)

        return results

    # APIを叩く
    def _search(self, request_url, top, skip, keys):
        # APIを叩くための最終的なURL
        final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)
        # レスポンス（json化）
        response = requests.get(final_url, 
                                auth=(self.api_key, self.api_key), 
                                headers={'User-Agent': 'My API Robot'})
        
        response = response.json()

        # 結果を格納する配列
        results = []
        # 返ってきたもののうち指定された情報を取得する
        for item in response["d"]["results"]:
            result = {}
            for key in keys:
                # result[key] = item[key].encode("utf-8")
                result[key] = item[key]
            results.append(result)

        # 結果を返す
        return results
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
    key = load_API_KEY()["name"=="Bing search API"]["key"]
    q = "TIS"
    bing = Bing(key)

    keys=["Title", "Url", "Source", "Description", "Date"]
    # keys=["Title", "Url", "Source", "Date"]
    results = bing.web_search(q, 100, keys)
    print( json.dumps(results, indent=2) )

    # print("------------------------------------------------")
    # keys=["Title", "BingUrl", "ID"]
    # results = bing.related_search(q, keys)
    # print(json.dumps(results, indent=2) )

