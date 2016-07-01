# APIkey_load_yaml.py

import yaml
import pprint
import sys,os
# os.path.dirname(os.path.abspath(__file__))

def load_API_KEY():
	f = open(os.path.dirname(os.path.abspath(__file__))+u"/../../API/API_KEY.yaml","r")
	data = yaml.load(f)
	f.close()
	# pprint.pprint(data)
	return data