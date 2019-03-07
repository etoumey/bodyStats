import json


with open('userData', 'r') as fh:
	userData = json.load(fh)
	fh.close()