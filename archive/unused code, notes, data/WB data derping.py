al_scarpone notes
#####TL:DR
#WB is giving us a list of dictionaries. the series is a list, each observation is a mini dictionary.
#If the fina db ever needs t go to sql, use http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
#http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
#
#
#
#
###############
getting indicator #list

In [49]: pindi=etree.fromstring(indi.content)

In [50]: pindi
Out[50]: <Element {http://www.worldbank.org}indicators at 0xb920408>

In [51]: indi=rq.get('http://api.worldbank.org/indicators')

print(etree.tostring(pindi, pretty_print=True))
#out: alll the xml
#if I want to go hard with that then here
#http://effbot.org/zone/element-namespaces.htm
...
#ew. how bout JSON for now???
indi=rq.get('http://api.worldbank.org/indicators?format=json')
jindi=indi.json()
In [110]: jindi[1][0]
Out[110]:
{u'id': u'1.0.HCount.1.25usd',
 u'name': u'Poverty Headcount ($1.25 a day)',
 u'source': {u'id': u'37', u'value': u'LAC Equity Lab'},
 u'sourceNote': u'The poverty headcount index measures the proportion of the population with daily per capita income below the poverty line.',
 u'sourceOrganization': u'LAC Equity Lab tabulations of SEDLAC (CEDLAS and the World Bank).',
 u'topics': [{u'id': u'11', u'value': u'Poverty '}]}

In [112]: jindi[1][0]['id']
Out[112]: u'1.0.HCount.1.25usd'

In [113]: jindi[1][0]['name']
Out[113]: u'Poverty Headcount ($1.25 a day)'
In [109]: jindi[0]
Out[109]: {u'page': 1, u'pages': 288, u'per_page': u'50', u'total': 14373}

In [117]: jindi[1][0]['topics'][0]['value']
Out[117]: u'Poverty '
In [120]: len(jindi[1])
Out[120]: 50
In [123]: jindi[1][49]['topics'][0]['value']
Out[123]: u'Poverty '

In [125]: jindi[1][45]
Out[125]:
{u'id': u'11.1_THERMAL.EFFICIENCY',
 u'name': u'Thermal efficiency (%) in power supply',
 u'source': {u'id': u'35', u'value': u'Sustainable Energy for All'},
 u'sourceNote': u'Thermal efficiency (%) in power supply:  This supply-side energy efficiency indicator measure the efficiency of thermal plants in converting primary energy sources\u2014such as coal, gas, and oil\u2014into electricity. They are calculated by dividing gross electricity production from electricity and cogeneration plants by total inputs of fuels into those plants. Whether market-based or privately owned, self-generating plants that do not export their power are included in the index assessment. In the case of cogeneration plants, fuel inputs are allocated between electricity and heat production in proportion to their shares of the annual output. ',
 u'sourceOrganization': u'World Bank and International Energy Agency (IEA Statistics \xa9 OECD/IEA, http://www.iea.org/stats/index.asp).  ',
 u'topics': []}

for i in herp_it:
  try:
    print jindi[1][i]['topics'][0]['value']
  except IndexError:
    print 'index error, probs no value for topics'
  else:
    print 'something else going on'
## -- End pasted text --
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
#27-29
index error, probs no value for topics
index error, probs no value for topics
index error, probs no value for topics
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
Poverty
something else going on
#41-48
index error, probs no value for topics
index error, probs no value for topics
index error, probs no value for topics
index error, probs no value for topics
index error, probs no value for topics
index error, probs no value for topics
index error, probs no value for topics
#49
Poverty
something else going on
###
#something else s up there are related to for loop error I think, cause
In [137]: jindi[1][1]['topics'][0]['value']
Out[137]: u'Poverty '

In [138]: jindi[1][0]['topics'][0]['value']
Out[138]: u'Poverty '

In [139]: jindi[1][2]['topics'][0]['value']
Out[139]: u'Poverty '

In [140]: jindi[1][3]['topics'][0]['value']
Out[140]: u'Poverty '

In [141]: jindi[1][4]['topics'][0]['value']
Out[141]: u'Poverty '

In [142]: jindi[1][5]['topics'][0]['value']
Out[142]: u'Poverty '

################
In [97]: print raw_jaysohn
[[{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2000', u'country': {u'id': u'BR', u'value': u'Brazil'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': None}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2001', u'country': {u'id': u'BR', u'value': u'Brazil'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'10.2004795074463'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2002', u'country': {u'id': u'BR', u'value': u'Brazil'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'8.87235355377197'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2007', u'country': {u'id': u'BR', u'value': u'Brazil'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'5.83593463897705'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2000', u'country': {u'id': u'BO', u'value': u'Bolivia'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'27.1525745391846'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2001', u'country': {u'id': u'BO', u'value': u'Bolivia'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'21.3751068115234'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2002', u'country': {u'id': u'BO', u'value': u'Bolivia'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'21.9765911102295'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2007', u'country': {u'id': u'BO', u'value': u'Bolivia'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'11.9812955856323'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2000', u'country': {u'id': u'EC', u'value': u'Ecuador'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'20.322135925293'}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2001', u'country': {u'id': u'EC', u'value': u'Ecuador'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': None}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2002', u'country': {u'id': u'EC', u'value': u'Ecuador'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': None}]],

 [{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1},
 [{u'date': u'2007', u'country': {u'id': u'EC', u'value': u'Ecuador'},
 u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'},
 u'decimal': u'0', u'value': u'6.94372797012329'}]]]

In [99]: print raw_jaysohn[0]
[{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1}, 
[{u'date': u'2000', u'country': {u'id': u'BR', u'value': u'Brazil'}, 
u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'}, 
u'decimal': u'0', u'value': None}]]

In [100]: print raw_jaysohn[2]
[{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1}, 
[{u'date': u'2002', u'country': {u'id': u'BR', u'value': u'Brazil'}, 
u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'}, 
u'decimal': u'0', u'value': u'8.87235355377197'}]]

In [101]: print raw_jaysohn[2][0]
{u'per_page': u'100', u'total': 1, u'page': 1, u'pages': 1}

In [102]: print raw_jaysohn[2][1]
[{u'date': u'2002', u'country': {u'id': u'BR', u'value': u'Brazil'}, 
u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'}, 
u'decimal': u'0', u'value': u'8.87235355377197'}]

In [105]: print raw_jaysohn[2][0]['per_page']
100

In [110]: print raw_jaysohn[2][1][0]
{u'date': u'2002', u'country': {u'id': u'BR', u'value': u'Brazil'}, 
u'indicator': {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'}, 
u'decimal': u'0', u'value': u'8.87235355377197'}

In [112]: hurr= raw_jaysohn[2][1][0]

In [113]: %paste
for llave in hurr:
   ....:     print "yave: %s, val: %s" % (llave, hurr[llave])

## -- End pasted text --
yave: date, val: 2002
yave: country, val: {u'id': u'BR', u'value': u'Brazil'}
yave: indicator, val: {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'}
yave: decimal, val: 0
yave: value, val: 8.87235355377197
#...
In [32]: print raw_jaysohn[0][1][0]['country']['value']
Brazil

In [33]: print raw_jaysohn[0][1][0]['country']['id']
BR

In [34]: print raw_jaysohn[0][1][0]['indicator']['value']
Poverty Headcount ($1.25 a day)

In [35]: print raw_jaysohn[0][1][0]['indicator']['id']
1.0.HCount.1.25usd

In [50]: ob= raw_jaysohn[0][1][0]

In [51]: df_ob=pd.DataFrame(ob)

In [52]: print df_ob
      country  date decimal                        indicator value
id         BR  2000       0               1.0.HCount.1.25usd  None
value  Brazil  2000       0  Poverty Headcount ($1.25 a day)  None

In [61]: va_df_ob=df_ob[df_ob.index=='value']

In [62]: print va_df_ob
      country  date decimal                        indicator value
value  Brazil  2000       0  Poverty Headcount ($1.25 a day)  None
#whats not clear is why ID and value are the default index, but Ill take the win!
#
In [63]: raw_jaysohn[0][1][1]
#...
IndexError: list index out of range
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#####################basic derping without bartender, old
In [15]: herp=pagina.json()

In [16]: type(herp)
Out[16]: list
In [21]: pagina.json()
Out[21]:
[{u'page': 1, u'pages': 1, u'per_page': u'100', u'total': 14},
 [{u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2013',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'4.16071319580078'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2012',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'3.75249171257019'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2011',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'4.53084993362427'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2010',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': None},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2009',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'4.72176885604858'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2008',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'4.8712592124939'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2007',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'5.83593463897705'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2006',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'5.95988702774048'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2005',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'7.17596483230591'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2004',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'8.13587665557861'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2003',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'9.63104438781738'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2002',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'8.87235355377197'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2001',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': u'10.2004795074463'},
  {u'country': {u'id': u'BR', u'value': u'Brazil'},
   u'date': u'2000',
   u'decimal': u'0',
   u'indicator': {u'id': u'1.0.HCount.1.25usd',
    u'value': u'Poverty Headcount ($1.25 a day)'},
   u'value': None}]]

In [45]: herp[0]
Out[45]: {u'page': 1, u'pages': 1, u'per_page': u'100', u'total': 14}

In [49]: herp[1][1]
Out[49]:
{u'country': {u'id': u'BR', u'value': u'Brazil'},
 u'date': u'2012',
 u'decimal': u'0',
 u'indicator': {u'id': u'1.0.HCount.1.25usd',
  u'value': u'Poverty Headcount ($1.25 a day)'},
 u'value': u'3.75249171257019'}

In [64]: type(herp)
Out[64]: list

In [52]: type(herp[1])
Out[52]: list

In [51]: type(herp[1][1])
Out[51]: dict
\herp[1][1] = hurr
In [57]: hurr["country"]
Out[57]: {u'id': u'BR', u'value': u'Brazil'}
In [58]: type(hurr["country"])
Out[58]: dict

In [61]: for llave in hurr:
   ....:     print "yave: %s, val: %s" % (llave, hurr[llave])
   ....:
yave: date, val: 2012
yave: country, val: {u'id': u'BR', u'value': u'Brazil'}
yave: indicator, val: {u'id': u'1.0.HCount.1.25usd', u'value': u'Poverty Headcount ($1.25 a day)'}
yave: decimal, val: 0
yave: value, val: 3.75249171257019

In [73]: type(hurr["country"])
Out[73]: dict
In [75]: print(hurr["country"]["value"])
Brazil

In [65]: dhurr = pd.DataFrame(hurr)
In [66]: print(dhurr)
#notice our keys are now columns. COOOL!!!!
      country  date decimal                        indicator             value
id         BR  2012       0               1.0.HCount.1.25usd  3.75249171257019
value  Brazil  2012       0  Poverty Headcount ($1.25 a day)  3.75249171257019

In [67]: hurr2=herp[1][2]

In [69]: dhurr2 = pd.DataFrame(hurr2)

In [70]: dhurr.append(dhurr2)
Out[70]:
      country  date decimal                        indicator             value
id         BR  2012       0               1.0.HCount.1.25usd  3.75249171257019
value  Brazil  2012       0  Poverty Headcount ($1.25 a day)  3.75249171257019
id         BR  2011       0               1.0.HCount.1.25usd  4.53084993362427
value  Brazil  2011       0  Poverty Headcount ($1.25 a day)  4.53084993362427


#########trying some stuff
 BRA_df=pd.DataFrame(BRA_jaysohn)