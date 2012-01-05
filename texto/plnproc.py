#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, time, datetime
from lingprocessador import Texto, Ngrama, Classificador
from pymongo import Connection
from pymongo.timestamp import Timestamp
from nltk.tokenize import RegexpTokenizer



def txt_pgs(pgs):
	def extrair_texto(obj):
		return obj['texto']	
	def limpar_curtas(obj):
		if int(obj['palavras']) < 40:
			return False
		else:
			return True
	def limpar_vazias(obj):
		if obj['texto'] == '' or obj['titulo'] == '':
			return False
		else:
			return True
	t0 = filter(limpar_curtas,pgs)
	t1 = filter(limpar_vazias,t0)
	t2 = map(extrair_texto,t1)
	texto = Texto(unicode(''.join(t2)))
	return texto

def carregar_ngramas(texto):
	texto.set_palavras()
	ngrama = Ngrama(texto.palavras)
	return ngrama

def guardar_bigramas(coll,ngrama):
	ngrama.set_bigramas(freq=3,best=100)
	bgs = ngrama.bigramas
	if bgs:
		for bg in bgs:
			termo = ' '.join(bg).encode('utf-8')
			print coll.insert(
				{
					'termo':termo.lower(),
					'ngrama':2,
					'data':datetime.datetime.today()
				}
			)
		
def guardar_trigramas(coll,ngrama):
	tgs = ngrama.set_trigramas(freq=2,best=100)
	if tgs:
		for tg in tgs:
			termo = ' '.join(tg).encode('utf-8')
			print coll.insert(
				{
					'termo':termo.lower(),
					'ngrama':3,
					'data':datetime.datetime.today()
				}
			)

def guardar_similares(coll,texto,alvo):
	similares = texto.similar(alvo)
	if similares:
		for i in similares:
			similar = i.encode('utf-8')
			print coll.insert(
				{
					'termo':similar.lower(),
					'alvo':alvo.lower(),
					'data':datetime.datetime.today()
				}
			)
		

def guardar_contextos(coll,texto,alvo):
	contextos = texto.concordance(alvo.lower(),width=70, lines=1000)
	if contextos:
		for i in contextos:
			contexto = i.encode('utf-8')
			print coll.insert(
				{
					'contexto':contexto,
					'alvo':alvo.lower(),
					'data':datetime.datetime.today()
				}
			)

def main():
	conn = Connection()
	buscas = conn.termos.termos.find({'tipo':{'$regex':'verbos_conjugados|buscas'}})
	alvos = conn.termos.termos.find({'tipo':{'$regex':'produtos|alvos'}})
	pln = conn.pln
	contextos_coll = pln.contextos
	similares_coll = pln.similares
	ngramas_coll = pln.ngramas
	tags_coll = pln.tags
	classificador = Classificador()
	pgs = []		
	tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')
	for busca in buscas:
		for pg in conn.aranha.paginas.find({'texto':{'$regex':busca['termo']}}):
			if pg not in pgs:
				pgs.append(pg)
				frases = tokenizer.tokenize(pg['texto'])
				classificador.classificar(frases)
				for i in classificador.texto_classificado:
					tags_coll.insert(
						{
#							'pgid':pg['_id'],
							'termo':i[0],
							'classe':i[1],
							'data': datetime.datetime.today()
						}
					)

	texto = txt_pgs(pgs)
	ngrama = carregar_ngramas(texto)
	
	guardar_bigramas(ngramas_coll,ngrama)
	guardar_trigramas(ngramas_coll,ngrama)
	
	for alvo in alvos:
		guardar_contextos(contextos_coll,texto,alvo['termo'])
		guardar_similares(similares_coll,texto,alvo['termo'])
		
if __name__ == '__main__':
	main()

