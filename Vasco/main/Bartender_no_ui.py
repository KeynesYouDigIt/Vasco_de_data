##pubdatapub - Countries#
##Working!!! 12/20#
#This code has no UI, simply replace the objects with the iso codes
#Years and indicators desired.
############################
import os
import lxml
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests as rq
import io
from io import StringIO, BytesIO
import urllib2 as url
from urllib2 import urlopen

'''put desired countries, years, indicators as strings. 
ISO codes for countries pls'''
global filename
filename='fertility, education, and mortality'
global order_countries
order_countries=['BRA','PER','ECU','CHL','BOL','COL','VEN','ARG','ZAF','CHN','RUS']
global order_years
order_years=['2005','2010','2011','2012','2013']
global indic_name
indic_name=[
'Population, total both sexes (thousands)'
,'Infant mortality rate'
,'Total fertility rate'
,'HDI: Education index'
,'Adult literacy rate, both sexes'
,'Coverage: Completing 6th grade on time'
,'Research and development expenditure (% of GDP)'
,'Access to electricity (% of total population)'
]
global glass
glass='csv'
global save_dir
save_dir=os.getcwd()

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

global iso_dic_code_is_key
iso_dic_code_is_key={v: k for k, v in iso_dic.items()}


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
###
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

global wb_raw_jaysohn
wb_raw_jaysohn=[]
global UN_raw_jaysohn
UN_raw_jaysohn=[]
for ing in recipe:
    if ing[1][0]=='from the World Bank data set':
        wb_name=ing[1][1]+' for '+ing[0]+' '+ing[2]
        try:
            wb_availibility_dic[wb_name][1][0]['country']['iso']=wb_name[-8:-5]
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
for i in UN_it:
    UN_ISO_code_as_str=str(UN_raw_jaysohn[i]['country_name'].keys()[0])
    UN_poured_jaysohn.append({})
    UN_poured_jaysohn[i]['Country']=str(iso_dic_code_is_key[UN_raw_jaysohn[i]['country_name'].keys()[0]])
    UN_poured_jaysohn[i]['Year']=str(UN_raw_jaysohn[i]['indicator_value'][0][2])
    UN_indic_id_as_str=str(UN_raw_jaysohn[i]['indicator_name'].keys()[0])
    UN_poured_jaysohn[i][UN_raw_jaysohn[i]['indicator_name'][UN_indic_id_as_str]]=str(UN_raw_jaysohn[i]['indicator_value'][0][3])

for i in wb_it:
    WB_poured_jaysohn.append({})
    WB_poured_jaysohn[i]['Country']=iso_dic_code_is_key[wb_raw_jaysohn[i][0]['country']['iso']]
    WB_poured_jaysohn[i]['Year']=wb_raw_jaysohn[i][0]['date']
    WB_indic_id_as_str=wb_raw_jaysohn[i][0]['indicator']['id']
    WB_inidic_name_as_str=wb_raw_jaysohn[i][0]['indicator']['value']
    WB_poured_jaysohn[i][WB_inidic_name_as_str]=wb_raw_jaysohn[i][0]['value']

global Mixed_and_Poured_names
Mixed_and_Poured_names=[]
global Mixed_and_Poured
Mixed_and_Poured=[]
for i in UN_poured_jaysohn:
    Mixed_and_Poured.append(i)
for i in WB_poured_jaysohn:
    Mixed_and_Poured.append(i)

def match_up(list_o_dics, llave):
    it=-1
    nxt=it+1
    for dick in list_o_dics:
        it+=1
        #print 'now batting %s' % it
        matched_it=[]
        while True:
            if nxt < len(list_o_dics):
                if [list_o_dics[it][llave[0]],list_o_dics[it][llave[1]]]==[list_o_dics[nxt][llave[0]],list_o_dics[nxt][llave[1]]]:
                    #print 'matched %s %s' % (it,nxt)
                    matched_it.append(nxt)
                    #print matched_it
                    nxt+=1
                else:
                    #print 'no match %s %s' % (it,nxt)
                    nxt+=1
            else:
                matched_it.append(it)
                #print 'updating now using %s' % matched_it
                to_pop=[]
                for i in matched_it:
                    list_o_dics[matched_it[0]].update(list_o_dics[i])
                    if i != it:
                        to_pop.append(i)
                to_pop.sort(reverse=True)
                for i in to_pop:
                    list_o_dics.pop(i)
                nxt=it+1
                break

match_up(Mixed_and_Poured, llave=['Country','Year'])
global final_df
final_df=pd.DataFrame.from_records(Mixed_and_Poured)

if glass in ['json','JSON','Json','jayson','javascript']:
    print('going home already? lol jk I have no idea how long you have been here.')
    print('[ : ) ]')
    with open(filename+'.json', 'w') as fp:
        json.dump(Mixed_and_Poured, fp)
elif glass in ['csv','CSV','Excel','excel','C','Cs','CS']:
	final_df.to_csv(filename+'.csv')
				