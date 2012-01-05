#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-
from math import log
import nltk,re

from nltk.probability import FreqDist, LidstoneProbDist
from nltk.probability import ConditionalFreqDist as CFD
from nltk.compat import defaultdict
from nltk.model import NgramModel
from nltk.metrics import f_measure, BigramAssocMeasures, TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.corpus import mac_morpho

# =======================		
# ADAPTADA DO NLTK
# =======================		

class ContextIndex(object):
    """
    A bidirectional index between words and their 'contexts' in a text.
    The context of a word is usually defined to be the words that occur
    in a fixed window around the word; but other definitions may also
    be used by providing a custom context function.
    """
    @staticmethod
    def _default_context(tokens, i):
        """One left token and one right token, normalized to lowercase"""
        if i == 0: left = '*START*'
        else: left = tokens[i-1].lower()
        if i == len(tokens) - 1: right = '*END*'
        else: right = tokens[i+1].lower()
        return (left, right)
        
    def __init__(self, tokens, context_func=None, filter=None, key=lambda x:x):
        self._key = key
        self._tokens = tokens
        if not context_func:
            self._context_func = self._default_context
        if filter:
            tokens = [t for t in tokens if filter(t)]
        self._word_to_contexts = CFD((self._key(w), self._context_func(tokens, i))
                                     for i, w in enumerate(tokens))
        self._context_to_words = CFD((self._context_func(tokens, i), self._key(w))
                                     for i, w in enumerate(tokens))

    def tokens(self):
        """
        @rtype: C{list} of token
        @return: The document that this context index was
            created from.  
        """
        return self._tokens

    def word_similarity_dict(self, word):
        """
        Return a dictionary mapping from words to 'similarity scores,'
        indicating how often these two words occur in the same
        context.  
        """
        word = self._key(word)
        word_contexts = set(self._word_to_contexts[word])

        scores = {}
        for w, w_contexts in self._word_to_contexts.items():
            scores[w] = f_measure(word_contexts, set(w_contexts))

        return scores

    def similar_words(self, word, n=20):
        scores = defaultdict(int)
        for c in self._word_to_contexts[self._key(word)]:
            for w in self._context_to_words[c]:
                if w != word:
                    print w, c, self._context_to_words[c][word], self._context_to_words[c][w]  
                    scores[w] += self._context_to_words[c][word] * self._context_to_words[c][w]  
        return sorted(scores, key=scores.get)[:n]

    def common_contexts(self, words, fail_on_unknown=False):
        """
        Find contexts where the specified words can all appear; and
        return a frequency distribution mapping each context to the
        number of times that context was used.
        
        @param words: The words used to seed the similarity search
        @type words: C{str} 
        @param fail_on_unknown: If true, then raise a value error if
            any of the given words do not occur at all in the index.
        """
        words = [self._key(w) for w in words]
        contexts = [set(self._word_to_contexts[w]) for w in words]
        empty = [words[i] for i in range(len(words)) if not contexts[i]]
        common = reduce(set.intersection, contexts)
        if empty and fail_on_unknown:
            raise ValueError("The following word(s) were not found:",
                             " ".join(words))
        elif not common:
            # nothing in common -- just return an empty freqdist.
            return FreqDist()
        else:
            fd = FreqDist(c for w in words
                          for c in self._word_to_contexts[w]
                          if c in common)
            return fd

		
# =======================		
# ADAPTADA DO NLTK
# =======================		

class ConcordanceIndex(object):
    """
    An index that can be used to look up the offset locations at which
    a given word occurs in a document.
    """
    def __init__(self, tokens, key=lambda x:x):
        """
        Construct a new concordance index.

        @param tokens: The document (list of tokens) that this
            concordance index was created from.  This list can be used
            to access the context of a given word occurance.
        @param key: A function that maps each token to a normalized
            version that will be used as a key in the index.  E.g., if
            you use C{key=lambda s:s.lower()}, then the index will be
            case-insensitive.
        """
        self._tokens = tokens
        """The document (list of tokens) that this concordance index
           was created from."""
        
        self._key = key
        """Function mapping each token to an index key (or None)."""
        
        self._offsets = defaultdict(list)
        """Dictionary mapping words (or keys) to lists of offset
           indices."""
        
        # Initialize the index (self._offsets)
        for index, word in enumerate(tokens):
            word = self._key(word)
            self._offsets[word].append(index)

    def tokens(self):
        """
        @rtype: C{list} of token
        @return: The document that this concordance index was
            created from.  
        """
        return self._tokens

    def offsets(self, word):
        """
        @rtype: C{list} of C{int}
        @return: A list of the offset positions at which the given
            word occurs.  If a key function was specified for the
            index, then given word's key will be looked up.
        """
        word = self._key(word)
        return self._offsets[word]

    def __repr__(self):
        return '<ConcordanceIndex for %d tokens (%d types)>' % (
            len(self._tokens), len(self._offsets))

    def generate_concordance(self, word, width=75, lines=25):
        """
        Print a concordance for C{word} with the specified context window.
        
        @param word: The target word
        @type word: C{str}
        @param width: The width of each line, in characters (default=80)
        @type width: C{int}
        @param lines: The number of lines to display (default=25)
        @type lines: C{int}
        """
        half_width = (width - len(word) - 2) / 2
        context = width/4 # approx number of words of context
        
        offsets = self.offsets(word)
        if offsets:
            lines = min(lines, len(offsets))
#            print "Displaying %s of %s matches:" % (lines, len(offsets))
            contexto = []
            for i in offsets:
                if lines <= 0:
                    break
                left = (' ' * half_width +
                        ' '.join(self._tokens[i-context:i]))
                right = ' '.join(self._tokens[i+1:i+context])
                left = left[-half_width:]
                right = right[:half_width]
                contexto.append( left +' '+ self._tokens[i] +' '+ right )
                lines -= 1
            self.contexto = contexto
        else:
            print "No matches"

# =======================		
# ADAPTADA DO NLTK
# =======================		

class TokenSearcher(object):
    """
    A class that makes it easier to use regular expressions to search
    over tokenized strings.  The tokenized string is converted to a
    string where tokens are marked with angle brackets -- e.g.,
    C{'<the><window><is><still><open>'}.  The regular expression
    passed to the L{findall()} method is modified to treat angle
    brackets as nongrouping parentheses, in addition to matching the
    token boundaries; and to have C{'.'} not match the angle brackets.
    """
    def __init__(self, tokens):
        self._raw = ''.join('<'+w+'>' for w in tokens) 

    def findall(self, regexp):
        """
        Find instances of the regular expression in the text.
        The text is a list of tokens, and a regexp pattern to match
        a single token must be surrounded by angle brackets.  E.g.
        
        >>> ts.findall("<.*><.*><bro>")
        ['you rule bro', ['telling you bro; u twizted bro
        >>> ts.findall("<a>(<.*>)<man>")
        monied; nervous; dangerous; white; white; white; pious; queer; good;
        mature; white; Cape; great; wise; wise; butterless; white; fiendish;
        pale; furious; better; certain; complete; dismasted; younger; brave;
        brave; brave; brave
        >>> text9.findall("<th.*>{3,}")
        thread through those; the thought that; that the thing; the thing
        that; that that thing; through these than through; them that the;
        through the thick; them that they; thought that the
        
        @param regexp: A regular expression
        @type regexp: C{str}
        """
        # preprocess the regular expression
        regexp = re.sub(r'\s', '', regexp)
        regexp = re.sub(r'<', '(?:<(?:', regexp)
        regexp = re.sub(r'>', ')>)', regexp)
        regexp = re.sub(r'(?<!\\)\.', '[^>]', regexp)

        # perform the search
        hits = re.findall(regexp, self._raw)

        # Sanity check
        for h in hits:
            if not h.startswith('<') and h.endswith('>'):
                raise ValueError('Bad regexp for TokenSearcher.findall')
            
        # postprocess the output
        hits = [h[1:-1].split('><') for h in hits]
        return hits

		
# =======================		
# COLOCACOES
# =======================		

class Ngrama (object):

	def __init__(self, palavras):
		self.palavras = palavras

  #checa ocorrencia de duplas de palavras e retorna uma lista de tuplas
	def set_bigramas(self,freq=3, best=50):
		bcf = BigramCollocationFinder.from_words(self.palavras)
		stopset = set(stopwords.words('portuguese'))
		filter_stops = lambda w: len(w) < 3 or w in stopset
		bcf.apply_word_filter(filter_stops)
		bcf.apply_freq_filter(freq)
		a = bcf.nbest(BigramAssocMeasures.pmi, best)
		self.bigramas = a

	def set_trigramas(self,freq=2,best=20):
		tcf = TrigramCollocationFinder.from_words(self.palavras)
		stopset = set(stopwords.words('portuguese'))
		filter_stops = lambda w: len(w) < 3 or w in stopset
		tcf.apply_word_filter(filter_stops)
		tcf.apply_freq_filter(freq)
		a = tcf.nbest(TrigramAssocMeasures.pmi, best)
		self.trigramas = a

	def set_ngramas(self, n):
		return ingrams(self.palavras, n)
		
	def fd(self):
		return FreqDist(self.palavras)

# =======================		
# POS TAGGEADOR 85%
# =======================		

class Classificador (object):

	def __init__(self):
		tsents = mac_morpho.tagged_sents()
		tsents = [[(w.lower(),t) for (w,t) in sent] for sent in tsents if sent]
		tagger0 = nltk.DefaultTagger('N')
		tagger1 = nltk.UnigramTagger(tsents[100:], backoff=tagger0)
		self.tagger = nltk.BigramTagger(tsents[100:], backoff=tagger1)		
	
	#classifica as palavras do texto
	def classificar(self,frases):
		self.texto_classificado = self.tagger.tag(frases)
	
	#devolve lista de palavras com determinada tag
	def filtrar(self,tag):
		filtrado = []
		for palavra in self.texto_classificado:
			if palavra[1] == tag:
				filtrado.append(palavra[0])
		return filtrado
	
# =======================		
# ADAPTADA DO NLTK
# =======================		

class Texto (object):
  #divide texto em palavras	
	def __init__(self, texto):
		self.texto = texto
		self.tokens = False
		self.palavras = False
		self.frases = False

	def set_tokens(self):
		self.tokens = WordPunctTokenizer().tokenize(self.texto)

	def set_palavras(self):
		tokenizer = RegexpTokenizer('\w+')
		self.palavras = tokenizer.tokenize(self.texto.lower())

	def set_frases(self):
		sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
		self.frases = sent_tokenizer.tokenize(self.texto)

	def similar(self, word, num=20):
		if not self.tokens:
			self.set_tokens()

		if '_word_context_index' not in self.__dict__:
			self._word_context_index = ContextIndex(self.tokens, filter=lambda x:x.isalpha(), key=lambda s:s.lower())
	#        words = self._word_context_index.similar_words(word, num)
		word = word.lower()
		wci = self._word_context_index._word_to_contexts
		if word in wci.conditions():
			contexts = set(wci[word])
			fd = FreqDist(w for w in wci.conditions() for c in wci[w] if c in contexts and not w == word)
			words = fd.keys()[:num]
			return words
		else:
			return False
            
	def concordance(self, word, width=79, lines=25):
		if not self.tokens:
			self.set_tokens()
		if '_concordance_index' not in self.__dict__:
			self._concordance_index = ConcordanceIndex(self.tokens,key=lambda s:s.lower())
		self._concordance_index.generate_concordance(word, width, lines)
		return self._concordance_index.contexto

# NAO FUNCIONA 
	def common_contexts(self, words, num=20):
		if not self.palavras:
			self.set_palavras()
		if '_word_context_index' not in self.__dict__:
			self._word_context_index = ContextIndex(self.palavras, key=lambda s:s.lower())
		try:
			fd = self._word_context_index.common_contexts(words, True)
			if not fd:
				return "No common contexts were found"
			else:
				ranked_contexts = fd.keys()[:num]
				return [(w1,w2) for w1,w2 in ranked_contexts]
		except ValueError, e:
			print e

	_CONTEXT_RE = re.compile('\w+|[\.\!\?]')

	def _context(self, tokens, i):
		# Left context
		j = i-1
		while j>=0 and not self._CONTEXT_RE.match(tokens[j]):
			j = j-1
		if j == 0: left = '*START*'
		else: left = tokens[j]
		# Right context
		j = i+1
		while j<len(tokens) and not self._CONTEXT_RE.match(tokens[j]):
			j = j+1
		if j == len(tokens): right = '*END*'
		else: right = tokens[j]
		return (left, right)

# =======================		
		
	
class Pagina (object):

	def __init__(self,url,titulo,texto):
		self.url = url
		self.titulo = titulo
		self.texto = Texto(texto)
		self.texto.set_palavras()
		self.palavras = self.texto.palavras
		self.ngrama = Ngrama(self.palavras)
		
	def extrair_bigramas(n):
		self.ngrama.set_bigramas(freq=n)
		return self.ngram.bigramas
		
	def extrair_trigramas(n):
		self.ngrama.set_trigramas(freq=n)
		return self.ngram.trigramas
	
	def extrair_fd():
		return self.ngrama.fd()
				
	def extrair_contextos(palavra):
		return self.texto.concordance(palavra)

# =======================		
		

class LingProcessador (object):

	def carregar_varredura():
		pass
	
	def salvar_termos():
		pass
		
	def salvar_ngramas():
		pass
		
	def salvar_entidades():
		pass
		
# =======================		
		
		
		


