#!/usr/bin/env python
#-*- coding:utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from monitoramento.items import Pagina
import justext
from pymongo import Connection
from nltk.tokenize import WordPunctTokenizer


class Generica(BaseSpider):
	name = 'generica'
	allowed_domains = []
	start_urls = []
	db = Connection().extratorUrls

	def __init__(self, **kwargs):
		self.start_urls = self.setUrls()

	def setUrls(self):
		urls = []
		for link in self.db.linksCache.find():
			if link.has_key('url'):
				urls.append(link['url'])
		return urls

	def contar_palavras(self,texto):
		txt = WordPunctTokenizer().tokenize(texto)
		return len(txt)
	
	def contar_palavras_unicas(self,texto):
		txt = WordPunctTokenizer().tokenize(texto)
		return len(set(texto))

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titulo = hxs.select('/html/head/title/text()').extract()
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
		item['palavras'] = self.contar_palavras(item['texto'])
		item['vocabulario'] = self.contar_palavras_unicas(item['texto'])
		
		return item
		
		
		
