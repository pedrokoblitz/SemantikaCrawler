#!/usr/bin/env python -tt
#-*- coding:utf-8 -*-

import urlparse
# =====================================================================  
# FUNCOES PUBLICAS
# =====================================================================    

# =====================================================================  
# CODIFICAÇÃO
# =====================================================================    

def decodeutf8(string):
  try:
    return unicode(string).decode('utf-8')
  except (UnicodeEncodeError,UnicodeDecodeError):
    print 'erro codificao ', string
    pass

def encodeutf8(string):
  try:
    return unicode(string).encode('utf-8')
  except (UnicodeEncodeError,UnicodeDecodeError):
    print 'erro decodificacao ', string
    pass


# =====================================================================  
# URLS & LINKS
# =====================================================================    

# =====================================================================  
# limpa urls longas
# utilizado como processador da aranha
# =====================================================================  

def limpar_url_longa(url):
  url_proc = ''.join(url)
  p_url = urlparse.urlparse(url_proc)
  if '?utm' in p_url[4]:
    url = url.split('?utm')[0]
  if '&feature' in p_url[4]:
    url = url.split('&feature')[0]
  url_limpa = re.sub('www\.','',url_proc)
  return url_limpa

# =====================================================================  
# DOMINIOS
# =====================================================================  
  
# =====================================================================  
# devolve dominio
# =====================================================================  

def tirar_dominio(url):
  if url.startswith('http'):
    try:
      parsed = urlparse.urlparse(url)
      if parsed[1].startswith('www'):
        dominio = parsed[1][4:]
      else:
        dominio = parsed[1]
      return dominio
    except ValueError:
      pass
  else:
    pass
    
# =====================================================================  
# cria lista de dominios
# =====================================================================  

def listar_dominios(urls):
  urls_unicas = list(set(urls))
  dominiosBase = map(tirar_dominio, urls_unicas)
  return dominiosBase
  
# =====================================================================  
# DATA
# =====================================================================    

def datahora():
  agora = str(datetime.datetime.utcnow())
  ano = agora[0:4]
  mes = agora[5:7]
  dia = agora[8:10]
  hora = agora[11:19]
  return (hora,dia,mes,ano)
  
# =====================================================================  
# HASH UNICO
# =====================================================================    

def hash_unico():
  unico = hash(datetime.datetime.utcnow())
  if unico < 0:
    unico = unico*-1
  return unico

def hash_url(url):
  url_hash = hash(url)
  if url_hash < 0:
    url_hash = url_hash*-1
  return str(url_hash)



