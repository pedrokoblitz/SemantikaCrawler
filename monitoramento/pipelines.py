# Copyright 2011 Julien Duponchelle <julien@duponchelle.info>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MongoDB Pipeline for scrappy"""

import os, time, datetime
import os.path
from pymongo import Connection
from pymongo.timestamp import Timestamp
from scrapy.conf import settings
from scrapy import log
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from nltk.tokenize import WordPunctTokenizer
from urlparse import urlparse

class Lexico(object):

	def contar_palavras(self,texto):
		txt = WordPunctTokenizer().tokenize(texto)
		return len(txt)
	
	def contar_palavras_unicas(self,texto):
		txt = WordPunctTokenizer().tokenize(texto)
		return len(set(texto))

	def process_item(self,item,spider):
		item['palavras'] = self.contar_palavras(item['texto'])
		item['vocabulario'] = self.contar_palavras_unicas(item['texto'])
		return item

# ========================

class ContadorUrls(object):
	def __init__(self):
		self.urls = {}
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		connection = Connection()
		db = connection.aranha
		collection = self.db.urlsVisitadas
		collection.insert(self.urls)
		del self.urls[spider]

	def process_item(self, item, spider):
		self.urls[spider].add(item['url'])
		return item	

# ========================

class LimparCurtos(object):
	def process_item(self, item, spider):
		if item['palavras'] < 40:
			raise DropItem("Muito curto: %s" % item)
		return item			

# ========================

class LimparCapas(object):
	def process_item(self, item, spider):
		parsed_url = urlparse(item['url'])
		if parsed_url.path == '' and parsed_url.query == '' and parsed_url.params == '':
			raise DropItem("Capa: %s" % item)
		return item			
		
# ========================

class Repetidas(object):
	def __init__(self):
		self.repetidas = {}
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_opened(self, spider):
		self.repetidas[spider] = set()

	def spider_closed(self, spider):
		del self.repetidas[spider]

	def process_item(self, item, spider):
		if item['texto'] in self.repetidas[spider]:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.repetidas[spider].add(item['texto'])
		return item			

# ========================

class MongoStore(object):

	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		self.connection = Connection()
		self.db = self.connection.aranha
		self.varreduras = self.db.varreduras
		self.paginas = self.db.paginas

	def spider_opened(self, spider):
		self.data = (datetime.datetime.today())
		self.varredura_id = str(self.varreduras.insert({'data':self.data, 'tipo':spider.name}))

	def process_item(self, item, spider):
		item['varredura'] = unicode(self.varredura_id)
		item['data'] = self.data
		self.paginas.insert(dict(item)) 
		return item







