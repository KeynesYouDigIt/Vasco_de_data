import os
import lxml
from bs4 import NavigableString
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests as rq
import urllib2 as url
from urllib2 import urlopen
import unicodedata

'''
this part of the project is being tabled. I cannot get the names on the website to match the names from the API, so the descriptions are not matching
'''

def UNHDR_scrape_description():
    #the final object will be a dictionary with indicator name as the key and desctiption as content
    may_contain_indicators=[]
    clean_listed_indicators={}
    urls = ['http://hdr.undp.org/en/composite/HDI',
    'http://hdr.undp.org/en/composite/IHDI',
    'http://hdr.undp.org/en/composite/trends',
    'http://hdr.undp.org/en/composite/GDI',
    'http://hdr.undp.org/en/composite/GII',
    'http://hdr.undp.org/en/composite/MPI',]
    for url in urls:
        url_response_raw = rq.get(url)
        BS = BeautifulSoup(url_response_raw.text, "lxml")
        p_elements = BS.find_all('p')
        p_contents = []
        for e in p_elements:
            p_contents.append(e)
            for paragraph in p_contents:
                if not isinstance(paragraph,NavigableString):
                    if 'Definitions' in paragraph.text:
                        may_contain_indicators.append(paragraph)

    for paragraf in may_contain_indicators:
        if ':' in paragraf.text:
            with_colons_added = paragraf.get_text('::')
            dub_colon_as_list = []
            for i in enumerate(with_colons_added.split('::')):
                dub_colon_as_list.append(i)
            for i,string in dub_colon_as_list:
                if ': ' in string:
                    indicator_name_full=str(unicodedata.normalize('NFKD',dub_colon_as_list[i-1][1]).encode('ascii', 'ignore')).strip('\n')
                    indicator_name_abridged=indicator_name_full[:indicator_name_full.find(':')]
                    description=str(unicodedata.normalize('NFKD',dub_colon_as_list[i][1]).encode('ascii', 'ignore')).strip('\n')
                    if i+1<len(dub_colon_as_list) and 'http' in dub_colon_as_list[i+1][1]:
                        details_link=dub_colon_as_list[i+1][1]
                    else:
                        details_link ='no further link provided for this indicator'
                    print 'adding %s %s %s' % (indicator_name_abridged, description, details_link)
                    clean_listed_indicators[indicator_name_abridged]=[description,details_link]
    return clean_listed_indicators


