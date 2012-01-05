#!/usr/bin/env python
#-*- coding:utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy import log # This module is useful for printing out debug information
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from monitoramento.items import Pagina
import justext
from pymongo import Connection
from urlparse import urlparse

class Parceiros(CrawlSpider):
	name = 'parceiros'
	allowed_domains = []
	start_urls = []
	conn = Connection()
	db = conn.extratorUrls

	def __init__(self, **kwargs):
		self.allowed_domains = self.setDomains()
		self.start_urls = self.setUrls()

	def setDomains(self):
		dominios = []
		for link in self.db.blogsParceiros.find():
			if link.has_key('url'):
				dominio = urlparse(link['url'])
				dominios.append(dominio.netloc)
		return dominios

	def setUrls(self):
		urls = []
		for link in self.db.blogsParceiros.find():
			if link.has_key('url'):
				urls.append(link['url'])
		return urls


	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titulo = hxs.select('/html/head/title/text()').extract()
		rules = (Rule(SgmlLinkExtractor(allow='.*'),follow=True,callback='parse'))
		corpo = justext.justext(response.body, justext.get_stoplist('Portuguese'))
		texto = ''
		for paragrafo in corpo:
			if paragrafo['class'] == 'good':
				texto += paragrafo['text']
		item = Pagina()
		item['url'] = response.url
		item['titulo'] = unicode(titulo[0])
		item['texto'] = unicode(texto)
		item['tipo'] = self.name
		return item
		
		
		
