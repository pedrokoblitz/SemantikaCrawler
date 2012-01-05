#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from pymongo import Connection
from nltk.stem import RSLPStemmer

stemmer = RSLPStemmer()


db = Connection().termos
a = open(sys.argv[1],'r').read().split('\n')
for x in a:
	if x != '':
		x = x.decode('utf-8')
		print db['termos'].insert({'termo':x,'stem':stemmer.stem(x),'tipo':sys.argv[1]})

