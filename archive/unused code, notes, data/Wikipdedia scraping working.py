#Data Derping ISO codes
import bs4
from bs4 import BeautifulSoup

In [105]: countryCode = BS.find_all('span', style='font-family: monospace, monospace;')

In [106]: type(countryCode)
Out[106]: bs4.element.ResultSet

In [107]: print(countryCode)

[<span style="font-family: monospace, monospace;">ABW</span>,
<span style="font-family: monospace, monospace;">AFG</span>,
<span style="font-family: monospace, monospace;">AGO</span>,
<span style="font-family: monospace, monospace;">AIA</span>,
<span style="font-family: monospace, monospace;">ALA</span>,
<span style="font-family: monospace, monospace;">ALB</span>,
<span style="font-family: monospace, monospace;">AND</span>,
<span style="font-family: monospace, monospace;">ARE</span>,
<span style="font-family: monospace, monospace;">ARG</span>,
<span style="font-family: monospace, monospace;">ARM</span>,
<span style="font-family: monospace, monospace;">ASM</span>,
<span style="font-family: monospace, monospace;">ATA</span>,
<span style="font-family: monospace, monospace;">ATF</span>,
<span style="font-family: monospace, monospace;">ATG</span>,
<span style="font-family: monospace, monospace;">AUS</span>,
<span style="font-family: monospace, monospace;">AUT</span>,
<span style="font-family: monospace, monospace;">AZE</span>,
<span style="font-family: monospace, monospace;">BDI</span>,
<span style="font-family: monospace, monospace;">BEL</span>,
<span style="font-family: monospace, monospace;">BEN</span>,
<span style="font-family: monospace, monospace;">BES</span>,
<span style="font-family: monospace, monospace;">BFA</span>,
<span style="font-family: monospace, monospace;">BGD</span>,
<span style="font-family: monospace, monospace;">BGR</span>,
<span style="font-family: monospace, monospace;">BHR</span>,
<span style="font-family: monospace, monospace;">BHS</s
#appended and edited for clarity ...
#
#Span missing countries, so lets start with these bad boys - there are 3 of these all containing data we want
#<table style="background:transparent;"
In [105]: countryCodeTables = BS.find_all('table', style='background:transparent;')

get=[]
for i in countryCodeTables: 
	it=i.find('td')
	get.append(it)

gett=[]
for i in get[0]:
	it=i.find('td')
	gett.append(it)

In [148]: type(get[0])
Out[148]: bs4.element.Tag
#with 1/3 tables of content...

the_d=[]
for i in get[0]: 
	it=i.find('span', style='font-family: monospace, monospace;').string
	print it
	#the_d.append(it)
ABW
ABW
GIB
NLD
#using the above for loob I can cal find, skipping nones according to the boolean below
In [225]: tds_in_tds[1] == None
Out[225]: True

tds=BS.find_all('td')
spans=BS.find_all('span')


###from dox
#AttributeError: 'ResultSet' object has no attribute 'foo' - This usually happens because you expected find_all() 
#to return a single tag or string. But find_all() returns a _list_ of tags and strings–a ResultSet object. 
#You need to iterate over the list and look at the .foo of each one. Or, if you really only want one result, you need to use find() instead of find_all().
###
#belowgets the tob of each list
get=[]
for i in countryCodeTables: 
	it=i.find('span', style='font-family: monospace, monospace;')
	get.append(it)
In [122]: print get
[<span style="font-family: monospace, monospace;">ABW</span>, <span style="font-family: monospace, monospace;">ABW</span>, <span style="font-family: monospace, monospace;">GIB</span>, <span style="font-family: monospace, monospace;">NLD</span>]

s_spans=[]
for i in spans:
	it=i.string
	s_spans.append(it)

codes =[]
for i in s_spans:
	if i == None:
		print 'nyan'
	else:
		s_len =len(i)
		if s_len == 3:
			codes.append(i)
		else:
			print 'looooser'

ahrefs=BS.find_all('a')
s_ahrefs=[]
for i in ahrefs:
	itr=i.string
	s_ahrefs.append(itr)

countries=[]
for i in s_ahrefs:
	if i == None:
		print 'nyan'
	else:
		countries.append(i)
######################################################################
######################################################################
#below works!!!
html = urlopen('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3').read()
BS = BeautifulSoup(html, "lxml")
tds=BS.find_all('td')

herp_it = []
it=-1
for d in tds:
	it += 1
	herp_it.append(it)
herp_it = np.asarray(herp_it)

final_dic={}

for t in herp_it:
	s_td=tds[t].string
	if s_td == None:
		one
	else:
		l_s_td=len(s_td)
		nxt = t + 1
		if l_s_td == 3:
			final_dic.update({s_td:tds[nxt].string})
		else:
			hurr = 'nota code'

