from zap_crawl import ZapCrawl
from data_process import DataProcess

# zap =  ZapCrawl('data.csv')
# zap.zap_data_crawl_all()
data_process = DataProcess('test3.csv')
data_process.process()
data_process.manipulate()
data_process.save()
