#!/usr/bin/env python
#-*- coding:utf-8 -*-

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst
from scrapy.utils.markup import remove_entities

def limpar_texto(self,texto):
	return texto.replace('\t', '').replace('\n', '').strip()
		
class Pagina(Item):
	url = Field(
		output_processor=Join()
	)
	titulo = Field(default=u'título não disponível')
	texto = Field(
		default=u'texto não disponível',
		input_processor=MapCompose(limpar_texto, remove_entities)
	)
	varredura = Field()
	data = Field()
	tipo = Field()
	palavras = Field()
	vocabulario = Field()
	
	
	
