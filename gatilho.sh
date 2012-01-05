#! /bin/bash


#links
/home/machina/semantika/links/guardarlinks.py

#analytics
#/home/machina/semantika/oraculo/coleta.py

#curl http://localhost:6800/schedule.json -d project=monitoramento -d spider=generica
#curl http://localhost:6800/schedule.json -d project=monitoramento -d spider=generica

# aranhas
cd /home/machina/semantika/
/usr/local/bin/scrapy crawl generica
#/usr/local/bin/scrapy crawl parceiros

/home/machina/semantika/texto/plnproc.py

touch /home/machina/SUCESSO
