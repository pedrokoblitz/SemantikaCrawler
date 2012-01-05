#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import sys, urlparse, urllib, time, re, simplejson, socket, datetime
from pattern.web import URL, find_urls, HTTPError, URLError




class BuscaTwitter (object):

  def __init__(self,busca):
    self.busca = busca
    

  # =====================================================================  
  # TWITTER
  # recebe termo da busca string, tweets por pagina int, pagina int
  # =====================================================================  

  def busca_twitter(self, tpp=100,p=1):
    query = urllib.urlencode({'q': self.busca, 'rpp': tpp, 'page': p, 'lang':'pt'})
    apiurl = 'http://search.twitter.com/search.json?'
    queryurl = apiurl + query
    try:
      search_results = URL(queryurl).download()
      json = simplejson.loads(search_results)
      results = json['results']
      return results
    except:
      print 'busca do twitter retornou vazia'
      pass
    
  def formata_twitter(self, results):
    tweets = []
    i = 0
    for t in results:
      i += 1
      try:
        lingua = t['iso_language_code']
      except KeyError:
        lingua = ''
      tweet = {'autor': t['from_user'], 'data' : t['created_at'], 'texto' : t['text'], 'lingua' : lingua}
      tweets.append(tweet)
    return tweets

