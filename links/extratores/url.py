#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import sys, urlparse, urllib, time, re, simplejson, socket, datetime
from pattern.web import URL, find_urls, HTTPError, URLError

from util import *
from apis.twitter import BuscaTwitter
from apis.google import BuscaGoogle
from apis.topsy import Topsy

# ===================================================================== 
# EXTRATORES
# retiram informaçoes das apis de busca
# ===================================================================== 

class ExtratorUrl (object):

  def __init__(self, timer=5, termo=None, url=None):
    # global! tempo de espera em segundos entre reqs das apis
    self.timer = timer
    self.termo = termo
    self.url = url

  # =====================================================================  
  # busca de links do twitter
  # apenas tweets com links
  # =====================================================================  

  def gerar_urls_twitter(self, loops=2):
    if loops < 2:
      print 'pelo menos 2'
      pass    
    urlsBase = []
    t = 1
    tweets = ''
    while t < loops:
      twitter = BuscaTwitter(self.termo)
      buscatwitter = twitter.formata_twitter(twitter.busca_twitter(tpp=100, p=t))
      if buscatwitter:
        for tweet in buscatwitter:
          tweets += ' ' + tweet['texto']
      else:
        pass
      t += 1
      time.sleep(self.timer)
    urlsBase = find_urls(tweets)
    print '%s links encontrados no Twitter para %s' % (len(urlsBase),self.termo)
    return urlsBase

  # =====================================================================  
  # retorna lista de links por dominio no topsy
  # =====================================================================  

  def gerar_urls_topsy(self, tempo='d'):
    query = urllib.urlencode({'q': 'site:' + self.url, 'window': tempo})
    topsy = Topsy(query)
    resultados = topsy.busca_topsy('search')
    try:
      lista = resultados['list']
      links = []
      for item in lista:
        links.append(item['url'])
      print '%s links encontrados no topsy para %s' % (len(links),self.termo)
      return links
    except TypeError:
      pass
      
      
  # ===================================================================== 
  # retira urls da busca google web 
  # =====================================================================  

  def gerar_urls_gweb(self, loops=2):  
    urlsBase = []
    i = 0
    google = BuscaGoogle(self.termo)
    while i < (loops*8)+1:
      try:
        results = google.formata_gweb(google.busca_google('web',inicio=i,quant=i+7))
        if results != None:
          for item in results:
            if item['url'] not in urlsBase:
              urlsBase.append(item['url']) 
        else:
          pass
      except:
        pass
      i += 8
      time.sleep(self.timer)
    print '%s links encontrados no Google para %s' % (len(urlsBase),self.termo)
    return urlsBase

  # ===================================================================== 
  # retira urls da busca google news
  # =====================================================================  

  def gerar_urls_gnews(self, loops=2):  
    urlsBase = []
    i = 0
    google = BuscaGoogle(self.termo)
    while i < (loops*8)+1:
      try:
        results = google.formata_gnews(google.busca_google('news', inicio=i,quant=i+7), achatar=True)
        if results != None:
          for item in results:
            if item['url'] not in urlsBase:
              urlsBase.append(item['url']) 
        else:
          pass
      except:
        pass
      i += 8
      time.sleep(self.timer)
    print '%s links encontrados no Google News para %s' % (len(urlsBase),self.termo)
    return urlsBase

  # ===================================================================== 
  # retira urls da busca google blogs
  # =====================================================================  

  def gerar_urls_gblogs(self, loops=2):  
    urlsBase = []
    i = 0
    google = BuscaGoogle(self.termo)
    while i < (loops*8)+1:
      try:
        results = google.formata_gblogs(google.busca_google('blogs',inicio=i,quant=i+7))
        if results != None:
          for item in results:
            if item['url'] not in urlsBase:
              urlsBase.append(item['url']) 
        else:
          pass
      except:
        pass
      i += 8
      time.sleep(self.timer)
    print '%s links encontrados no Google News para %s' % (len(urlsBase),self.termo)
    return urlsBase

  # ===================================================================== 
  # busca sites relacionados a url no google
  # busca termo em sites relacionados + original via google
  # ===================================================================== 

  def gerar_urls_relacionadas(self):
    dominio = tirar_dominio(self.url)
    termobak = self.termo
    self.termo = 'related:' + dominio
    sites = self.gerar_urls_gweb()
    urlsBase = [self.url]
    for u in sites:
      dominio = tirar_dominio(u)
      self.termo = termobak + ' site:' + dominio
      urls_extras = self.gerar_urls_gweb()
      urlsBase += urls_extras
      time.sleep(self.timer)
    print '%s links relacionados encontrados no Google para %s em %s' % (len(urlsBase),self.termo,self.url)
    self.termo = termobak
    return urlsBase
    
    
