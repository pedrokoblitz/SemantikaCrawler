#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import sys, urlparse, urllib, time, re, simplejson, socket, datetime
from pattern.web import URL, find_urls, HTTPError, URLError

# =====================================================================  
# ALEXA
# =====================================================================  
class Alexa(object):

	def __init__(self,url):
		self.url = url

	def busca(self):
		apiurl = 'http://data.alexa.com/data?cli=10&dat=snbamz&url='
		queryurl = apiurl + self.url
		try:
		  return URL(queryurl).download()
		except:
		  pass

	def formata(self):
		dados = self.busca()
		if dados:
			raiz = etree.parse(self.dados)
			return raiz
