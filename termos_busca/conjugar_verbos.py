#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pattern.web import URL, plaintext
from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer

  	

tokenizer = RegexpTokenizer('\w+')
stemmer = RSLPStemmer()

verbos = tokenizer.tokenize(open('verbos','rb').read())

radicais = []
resultados = []

for verbo in verbos:
	radical = stemmer.stem(verbo)
	radicais.append(radical)

for verbo in verbos:
	pg = URL('http://linguistica.insite.com.br/mod_perl/conjugue?verbo='+verbo).download()
	palavras = tokenizer.tokenize(pg)
	for palavra in palavras:
		radical = stemmer.stem(palavra)
		if radical in radicais:
			if palavra not in resultados:
				print palavra.encode('utf-8')
			resultados.append(palavra)
