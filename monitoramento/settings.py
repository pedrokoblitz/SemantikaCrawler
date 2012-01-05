# Scrapy settings for monitoramento project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'estimado'
BOT_VERSION = '0.1'

SPIDER_MODULES = ['monitoramento.spiders']
NEWSPIDER_MODULE = 'monitoramento.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#DEPTH_LIMIT = 2

ITEM_PIPELINES = [
	'monitoramento.pipelines.Lexico',
	'monitoramento.pipelines.LimparCurtos',
	'monitoramento.pipelines.LimparCapas',
	'monitoramento.pipelines.Repetidas',
	'monitoramento.pipelines.MongoStore',
	#'monitoramento.pipelines.ContadorUrls'
	]
