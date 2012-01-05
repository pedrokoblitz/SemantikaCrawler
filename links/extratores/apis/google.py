#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import sys, urlparse, urllib, time, re, simplejson, socket, datetime
from pattern.web import URL, find_urls, HTTPError, URLError


class BuscaGoogle (object):

  def __init__(self, termo):
    self.termo = termo

  # =====================================================================  
  # GOOGLE
  # =====================================================================  

  def busca_google(self, service, versao='1.0', inicio=0, quant=8, lingua='pt_br', ip=None):
    if not ip:
      ip = socket.gethostbyname(socket.gethostname())
    query = urllib.urlencode({'v' : versao, 'start' : str(inicio), 'rsz' : str(quant), 'hl': lingua, 'q' : self.termo, 'userip':ip})
    apiurl = "http://ajax.googleapis.com/ajax/services/search/"
    queryurl = apiurl + service +'?' + query
    try:
      search_results = URL(queryurl).download()
      json = simplejson.loads(search_results)
      results = json['responseData']['results']
      return results
    except (TypeError, URLError):
      print 'erro para a busca Google',service,self.termo
      pass
      
  # =====================================================================  
  # recebe resultados (string) e devolve resultados (lista de dicionarios)
  # formatados para a busca_google
  # Google Web
  # =====================================================================  
      
  def formata_gweb(self, results):
    web = []
    if results:
      for r in results:
        item = {'titulo' : r['titleNoFormatting'],'url' : r['unescapedUrl'], 'conteudo' : r['content']}
        web.append(item)
    return web

  # =====================================================================  
  # recebe termo (string) e devolve resultados (lista de dicionarios) formatados para a busca_google
  # Google Blogs
  # =====================================================================  

  def formata_gblogs(self, results):
    blogs = []
    for r in results:
      item = {'blog' : r['blogUrl'], 'autor' : r['author'], 'data' : r['publishedDate'], 'titulo' : r['titleNoFormatting'], 'conteudo' : r['content'], 'url' : r['postUrl']}
      blogs.append(item)
    return blogs

  # =====================================================================  
  # recebe termo (string) e devolve resultados (lista de dicionarios) formatados para a busca_google
  # Google News
  # =====================================================================  

  def formata_gnews(self, results, achatar=False):
    news  = []
    for r in results:
      noticia = {}
      if 'publisher' in r:  
        noticia['fonte'] = r['publisher']
      noticia['titulo'] = r['titleNoFormatting']
      if 'publishedDate' in r:  
        noticia['data'] = r['publishedDate']
      noticia['url'] = r['unescapedUrl']
      if 'relatedStories' in r:
        relacionadas = []
        for rr in r['relatedStories']:
          relacionada = {}
          if 'publisher' in r:  
            relacionada['fonte'] = rr['publisher']
          relacionada['titulo'] = rr['titleNoFormatting']
          if 'publishedDate' in r:  
            relacionada['data'] = rr['publishedDate']
          relacionada['url'] = rr['unescapedUrl']
          if achatar == True:
            news.append(relacionada)
          else:
            relacionadas.append(relacionada)
        if achatar == False:
          noticia['relacionadas'] = relacionadas
          news.append(noticia)      
      return news

