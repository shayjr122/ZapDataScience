from bs4 import BeautifulSoup
import requests
import pandas as pd


BASE_URL = "https://www.zap.co.il/"
class ZapCrawl:
    def __init__(self, filename='test.csv',page=1):
        self.headers = { "User-Agent":"PostmanRuntime/7.29.0" }
        self.page = page
        self.filename= filename

    def crawl_data(self, link): 
        page = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.findAll ('div', {'class' : 'detailsRow'}, limit=None)
        titles = ['מחיר מינימלי','מחיר מקסימלי']
        spans = soup.find('div','PricesTxt').findAll('span') 
        if len(spans) == 2:
            values = [ spans[1].text, spans[0].text ]
        elif len(spans) == 1: 
            values = [ spans[0].text, spans[0].text ]
        else:
            values = [ None,None ]
        
        for i in range(0, len(links)):
            titles.append(links[i].find('div','detailsRowTitle').text.replace('?','').strip())
            # values.append(self.strip(links[i].find('div','detailsRowTxt').text.strip()))
            values.append(links[i].find('div','detailsRowTxt').text.strip())

            # if titles[-1] == 'תאריך כניסה לזאפ':
            #     values[-1] = values[-1].replace('מ','').strip()

        return dict(zip(titles,values))

    def zap_data_crawl_all(self):
        index = self.page
        df = pd.DataFrame()
        url = f'{BASE_URL}models.aspx?sog=c-pclaptop&pageinfo={index}'
        page = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        while soup.select_one('.selectedNumBtn') and soup.select_one('.selectedNumBtn').text == str(index):
            print(f'page number {index}')
            links = soup.findAll ('div', {'class' : 'MoreInfo'}, limit=None)   
            for i in range(0, len(links)):
                link = BASE_URL + links[i].find('a')["href"]
                cd = self.crawl_data(link)
                cd['מספר עמוד']=index
                df = pd.concat([df,pd.DataFrame([cd])])
                
            index+=1
            url = f'{BASE_URL}models.aspx?sog=c-pclaptop&pageinfo={index}'
            page = requests.get(url,headers=self.headers)
            soup = BeautifulSoup(page.text, 'html.parser')

        df.to_csv(self.filename, index=False ,encoding = 'utf-8-sig')
    
    # def strip(value):
    #     if value == 'לא זמין' or 'יעודכן בקרוב':
    #         return None