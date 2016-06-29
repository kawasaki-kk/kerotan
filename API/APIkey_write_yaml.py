# APIkey_write_yaml.py

import yaml

# ↓コメントアウトを外す
# data=[]

# ↓次の形式でデータを保存
data.append({
	"name":u"Bing search API",
	"url":u"https://api.datamarket.azure.com/Bing/Search/Web?",
	"key":u"",
	})
# data.append({
# 	"name":u"ぐるなび都道府県マスタAPI",
# 	"url":u"http://api.gnavi.co.jp/master/PrefSearchAPI/20150630/",
# 	"key":u"aaaaaaaaaaaaaaaa",
# 	})

# dataをアペンド
f = open("API_KEY.yaml","a")
f.write(yaml.dump(data))

f.close()