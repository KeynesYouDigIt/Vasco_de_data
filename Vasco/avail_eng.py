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

def get_avail(countries=['BRA','PER','CHL'], years=['2011','2012','2013']):
    '''this is function is the begining of a project to make the original API (archive/Bartender_no_ui.py) modular and flexible. 
    as stated in views.py, I plan on creating a robust system that calls the public data APIs and stores the data in a Postgres database.'''

    '''put desired countries, years, indicators as strings. 
    ISO codes for countries'''
    order_countries=countries
    order_years=years
    saveas_file_type='csv'
    save_dir=os.getcwd()

    #the below gets a list of dictionaries that constitutes a full library of World Bank indicators
    #the indicators are simply represented by meta data which is converted into actual indicator names below (line 91 and on)

    ###by generating its own iterator it violates 7 PEP 279, I am hoping to fix that soon.
    ###I should be able to test and remove of the global calls soon, as this is not good practice long term.
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


    #the below gets a list of dictionaries that constitutes a full library of United Nations indicators
    #the indicators are simply represented by id numbers which are converted into actual indicator names below (line 91 and on)
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

    #the below gets a list a Dictionary of ISO codes and their corresponding countries
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

    #the below reverses the ISO code dictionary in a new object to get country name using the ISO code
    global iso_dic_code_is_key
    iso_dic_code_is_key={v: k for k, v in iso_dic.items()}

    #lines 91-165 parse the dictionaries above to check the availibility of every indicator for the specified Countries (or entities) and years
    #if the data exists, it is returned
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

    wb_finished_avail=[]
    ob=0
    for i in wb_availibility_dic.keys():
        wb_finished_avail.append({})
        wb_finished_avail[ob]['Country']=str(wb_availibility_dic[i][1][0]['country']['value'])
        wb_finished_avail[ob]['Year']=wb_availibility_dic[i][1][0]['date']
        wb_finished_avail[ob][str(wb_availibility_dic[i][1][0]['indicator']['value'])]=wb_availibility_dic[i][1][0]['value']
        ob+=1

    un_finished_avail=[]
    ob=0
    for i in UNHDR_availibility_dic.keys():
        un_finished_avail.append({})
        un_finished_avail[ob]['Country']=str(UNHDR_availibility_dic[i][3]['country_name'][UNHDR_availibility_dic[i][0]])
        un_finished_avail[ob]['Year']=UNHDR_availibility_dic[i][1]
        un_finished_avail[ob][str(UNHDR_availibility_dic[i][3]['indicator_name'][UNHDR_availibility_dic[i][2]].encode('ascii', 'ignore'))]=UNHDR_availibility_dic[i][3]['indicator_value'][0][3]
        ob+=1

    both=[un_finished_avail,wb_finished_avail]
    

    return both


def make_files(ftype='csv'):

    ftype=ftype

    if ftype='csv':
        with open('wb_availibility.json', 'w') as fp:
            wb_df=pd.DataFrame(both)
            wb_df.to_csv('availibility.csv')

    elif ftype='json':
        with open('un_availibility.json', 'w') as fp:
            json.dump(un_finished_avail, fp)