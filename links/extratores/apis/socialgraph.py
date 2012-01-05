#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import sys, urlparse, urllib, time, re, simplejson, socket, datetime
from pattern.web import URL, find_urls, HTTPError, URLError


class SocialGraph (object):

  def __init__(self, urls):
    self.urls = ','.join(urls)

  # =====================================================================  
  # SOCIAL GRAPH
  # nodes_referenced = quem o perfil segue
  # nodes_referenced_by = quem segue o perfil
  # pode receber urls separadas por virgula
  # =====================================================================  

  # =====================================================================  
  # socialgraph otherme
  # http://code.google.com/intl/pt-BR/apis/socialgraph/docs/otherme.html
  # =====================================================================  

  def busca(self, service, query):
    apiurl = 'https://socialgraph.googleapis.com/'
    queryurl = apiurl + service + '?' + query
    try:
      search_results = URL(queryurl).download()
      results = simplejson.loads(search_results)
      return results
    except:
        print 'erro socialgraph'  

  # ===================================================================== 
  # otherme
  # ===================================================================== 

  def otherme(self):
    query = urllib.urlencode({'q': self.urls})
    results = self.busca('otherme', query)
    if results:
      return results.keys()
    else:
      print 'erro sg_otherme'  



  # ===================================================================== 
  # seguidores
  # ===================================================================== 

  def seguidores(self):
    query = urllib.urlencode({'q': self.urls, 'edi': 'true', 'edo': 'true'})
    results = self.busca('lookup', query)
    if results:
      nodes = results['nodes'].keys()
      seguido = []
      for node in nodes:
        item = results['nodes'][node]
        seguido.append(item['nodes_referenced_by'].keys())
      return seguido
    else:
      print 'erro sg_seguidores' 
