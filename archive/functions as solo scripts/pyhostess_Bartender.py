##pubdatapub - Countries#
##Working!!! 12/20#
#the result of line 330 is sitting on the desktop
#UI is crappy though
#also this :( https://www.python.org/dev/peps/pep-0279/
############################

import os
import lxml
from lxml import html
from lxml import etree
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests as rq
import io
from io import StringIO, BytesIO
import urllib2 as url
from urllib2 import urlopen

def bartender():
	os.chdir('C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub\\bin')
	execfile('jus_get_dics.py')
	os.chdir('C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub')
	C_Y_fp=open('C_Y_order.json','r')
	C_Y_order=C_Y_fp.read()
	C_Y=json.loads(C_Y_order)
	not_iso_order_countries=str(C_Y[0])
	not_iso_order_countries=not_iso_order_countries.split(',')
	global order_countries
	order_countries=[]
	for co in not_iso_order_countries:
		if co in iso_dic:
			order_countries.append(iso_dic[co])
		else:
			for iso in iso_dic:
				if co[:3] in iso_dic[iso]:
					order_countries.append(iso_dic[iso])
				else:
					pass
	global order_years
	order_years=str(C_Y[1])
	order_years=order_years.split(',')
	global wb_availibility_dic
	wb_availibility_dic={}
	global wb_checkiftheyhave_list
	wb_checkiftheyhave_list=[]
	global UNHDR_availibility_dic
	UNHDR_availibility_dic={}
	global un_checkiftheyhave_list
	un_checkiftheyhave_list=[]
	global errorlist
	errorlist=[]
	global mislist
	mislist=[]
	for wb_i in wb_indi_it:
		for c in order_countries:
			for y in order_years:
				wb_checkiftheyhave_list.append([c,wb_i,y])
	for UN_i in UN_indi_it:
		for c in order_countries:
			for y in order_years:
				un_checkiftheyhave_list.append([c,UN_i,y])
	for wb in wb_checkiftheyhave_list:
		id_as_str=str(wb_indi_list[wb[1]]['id']) 
		raw_wb_avail_call=rq.get('http://api.worldbank.org/countries/' + wb[0] + '/indicators/' + id_as_str + '?per_page=100&date=' + wb[2] +'&format=json')
		wb_avail_json=raw_wb_avail_call.json()
		if str(wb_avail_json[1]) == 'None':
			errorlist.append('http://api.worldbank.org/countries/' + wb[0] + '/indicators/' + id_as_str + '?per_page=100&date=' + wb[2] +'&format=json')
		else:
			value=wb_avail_json[1][0]['value']
			try:
				float(value)
			except TypeError:
				mislist.append([wb[0],id_as_str,wb[2]])
			else:
				key_string=str(wb_avail_json[1][0]['indicator']['value']+' for '+wb[0]+' '+wb[2])
				wb_availibility_dic.update({key_string:wb_avail_json})
			finally:
				pass
	for UN in un_checkiftheyhave_list:
		id_as_str=UNHDR_indi_list[UN[1]]
		raw_un_avail_call=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/' + id_as_str + '/year/' + UN[2] + '/country_code/' + UN[0])
		UN_avail_json=raw_un_avail_call.json()
		if type(UN_avail_json) == unicode:
			mislist.append(UNHDR_indi_dic[id_as_str])
			mislist.append('for'+UN[0]+UN[2])
		else:
			to_add_to_avail_dic=[UN[0],UN[2],id_as_str,UN_avail_json]
			key_string=str(UN_avail_json['indicator_name'][id_as_str].encode('ascii', 'ignore')+' for '+UN[0]+' '+UN[2])
			UNHDR_availibility_dic.update({key_string:to_add_to_avail_dic})
	all_source_master_dic={'World Bank': wb_availibility_dic, 'UNHDR':UNHDR_availibility_dic}
	with open('availibility.json','w') as fp:
		json.dump(all_source_master_dic, fp)
if __name__ in '__main__':
	bartender()