'''unhdr data derping
via http://hdr.undp.org/en/content/developers-data-api
meta information on indicators is sparse at best --
http://hdr.undp.org/sites/default/files/hdr2015_technical_notes.pdf

maybe we should try wikipedia?
'''
Years
1980
1985
1990
1995
2000
2005
2010
2011
2012
2013

In [1]: import json

In [2]: import requests as rq

In [3]: raw=json=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/137506/year/2013/country_code/bra')

In [4]: raw
Out[4]: <Response [200]>

In [6]: raw.json()
Out[6]:
{u'country_name': {u'BRA': u'Brazil'},
 u'indicator_name': {u'137506': u'HDI: Human development index (HDIg) value'},
 u'indicator_value': [[u'BRA', u'137506', u'2013', u'0.744']]}


###########for ind list
#to scrape or call? heres both. Note that both have both ISOs and indi IDs!!!!
#scrape
html = urlopen('http://hdr.undp.org/en/content/developers-data-api').read()
BS = BeautifulSoup(html, "lxml")
listss=BS.find_all('ul')
HTTPError: HTTP Error 403: Forbidden

#json
un_indi=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator')
jun_indi=un_indi.json()
UNHDR_indi_dic=jun_indi['indicator_name']

In [8]: jun_indi['indicator_name']['89006']
Out[8]: u'Maternal mortality ratio'

##backup iso
	un_indi=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator')
	jun_indi=un_indi.json()
	backup_iso=jun_indi['country_name']


##haz dat v no haz dat
In [57]: raw_UN_avail_json=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/137506/year/2013/country_code/bra')

In [59]: unhaz=raw_UN_avail_json.json()

In [60]: unhaz
Out[60]:
{u'country_name': {u'BRA': u'Brazil'},
 u'indicator_name': {u'137506': u'HDI: Human development index (HDIg) value'},
 u'indicator_value': [[u'BRA', u'137506', u'2013', u'0.744']]}

In [61]: raw_UN_avail_json=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/137506/year/1989/country_code/bra')

In [62]: unNOhaz=raw_UN_avail_json.json()

In [63]: unNOhaz
Out[63]: u'No data was found for the request version/1/indicator_id/137506/year/1989/country_code/bra'

In [64]: type(unNOhaz)
Out[64]: unicode

In [65]: str(unNOhaz)
Out[65]: 'No data was found for the request version/1/indicator_id/137506/year/1989/country_code/bra'


################
##AT or around line219 in Bartender WB and UN.py
#now that we have data, how do we make it play nicely with other data?
	print UN_raw_jaysohn

[
{u'country_name': {u'BRA': u'Brazil'}, 
u'indicator_name': {u'43606': u'Internet users'}, 
u'indicator_value': [[u'BRA', u'43606', u'2000', u'2.9']]}
]

In [55]: ob=UN_raw_jaysohn

In [56]: df_ob=pd.DataFrame(ob)

In [57]: df_ob
Out[57]:
          country_name                 indicator_name  \
0  {u'BRA': u'Brazil'}  {u'43606': u'Internet users'}

             indicator_value
0  [[BRA, 43606, 2000, 2.9]]

In [62]: type(df_ob['indicator_value'])
Out[62]: pandas.core.series.Series

In [63]: df_ob['indicator_value'][0]
Out[63]: [[u'BRA', u'43606', u'2000', u'2.9']]

In [64]: df_ob['indicator_value'][0][0]
Out[64]: [u'BRA', u'43606', u'2000', u'2.9']

In [65]: df_ob['indicator_value'][0][0][0]
Out[65]: u'BRA'

###cleaning lists, dicts nested in raw json
In [89]: UN_raw_jaysohn[0]['indicator_value']=UN_raw_jaysohn[0]['indicator_value'][0][3]

In [90]: UN_raw_jaysohn[0]
Out[90]: {u'country_name': {}, u'indicator_name': {}, u'indicator_value': u'2.9'}