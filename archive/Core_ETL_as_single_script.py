import os
import datetime
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
from Vasco.order_takers import get_countries_etld

#from Scraper_for_UN_indicator_descriptions import UNHDR_scrape_description

'''This is the core ETL process based on the original API. it uniformilizes and loads indicat'''

def get_supporting_data():
    #the below gets a list a Dictionary of ISO codes and their corresponding countries
    html = urlopen('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3').read()
    BS = BeautifulSoup(html, "lxml")
    tds = BS.find_all('td')
    herp_it = []
    it =- 1
    for d in tds:
        it += 1
        herp_it.append(it)

    herp_it = np.asarray(herp_it)
    global iso_dic
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

    Years=[]
    add_this_year=1989
    while add_this_year < 2015:
        add_this_year +=1
        Years.append(add_this_year)

    #the below reverses the ISO code dictionary in a new object to get country name using the ISO code
    global iso_dic_code_is_key
    iso_dic_code_is_key={v: k for k, v in iso_dic.items()}

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

    wb_indi_it=np.asarray(wb_indi_it)

    #the below gets a list of dictionaries that constitutes a full library of United Nations indicators
    #the indicators are simply represented by id numbers which are converted into actual indicator names below (line 91 and on)
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

    ETL_logger = open('ETL_log_tests.txt', 'w')
    ETL_logger.write('initial objects created and log started at' + str(datetime.now().utcnow()) + '\n')


def get_countries():
    '''this gets and commits all countries and iso codes'''
    for country in iso_dic:
        camelot = Entity(
            level='Country', 
            name=country, 
            iso_code=iso_dic[country]
            )
        db.session.add(camelot)
    db.session.commit()

def get_meta_indicator_data():
    '''This gets and commits indicator meta info'''
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
    #NOTE this commit currently throws non fatal errors for indictors that are in the world bank set and have the same name (2-3 right now). Next data refresh tis will be debugged
    for indicator in wb_indi_it:
        #try and except here is for indicators without topics (aka "families"), which throw index and key errors
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


def get_literal_indicators(countries=iso_dic_code_is_key.keys(), years=Years):
    '''this is function is the begining of a project to make the original API (archive/Bartender_no_ui.py) modular and flexible. 
    as stated in views.py, I plan on creating a robust system that calls the public data APIs and stores the data in a Postgres database.'''
    
    #below should be a list of ISO codes

    '''
    In [24]: len(iso_dic)
    Out[24]: 249
    0-15 already done
    '''
    years=Years


    order_countries=[countries]
    order_years=years


    #lines 95-165 parse the dictionaries above to check the availibility of every indicator for the specified Countries (or entities) and years
    #if the data exists, it is extracted

    wb_availibility_dic={}

    wb_checkiftheyhave_list=[]

    UNHDR_availibility_dic={}

    un_checkiftheyhave_list=[]

    mislist=[]

    for wb_i in wb_indi_it:
        for c in order_countries:
            for y in order_years:
                wb_checkiftheyhave_list.append([str(c),wb_i,str(y)])

    for UN_i in UN_indi_it:
        for c in order_countries:
            for y in order_years:
                un_checkiftheyhave_list.append([str(c),UN_i,str(y)])

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
        id_as_str=UNHDR_indi_list[UN[1]]
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
                    mislist.append(UNHDR_indi_dic[id_as_str])
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
        print db.engine.execute('select * from meta').first()
    except:
        db.session.rollback()
        pass

try:
    get_countries()
    print 'got countries'
except:
    print 'get meta failed. might we already have this data?'
    try:
        print db.engine.execute('select * from ent').first()
    except:
        db.session.rollback()
        pass

get_supporting_data()

already_got=get_countries_etld()

already_got=[country[0] for country in already_got]

get_these=raw_input('gimmie countries, by iso code, we need data for')

get_these=get_these.split(',')

for c in get_these:
    if c in already_got:
        get_these.pop(c)
    else:
        pass

for country in get_these:
        print 'now attempting to get %s' % country
        get_literal_indicators(countries=country, years=Years)
        ETL_logger.write('succeeded on %s' % country)
        print 'finished on %s, printing last record in db to see if it went through' % country
        print db.engine.execute('select * from literal').fetchall()[-1]

ETL_logger.close()