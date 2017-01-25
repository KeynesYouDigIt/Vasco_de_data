'''This is the core ETL process based on the original API. 
it uniformilizes and loads indicator data'''

print 'Please be patient while the interface loads, \n'
print 'these functions use various python libraries that can take a moment to boot.'

import os
import datetime
import time
import lxml
from bs4 import NavigableString
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests as rq
import urllib2 as url
from urllib2 import urlopen
from Vasco.models import *
from Vasco.order_takers import get_countries_etld, create_years

def scrape_ISO_codes():
    '''the below gets a tuple of a Dictionary of ISO codes and their 
    corresponding countries and the same dictionary with keys and values reversed'''
    html = urlopen('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3').read()
    BS = BeautifulSoup(html, "lxml")
    tds = BS.find_all('td')
    herp_it = []
    it =- 1
    for d in tds:
        it += 1
        herp_it.append(it)

    herp_it = np.asarray(herp_it)
    iso_dic = {}
    for t in herp_it:
        s_td = tds[t].string
        if s_td == None:
            pass
        else:
            l_s_td = len(s_td)
            nxt = t+1
            if l_s_td == 3:
                iso_dic.update({tds[nxt].string:s_td})
            else:
                pass

    iso_dic_code_is_key={v: k for k, v in iso_dic.items()}

    return iso_dic, iso_dic_code_is_key




def get_worldbank_indicator_list():
    '''the below gets a list of dictionaries that constitutes a full 
    library of World Bank indicators'''
    indi=rq.get('http://api.worldbank.org/indicators?format=json')
    jindi=indi.json()
    wb_indi_list=jindi[1]

    return wb_indi_list



def get_UN_indicator_dic():
    '''the below gets a dictionary that constitutes a full 
    library of United Nations indicators'''
    un_indi=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator')
    jun_indi=un_indi.json()
    UNHDR_indi_dic=jun_indi['indicator_name']

    return UNHDR_indi_dic


def get_countries():
    '''this gets and commits all countries and iso codes to the database'''
    ISOs = scrape_ISO_codes()[0]
    for country in ISOs:
        camelot = Entity(
            level='Country', 
            name=country, 
            iso_code=ISOs[country]
            )
        db.session.add(camelot)
    db.session.commit()

def get_meta_indicator_data():
    '''This gets and commits indicator meta info to the database'''
    for ind in jun_indi['indicator_name']:
        UN_indicator=Meta_indicator_data(
            p_name=jun_indi['indicator_name'][ind].encode('ascii', 'ignore'),
            family='none assigned yet',
            num_type='none assigned yet',
            provider='United nations Human Development Report',
            p_description='this provider has indicator descriptions, but this computer can\'t (yet) figure out how to match them to the right indicator. \n please see more info at http://hdr.undp.org/en/data',
            ) 
        try:  
            db.session.merge(UN_indicator)
            print ' %s added successfully to session' % UN_indicator
        except:
            db.session.rollback()
            print ' %s skipped' % UN_indicator
    db.session.commit()
    
    wb_indi_list=get_worldbank_indicator_list()
    wb_indi_it=enumerate(wb_indi_list)
    for indicator in wb_indi_it:
        #try and except here is for indicators without topics 
        #(aka "families"), which throw index and key errors
        try:
            WB_indicator=Meta_indicator_data(
                p_name=wb_indi_list[indicator]['name'],
                family=wb_indi_list[indicator]['topics'][0]['value'],
                num_type='none assigned yet',
                provider='The World Bank, via: ' + wb_indi_list[indicator]['source']['value'],
                p_description=wb_indi_list[indicator]['sourceNote'],
                )
            db.session.merge(WB_indicator)
            print ' %s added successfully to session' % indicator
            db.session.commit()
        except:
            db.session.rollback()
            WB_indicator=Meta_indicator_data(
                p_name=wb_indi_list[indicator]['name'],
                family='none assigned yet',
                num_type='none assigned yet',
                provider='The World Bank, via: ' + wb_indi_list[indicator]['source']['value'],
                p_description=wb_indi_list[indicator]['sourceNote'],
                )
            db.session.merge(WB_indicator)
            print ' %s added successfully to session' % indicator
            db.session.commit()


def get_literal_indicators(countries, years=create_years()):
    '''this is function is the begining of a project to make the 
    original API (archive/Bartender_no_ui.py) modular and flexible. 
    As stated in views.py, I plan on creating a robust system that 
    calls the public data APIs and stores the data in a Postgres database.'''

    order_countries=[countries]
    order_years=years

    #lines 95-165 parse the dictionaries above to check the availibility of 
    #every indicator for the specified Countries (or entities) and years
    #if the data exists, it is extracted

    wb_availibility_dic={}
    wb_checkiftheyhave_list=[]
    UNHDR_availibility_dic={}
    un_checkiftheyhave_list=[]
    mislist=[]
    wb_indi_list=get_worldbank_indicator_list()
    UN_indi_dic=get_UN_indicator_dic()

    for wb_i in enumerate(wb_indi_list):
        for c in order_countries:
            for y in order_years:
                wb_checkiftheyhave_list.append([str(c),wb_i[0],str(y[0])])

    for UN_i in enumerate(UN_indi_dic):
        for c in order_countries:
            for y in order_years:
                un_checkiftheyhave_list.append([str(c),UN_i[0],str(y[0])])

    for wb in wb_checkiftheyhave_list:
        id_as_str=str(wb_indi_list[wb[1]]['id'])
        call='http://api.worldbank.org/countries/' + wb[0] + '/indicators/' + id_as_str + '?per_page=100&date=' + wb[2] +'&format=json'
        ETL_logger.write('fething from world bank : %s \n' % call)
        print 'fething from world bank : %s \n' % call
        wb_raw_response=rq.get(call)
        if str(wb_raw_response) == '<Response [400]>':
            #servers erroring out, may be too many requests
            ETL_logger.write('ERROR ON WB SERVERS!!! response from world bank api %s \n xxxxxxxxxxxx \n' % wb_raw_response)
        else:
            wb_avail_json=wb_raw_response.json()
            try:
                for obj in wb_avail_json[0]:
                    ETL_logger.write(str(obj) + str(wb_avail_json[0][obj]) + '\n')
                try:
                    #GUF BLM and other iso codes are returning an error will investigate later and silence for now
                    #these are most likely countries not in the wb database  like French Guiana or Saint-Barthelemy
                    if str(wb_avail_json[1]) == 'None':
                        mislist.append(id_as_str)
                        mislist.append('for '+str(wb[0])+str(wb[2]))
                        mislist.append(str(call))
                    else:
                        value=wb_avail_json[1][0]['value']
                        try:
                            float(value)
                        except TypeError:
                            mislist.append('Type error on ' + id_as_str)
                            mislist.append('for '+str(wb[0])+str(wb[2]))
                            mislist.append(str(call))
                        key_string=str(wb_avail_json[1][0]['indicator']['value']+' for '+wb[0]+' '+wb[2])
                        wb_availibility_dic.update({key_string:wb_avail_json})
                        ETL_logger.write('successfully got %s \n--\n %s \n --' % (key_string,wb_avail_json))
                        print 'successfully got %s \n--\n %s \n --' % (key_string,wb_avail_json)
                except:
                    mislist.append(id_as_str)
                    mislist.append('for '+str(wb[0])+str(wb[2]))
                    mislist.append(str(call))
            except:
                ETL_logger.write('key or unspecd error on %s' % call)
                ETL_logger.write('\n\n')


    ETL_logger.write('the following world bank indicators were determined to be missing or in error\n')
    for m in mislist:
        ETL_logger.write(m.encode('ascii', 'ignore') + ', ')


    mislist=[]
    for UN in un_checkiftheyhave_list:
        id_as_str=UN_indi_dic.keys()[UN[1]]
        call='http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/' + id_as_str + '/year/' + UN[2] + '/country_code/' + UN[0]
        ETL_logger.write('fething from UNHDR %s' % call)
        print 'fething from UNHDR : %s \n' % call
        un_raw_response=rq.get(call)
        if str(un_raw_response) == '<Response [400]>':
            ETL_logger.write('ERROR ON WB SERVERS!!! response from world bank api %s \n xxxxxxxxxxxx \n' % wb_raw_response)
        else:
            UN_avail_json=un_raw_response.json()
            try:
                if type(UN_avail_json) == unicode:
                    mislist.append(UN_indi_dic[id_as_str])
                    mislist.append('for '+UN[0]+UN[2])
                    mislist.append(call)
                else:
                    to_add_to_avail_dic=[UN[0],UN[2],id_as_str,UN_avail_json]
                    key_string=str(UN_avail_json['indicator_name'][id_as_str].encode('ascii', 'ignore')+' for '+UN[0]+' '+UN[2])
                    UNHDR_availibility_dic.update({key_string:to_add_to_avail_dic})
                    ETL_logger.write('successfully got %s \n--\n %s \n --' % (key_string,to_add_to_avail_dic))
                    print 'successfully got %s \n--\n %s \n --' % (key_string,to_add_to_avail_dic)
            except:
                ETL_logger.write('un specd error on %s' % call)
                ETL_logger.wrie('\n\n')

    ETL_logger.write('the following UNHDR indicators were determined to be missing or in error\n')
    for m in mislist:
        ETL_logger.write(m.encode('ascii', 'ignore') + ', ')

    #begin database processes
    for i in wb_availibility_dic.keys():
        #lit = Literal_data(ent_id=1, year=2012, 
        #value=2, display_name = 'swallow count', meta_id=1)
        try:
            point=Literal_data(
                ent_id=Entity.get_by_name(str(wb_availibility_dic[i][1][0]['country']['value'])).id,
                year=wb_availibility_dic[i][1][0]['date'],
                display_name=str(wb_availibility_dic[i][1][0]['indicator']['value']),
                value=wb_availibility_dic[i][1][0]['value'],
                meta_id=Meta_indicator_data.query.filter_by(p_name=wb_availibility_dic[i][1][0]['indicator']['value']).first().id,
            )
            ETL_logger.write('adding %s for ent id - %s and meta id - %s' % (point.display_name, point.ent_id, point.meta_id))
            db.session.add(point)
            db.session.commit()
        except:
            db.session.rollback()
            ETL_logger.write('cant find %s' % wb_availibility_dic[i][1][0]['country']['value'] +'in meta tabe \n')
            db.session.rollback()


    for i in UNHDR_availibility_dic.keys(): 
        try:
            point=Literal_data(
                ent_id=Entity.get_by_name(str(UNHDR_availibility_dic[i][3]['country_name'][UNHDR_availibility_dic[i][0]])).id,
                year=UNHDR_availibility_dic[i][1],
                display_name=str(UNHDR_availibility_dic[i][3]['indicator_name'][UNHDR_availibility_dic[i][2]].encode('ascii', 'ignore')),
                value=UNHDR_availibility_dic[i][3]['indicator_value'][0][3],
                meta_id=Meta_indicator_data.query.filter_by(p_name=UNHDR_availibility_dic[i][3]['indicator_name'][UNHDR_availibility_dic[i][2]].encode('ascii', 'ignore')).first().id,
            )
            print 'adding %s for ent id - %s and meta id - %s' % (point.display_name, point.ent_id, point.meta_id)
            ETL_logger.write('adding %s for ent id - %s and meta id - %s' % (point.display_name, point.ent_id, point.meta_id))
            db.session.add(point)
            db.session.commit()
        except:
            db.session.rollback()
            print 'cant find %s' % UNHDR_availibility_dic[i][3]['indicator_name'][UNHDR_availibility_dic[i][2]].encode('ascii', 'ignore') +'in meta tabe \n'
            ETL_logger.write('cant find %s' % UNHDR_availibility_dic[i][3]['indicator_name'][UNHDR_availibility_dic[i][2]].encode('ascii', 'ignore') +'in meta tabe \n')
            db.session.rollback()

try:
    get_meta_indicator_data()
    print 'got metas'
except:
    print 'get meta failed. might we already have this data?'
    try:
    	print 'Here is everything in the meta table'
        print db.engine.execute('select * from meta').first()
    except:
        db.session.rollback()
        pass

try:
    get_countries()
    print 'got countries'
except:
    print 'get countries failed. might we already have this data?'
    try:
    	print 'Here is everything in the countries table'
        print db.engine.execute('select * from ent').first()
    except:
        db.session.rollback()
        pass

already_got=get_countries_etld()

already_got=[country[0] for country in already_got]

all_or_some=raw_input('if you would like to try and build out the entire database, type \'all\', other wise hit enter ')
if str(all_or_some)=='all':
	print 'getting all countries availible...'
	get_these=[]
	for iso_code in scrape_ISO_codes()[1]:
		get_these.append(iso_code)
else:
	get_these=raw_input('type countries, by iso code, we need data for, seperated by comma \n')
	get_these=get_these.split(',')
print get_these

for c in get_these:
    if c in already_got:
        get_these.pop(c)
    else:
        pass

logname='data_extraction_log__'+\
str(datetime.datetime.now().month)+\
str(datetime.datetime.now().day)+\
str(datetime.datetime.now().year)

ETL_logger = open(logname+'.txt', 'w')
ETL_logger.write('initial objects created and log started at' + str(datetime.datetime.now().utcnow()) + '\n')


for country in get_these:
        print 'now attempting to get %s' % country
        get_literal_indicators(countries=country)
        ETL_logger.write('succeeded on %s' % country)
        print 'finished on %s, printing last record in db to see if it went through' % country
        print db.engine.execute('select * from literal').fetchall()[-1]
        print 'sleeping for 5 minutes to avoid server over load'
        time.sleep(300)

ETL_logger.close()