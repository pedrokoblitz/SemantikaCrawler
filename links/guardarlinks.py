#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from pymongo import Connection
from extratores.url import ExtratorUrl

class Extracao(object):

  def __init__(self, urls, db):
    self.coll = db
    self.urls = urls

  def guardar_links(self):
		dados = []
		for url in self.urls:
			dado = {}
			dado['url'] = url
			dados.append(dado)
		print self.coll.linksCache.insert(dados)

produtos = Connection().termos.termos.find({'tipo':{'$regex':'produtos|buscas'}})

urls = []
db = Connection().extratorUrls

db.linksCache.drop()

for produto in produtos:
	extrator = ExtratorUrl(termo=produto['termo'].lower().encode('utf-8'),url='http://embelleze.com')
	urls += extrator.gerar_urls_topsy('m')
	urls += extrator.gerar_urls_gblogs()
	urls += extrator.gerar_urls_gweb()
	urls += extrator.gerar_urls_gnews()
	urls += extrator.gerar_urls_twitter()
#	urls += extrator.gerar_urls_relacionadas()

	busca = Extracao(urls, db) 
	busca.guardar_links()
	urls = []

