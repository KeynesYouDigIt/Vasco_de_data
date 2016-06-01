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
os.chdir('C:\\Users\\Vince\\Google Drive\\PeacefulMandE\\pubdatapub')

def get_dics():
	all_dics={}
	indi=rq.get('http://api.worldbank.org/indicators?format=json')
	jindi=indi.json()
	global wb_indi_list
	wb_indi_list=jindi[1]
	all_dics.update({'WB_list_of_indicators':wb_indi_list})
	global wb_indi_it
	wb_indi_it = []
	it=-1
	for i in wb_indi_list:
		it += 1
		wb_indi_it.append(it)
	wb_indi_it=np.asarray(wb_indi_it)
	#wb list done
	un_indi=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator')
	jun_indi=un_indi.json()
	global UNHDR_indi_dic
	UNHDR_indi_dic=jun_indi['indicator_name']
	global UNHDR_indi_list
	UNHDR_indi_list=[]
	for i in UNHDR_indi_dic:
		si=str(i)
		UNHDR_indi_list.append(si)
	global UN_indi_it
	UN_indi_it = []
	it=-1
	for i in UNHDR_indi_dic:
		it += 1
		UN_indi_it.append(it)
	UN_indi_it=np.asarray(UN_indi_it)
	all_dics.update({'UNHDR_indi_dic':UNHDR_indi_dic})
	all_dics.update({'UNHDR_indi_list':UNHDR_indi_list})
	#un list done
	html = urlopen('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3').read()
	BS = BeautifulSoup(html, "lxml")
	tds=BS.find_all('td')
	herp_it = []
	it=-1
	for d in tds:
		it += 1
		herp_it.append(it)
	herp_it = np.asarray(herp_it)
	global iso_dic
	iso_dic={}
	for t in herp_it:
		s_td=tds[t].string
		if s_td == None:
			pass
		else:
			l_s_td=len(s_td)
			nxt=t+1
			if l_s_td == 3:
				iso_dic.update({tds[nxt].string:s_td})
			else:
				pass
	all_dics.update({'ISO_codes_dictionary':iso_dic})
	global iso_dic_code_is_key
	iso_dic_code_is_key={v: k for k, v in iso_dic.items()}
	all_dics.update({'iso_dic_code_is_key':iso_dic_code_is_key})
	#iso code dic done
	for i in all_dics:
		if i.__class__==dict:
			fname=str(i)
			with open('fname', 'w')  as fp:
				json.dump(all_dics[i],fp)
get_dics()