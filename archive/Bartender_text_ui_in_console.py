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
def drink_or_first_mix():
	print('so here at pub data pub, we can refirst_mix your coctail if you dont like how it looks, or if you want to try something else with it.')
	print('[ : ) ]')
	d_m=raw_input('if you would like to see what else we can do with your data here, type mix. If youd like to start from scratch, say bartender. If you have what you need, type drink and we will save the data to a file')
	d_m=str(d_m)
	if d_m in 'mix':
		pre_first_mix()
	elif d_m in 'bartender':
		bartender()
	elif d_m in 'drink':
		drink()

def get_dics():
	indi=rq.get('http://api.worldbank.org/indicators?format=json')
	jindi=indi.json()
	global wb_indi_list
	wb_indi_list=jindi[1]
	global wb_indi_it
	wb_indi_it = []
	it=-1
	for i in wb_indi_list:
		it += 1
		wb_indi_it.append(it)
	wb_indi_it=np.asarray(wb_indi_it)
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

def bartender():
	get_dics()
	print('welcome to pubdatapub! a place where nasty, unorginized public data is first_mixed and served as you want it: a complex, rich, coctail, or a straight pour of a single data set.')
	print('sadly, my developer is a hardcore n00b at all this, but the great folks at blazing db are giving him a chance to build something special! email feedback to altereeeeego@gmail.com')
	print('/////////')
	print('be sure to check out blazing db at http://blazingdb.com/')
	print('/////////')
	print('So right now, I have data from the World Bank on global economics and data from the UN Human development Report on Poverty and standard of living')
	print('[ : ) ]')
	not_iso_order_countries=raw_input("Hey there, which countries in your custom data coctail tonight? Please seperate each with a comma, don't just throw em all me at once. They are case sensitive (its an entire country! don't be lazy.)")
	not_iso_order_countries=str(not_iso_order_countries)
	not_iso_order_countries=not_iso_order_countries.split(',')
	#>spellchecker here
	global order_countries
	order_countries = []
	for co in not_iso_order_countries:
		if co in iso_dic:
			order_countries.append(iso_dic[co])
		else:
			print('I cant find the ISO code for %s , is that country spelled right?') % co
			YN=raw_input('Care to try that country name agin? Type Y for yes or N for no')
			if YN in ('n', 'no', 'N', 'No', 'NO'):
				print('OK, on we go')
			elif YN in ('y','ye', 'yes','Yes','Y','YEs','YES'):
				correction=raw_input('ok type that (or those) country name(s) again')
				if correction in iso_dic:
					print('oh you meant %s !! why didnt you say so? yeah I got their ISO code we are all set to move on.') % correction
				else:
					YNtwo=raw_input('still not gettin it. Start over (Start) or Move on without this country (Go)')
					if YNtwo == 'Start' or 'start':
						bartender()
					else:
						pass
			else:
				YN=raw_input('what? Y for yes N for no')
	global order_years
	order_years=raw_input('Got it! For which years do you need data? seperate each with a comma as well')
	order_years=str(order_years)
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
			#saving the JSON since we already have it, to use later in first_mix
			to_add_to_avail_dic=[UN[0],UN[2],id_as_str,UN_avail_json]
			key_string=str(UN_avail_json['indicator_name'][id_as_str].encode('ascii', 'ignore')+' for '+UN[0]+' '+UN[2])
			UNHDR_availibility_dic.update({key_string:to_add_to_avail_dic})
	source=raw_input('ok, I know what we have. To see missing data type missing, other wise type WB or UN to see different sources. just hit enter twice to skip')

	if source in ['m','miss','mising','missing',]:
		print('I dont have')
		print(mislist)
	elif source in ['WB']:
		print('Here is what I have from the World Bank')
		for w in wb_availibility_dic:
			try:
				print('WB', w)
				print(wb_availibility_dic[w][0:2])
			except UnicodeEncodeError:
				print('unicode error here :/ id is %s' % wb_availibility_dic[w][0:2])
	elif source in ['UN','UNHDR']:	
		for U in UNHDR_availibility_dic:
			try:
				print('un', U)
				print(UNHDR_availibility_dic[U][0:2])
			except UnicodeEncodeError:
					print('unicode error here :/ id is %s' % UNHDR_availibility_dic[U][0:2])
	else:
		source=raw_input('what? To see missing data type missing, other wise type WB or UN to see different sources. just hit enter to skip')
	indic_name=raw_input('which indicators would you like?')
	indic_name=str(indic_name)
	indic_name=indic_name.split(',')
	while '' in indic_name:
		indic_name.remove('')
	set_of_indics=set()
	missing_indis=[]
	for name in indic_name:
		for k in wb_availibility_dic.keys()[:]:
			if name in k:
				if name not in set_of_indics:
					set_of_indics.add('from the World Bank data set,'+name)
			else:
				pass
	for name in indic_name:
		for k in UNHDR_availibility_dic.keys()[:]:
			if name  in k:
				if name not in set_of_indics:
					set_of_indics.add('from United Nations data set,'+name)
			else:
				pass
	list_of_indics=[]
	for i in set_of_indics:
		not_toop=[]
		not_toop.append(i)
		toop=not_toop[0].split(',')
		list_of_indics.append(toop)
	global recipe
	recipe=[]
	for c in order_countries:
		for i in list_of_indics:
			for y in order_years:
				recipe.append([c,i,y])
	print('so I am going to mix')
	print(recipe)
	print('[ : ) ]')
	uat_pre_call=raw_input('Anything youd like to change before I get these ingredients and make your data coctail?')
	if uat_pre_call in ('n', 'no', 'N', 'No', 'NO'):
		print('OK, on we go. Let me go grab those ingredients and mix you up something nice.')
		first_mix()
	elif uat_pre_call in ('y','ye', 'yes','Yes','Y','YEs','YES'):
		print('OK, my developer is kinda lazy so we are starting over :/ ... in the future youll be able to pick out exactly whats missing')
		bartender()
	else:
		uat_pre_call=raw_input('what? Y for yes N for no')
def first_mix():
	global wb_raw_jaysohn
	wb_raw_jaysohn=[]
	global UN_raw_jaysohn
	UN_raw_jaysohn=[]
	for ing in recipe:
		if ing[1][0]=='from the World Bank data set':
			wb_name=ing[1][1]+' for '+ing[0]+' '+ing[2]
			try:
				wb_raw_jaysohn.append(wb_availibility_dic[wb_name][1])
			except KeyError:
				mislist.append(wb_name)
		elif ing[1][0]=='from United Nations data set':
			UN_name=ing[1][1]+' for '+ing[0]+' '+ing[2]
			try:
				UN_raw_jaysohn.append(UNHDR_availibility_dic[UN_name][3])
			except KeyError:
				mislist.append(UN_name)
	wb_it = []
	it=-1
	for d in wb_raw_jaysohn:
		it += 1
		wb_it.append(it)
	wb_it = np.asarray(wb_it)
	UN_it = []
	it=-1
	for d in UN_raw_jaysohn:
		it += 1
		UN_it.append(it)
	UN_it = np.asarray(UN_it)
	UN_poured_jaysohn=[]
	WB_poured_jaysohn=[]
	global first_mixed_and_Poured_names
	first_mixed_and_Poured_names=[]
	global first_mixed_and_Poured
	first_mixed_and_Poured=[]
	
	for i in UN_it:
		UN_poured_jaysohn.append({})
		UN_ISO_code_as_str=str(UN_raw_jaysohn[i]['country_name'].keys()[0])
		UN_poured_jaysohn[i]['Country']=str(UN_raw_jaysohn[i]['country_name'][UN_ISO_code_as_str])
		UN_poured_jaysohn[i]['Year']=str(UN_raw_jaysohn[i]['indicator_value'][0][2])
		UN_indic_id_as_str=str(UN_raw_jaysohn[i]['indicator_name'].keys()[0])
		UN_poured_jaysohn[i][UN_raw_jaysohn[i]['indicator_name'][UN_indic_id_as_str]]=str(UN_raw_jaysohn[i]['indicator_value'][0][3])
	first_mixed_and_Poured.append(UN_poured_jaysohn)
	first_mixed_and_Poured_names.append('UN_poured_jaysohn')
	for i in wb_it:
		WB_poured_jaysohn.append({})
		WB_poured_jaysohn[i]['Country']=wb_raw_jaysohn[i][0]['country']['value']
		WB_poured_jaysohn[i]['Year']=wb_raw_jaysohn[i][0]['date']
		WB_indic_id_as_str=wb_raw_jaysohn[i][0]['indicator']['id']
		WB_inidic_name_as_str=wb_raw_jaysohn[i][0]['indicator']['value']
		WB_poured_jaysohn[i][WB_inidic_name_as_str]=wb_raw_jaysohn[i][0]['value']
	first_mixed_and_Poured[0].append(WB_poured_jaysohn)
	first_mixed_and_Poured_names.append('WB_poured_jaysohn')
	
#making this uniform woud be much easier if it was one dict!! make it so!



















	print('ok I have the data!')
	print('--')
	print('dang, what a sexy looking data set! Please save your complements for my wonderful dev')
	print('here at PubDataPub, we can serve that in a JSON glass or move on to remix our coctail do cool stuff!')
	drink_or_first_mix()
def pre_first_mix():
	df=pd.DataFrame()
	global final_df
	final_df=pd.DataFrame(first_mixed_and_Poured_names)
	lines=raw_input('how many lines would you like in your preview? just hit a number and hit enter. If yould like to skip the preview, type 0 and hit enter.')
	try:
		print(final_df[:lines])
	except:
		print ('some kind of error occurred, but lets move on.')
	print('do something cool!!!! lol my dev hasnt built this yet. what a butthead.')
def drink():
	print('going home already? lol jk I have no idea how long you have been here.')
	print('[ : ) ]')
	prev=raw_input('just hit enter to continue, or type preview to glance at your data here in the console before saving.')
	if prev in ('p','pr','pre','prev','preview'):
		print(first_mixed_and_Poured)
	final_df_uat=raw_input('hit any key and enter to continue, unless you would like a different drink (set of data). If you need a different set, type NOPE in all caps and hit enter.')
	if final_df_uat == 'NOPE':
		print('*sigh* ok lets try this again. Bartender!')
		bartender()
	else:
		drink2()
def drink2():
	print('')
	glass=str(raw_input('Please enter, without the dot, the file type you need your data in. Ill let you know if we have it.'))
	if glass in ['csv','CSV','Excel','excel','C','Cs','CS']:
			pre_first_mix()
			save_dir=raw_input('Great! paste in the full path where you would like your file. For now, it will be a csv.')
			save_dir=str(save_dir)
			os.chdir(save_dir)
			final_df.to_csv('my_data.csv')
	elif glass in ['json','JSON','Json','jayson','javascript']:
			save_dir=raw_input('Great! paste in the full path where you would like your file. For now, it will be a json file.')
			save_dir=str(save_dir)
			os.chdir(save_dir)
			with open('data_cocktail.json', 'w') as fp:
				json.dump(first_mixed_and_Poured, fp)
	else:
		print('well Im not really programmed for that')
		do=raw_input('I can try to save to a %s file and see what happens, wanna try?')
		if do in ('n', 'no', 'N', 'No', 'NO'):
			print('arighty, so far its just CSV and JSON that are programmed to be returned properly. Try one of those.')
			drink2()
		elif do in ('y','ye', 'yes','Yes','Y','YEs','YES', 'ok', 'Ok', 'OK', 'k'):
			with open('data_cocktail.'+glass, 'w') as fp:
				try:
					fp.write(first_mixed_and_Poured)
					fp.close()
					print('Holy crap it worked!! I think. At least there wasnt an error.')
				except:
					print('that didnt work - there was an error. From the top!')
					drink2()
		else:
			print('come on man, its a yes or no question. Lets try this again-')
		drink2()
