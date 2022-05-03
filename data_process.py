from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

class DataProcess:
    def __init__(self,csv):
        self.df = pd.read_csv(csv)
    
    def process(self):

        for col in self.df:
            self.df.loc[(self.df[col] == 'לא זמין') | (self.df[col] == 'יעודכן בקרוב'), col] = None    

        self.df['תאריך כניסה לזאפ'] = self.df['תאריך כניסה לזאפ'].str.replace('מ','').str.strip()
        self.df['נפח זיכרון RAM'] = pd.to_numeric(self.df['נפח זיכרון RAM'].str.replace('GB','').str.strip())
        self.df['מהירות מעבד'] = pd.to_numeric(self.df['מהירות מעבד'].str.replace('Mhz','').str.replace('MHz','').str.strip())
        self.df['דור מעבד'] = pd.to_numeric(self.df['דור מעבד'].str.replace('דור','').str.strip())
        self.df['גודל מסך'] = pd.to_numeric(self.df['גודל מסך'].str.replace('אינטש','').str.strip())
        
        
        # self.df['כונן קשיח'] = pd.to_numeric(self.df['כונן קשיח'].str.replace('GB','').str.strip())
        

        self.df['רזולוציית מסך'] = self.df['רזולוציית מסך'].str.replace('X','x')
        self.df['משקל'] = self.df['משקל'].str.replace('ק"ג','').str.strip()
        self.df['משקל']= pd.to_numeric(self.df['משקל'])
        self.df['התאמה לגיימינג'] = self.df['התאמה לגיימינג'] == 'גיימינג' 
        self.df['מחיר מקסימלי'] = pd.to_numeric(self.df['מחיר מקסימלי'].str.replace(',',''))
        self.df['מחיר מינימלי'] = pd.to_numeric(self.df['מחיר מינימלי'].str.replace(',','' ))

        



        
        
        print(self.df.head())

    def manipulate(self):
        self.df['מחיר'] = (self.df['מחיר מקסימלי'] + self.df['מחיר מינימלי'])/2


        cond_dict = {
            'מתקפל':500,
            'מסך מסתובב':750,
            'מסך נשלף':1000,
            'ללא':0,
            'לא זמין':0,
            'לא רלוונטי':0
        }
        self.df['תוספת מחיר']=self.df['תצורת ‎ 2 in 1'].map(cond_dict)
        self.df['רזולוציית מסך'] = self.df['רזולוציית מסך'].fillna('0x0') 
        self.df['רזולוציית מסך'] = self.df['רזולוציית מסך'].apply(lambda s: int(s.split('x')[0]) *int(s.split('x')[1]))
        self.df['רזולוציית מסך'] = (self.df['רזולוציית מסך'] - self.df['רזולוציית מסך'].min()) / (self.df['רזולוציית מסך'].max() - self.df['רזולוציית מסך'].min())    

        self.df = self.df.drop(["מחיר מקסימלי" , "מחיר מינימלי", "תצורת ‎ 2 in 1" ] , axis = 1)
        
        print(self.df['רזולוציית מסך'].head())

    def save(self):
        self.df.to_csv('data.csv', index=False ,encoding = 'utf-8-sig')
        
        
        
