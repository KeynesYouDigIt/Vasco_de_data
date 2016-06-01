###gets josn 1/5!!!!!
import web
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
		main_dir='C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub'
		durr=os.listdir(main_dir)
		while 'C_Y_order.json' not in durr:
			durr=os.listdir(main_dir)
		execfile('C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub\\bin\\pyhostess_Avail_get.py')
		durr=os.listdir(main_dir)
		while 'availibility.json' not in durr:
			durr=os.listdir(main_dir)
		with open('availibility.json','r') as fp:
			global order
			order=fp.read()
		return render.Bar(order_html = order)

if __name__ == "__main__":
	app.run()

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
		main_dir='C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub'
		durr=os.listdir(main_dir)
		while 'C_Y_order.json' not in durr:
			durr=os.listdir(main_dir)
		execfile('C:\Users\Vince\Google Drive\PeacefulMandE\pubdatapub\\bin\\pyhostess_Avail_get.py')
		durr=os.listdir(main_dir)
		while 'availibility.json' not in durr:
			durr=os.listdir(main_dir)
		with open('availibility.json','r') as fp:
			global order
			order=fp.read()
		return render.Bar(order_html = order)

if __name__ == "__main__":
	app.run()