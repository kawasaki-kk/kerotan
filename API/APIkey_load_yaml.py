# APIkey_load_yaml.py

import yaml
import pprint
import sys,os
# os.path.dirname(os.path.abspath(__file__))

def load_API_KEY(name):
	try:
		with open(os.path.dirname(os.path.abspath(__file__))+u"/../../API/API_KEY.yaml","r") as f:
			data = yaml.load(f)[name]["key"]
			# pprint.pprint(data)
			# f.close()
			return data
	except:
		print('load yaml error')
		raise