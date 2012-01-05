#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import sys, urlparse, urllib, time, re, simplejson, socket, datetime
from pattern.web import URL, find_urls, HTTPError, URLError

# =====================================================================  
# TOPSY
# =====================================================================  

class Topsy(object):

	def __init__(self, query):
	  self.query = query

 # =====================================================================  
 # buscar no topsy
 # =====================================================================  

	def busca_topsy(self, service):
	  apiurl = 'http://otter.topsy.com/'
	  queryurl = apiurl + service + '.json?' + self.query
	  try:
	    search_results = URL(queryurl).download()
	    json = simplejson.loads(search_results)
	    resultados = json['response']
	    return resultados
	  except:
	    pass

	# =====================================================================  
	# retorna perfil do autor ou site
	# =====================================================================
 
	def authorinfo(self):
	  url = self.query
	  self.query = urllib.urlencode({'url': self.query})
	  resultados = self.busca('authorinfo')
	  perfil = {}
	  perfil['url'] = url
	  perfil['nome'] = resultados['name']
	  perfil['descricao'] = resultados['description']
	  perfil['influencia'] = resultados['influence_level']    
	  return perfil

	# =====================================================================  
	# TEM DE FORMATAR ESSES RESULTADOS
	# tweets mencionando o site 
	# =====================================================================  

	def trackbacks(self):
		querybak = self.query
		self.query = urllib.urlencode({'url': querybak})
		resultados = self.busca('trackbacks')
		return resultados

