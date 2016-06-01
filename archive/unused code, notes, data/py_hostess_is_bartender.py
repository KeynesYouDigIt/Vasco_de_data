###gets josn 1/5!!!!!
import web
import os
import json
import lxml
from lxml import html
from lxml import etree
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests as rq
import io
from io import StringIO, BytesIO
import urllib2 as url
from urllib2 import urlopen

os.chdir('C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub')

urls = (
  '/Bar', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('Front/templates/')

class Index(object):
	def GET(self):
		return render.Bar_form()

	def POST(self):
		form = web.input(countries="", years="")
		global CYorder
		CYorder = "%s %s" % (form.countries, form.years)
		CYorder=CYorder.split(' ')
		with open('C_Y_order.json', 'w') as fp:
			json.dump(CYorder, fp)
		bartender()
		return render.Bar(order_html = order)

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
	#iso code dic done
	for i in all_dics:
		if i.__class__==dict:
			fname=str(i)
			with open('fname', 'w')  as fp:
				json.dump(all_dics[i],fp)

def bartender():
	get_dics()
	not_iso_order_countries=str(CYorder[0])
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
	order_years=str(CYorder[1])
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
	global order
	order=all_source_master_dic
	with open('availibility.json','w') as fp:
		json.dump(all_source_master_dic, fp)
if __name__ == "__main__":
	app.run()