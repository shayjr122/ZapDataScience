from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

class DataProcess:
    def __init__(self,csv):
        self.df = pd.read_csv(csv)
    
    def process(self):

        for col in self.df:
            self.df.loc[(self.df[col] == 'לא זמין') | (self.df[col] == 'יעודכן בקרוב'), col] = None    

        self.df['תאריך כניסה לזאפ'] = pd.to_numeric(self.df['תאריך כניסה לזאפ'].str.replace('מ','').str.replace('עד','').str.strip())
        self.df['נפח זיכרון RAM'] = pd.to_numeric(self.df['נפח זיכרון RAM'].str.replace('GB','').str.strip())
        self.df['מהירות מעבד'] = pd.to_numeric(self.df['מהירות מעבד'].str.replace('Mhz','').str.replace('MHz','').str.strip())
        self.df['דור מעבד'] = pd.to_numeric(self.df['דור מעבד'].str.replace('דור','').str.strip())
        self.df['גודל מסך'] = pd.to_numeric(self.df['גודל מסך'].str.replace('אינטש','').str.strip())
        self.df["קצב רענון תצוגה"] = pd.to_numeric(self.df["קצב רענון תצוגה"].str.lower().str.replace('hz','').str.strip())
        self.df.loc[(self.df["סוג הזכרון"] == "לא רלוונטי") | (self.df["סוג הזכרון"] == "DDRAM"), "סוג הזכרון"] = None
        self.df["סוג הזכרון"] = pd.to_numeric(self.df["סוג הזכרון"].str.replace('DDR','').str.strip())


        
        
        self.df['כונן קשיח'] = self.df['כונן קשיח'].str.replace('GB','').str.strip()
        for i in range(len(self.df['כונן קשיח'])):
            if i == 200:
                x = 5
            if not self.df.loc[i, 'כונן קשיח']:
                continue
            arr = self.df.loc[i, 'כונן קשיח'].replace(",","+").split("+")
            if len(arr) > 1:
                sum = 0
                for num in arr:
                    sum += int(num)
                self.df.loc[i, 'כונן קשיח'] = sum
            else:
                self.df.loc[i, 'כונן קשיח'] = int(arr[0])

       
        self.df['רזולוציית מסך'] = self.df['רזולוציית מסך'].str.replace('X','x')
        self.df['משקל'] = self.df['משקל'].str.replace('ק"ג','').str.strip()
        self.df['משקל']= pd.to_numeric(self.df['משקל'])
        

        self.df['מחיר מקסימלי'] = pd.to_numeric(self.df['מחיר מקסימלי'].str.replace(',',''))
        self.df['מחיר מינימלי'] = pd.to_numeric(self.df['מחיר מינימלי'].str.replace(',','' ))

        

    def manipulate(self):
        self.df=self.df.dropna()
        self.df['מחיר'] = (self.df['מחיר מקסימלי'] + self.df['מחיר מינימלי'])/2
        self.df['מסך מגע']  = np.where(self.df['מסך מגע']  == "כולל" , 1 , 0)
        self.df['כונן אופטי']  = np.where(self.df['כונן אופטי']  == "כולל" , 1 , 0)
        self.df['מודם סלולארי']  = np.where(self.df['מודם סלולארי']  == "כולל" , 1 , 0)
        self.df['התאמה לגיימינג']  = np.where(self.df['התאמה לגיימינג']  == "גיימינג" , 1 , 0)


        cond_dict = {
            'מתקפל':500,
            'מסך מסתובב':750,
            'מסך נשלף':1000,
            'ללא':0,
            'לא זמין':0,
            'לא רלוונטי':0
        }
        self.df['תוספת מחיר']=self.df['תצורת ‎ 2 in 1'].map(cond_dict)
        # self.df['רזולוציית מסך'] = self.df['רזולוציית מסך'].fillna('0x0') 
        self.df['רזולוציית מסך'] = self.df['רזולוציית מסך'].apply(lambda s: int(s.split('x')[0]) *int(s.split('x')[1]))
        self.df['רזולוציית מסך'] = (self.df['רזולוציית מסך'] - self.df['רזולוציית מסך'].min()) / (self.df['רזולוציית מסך'].max() - self.df['רזולוציית מסך'].min())    
        self.df['מחיר'] = (self.df['מחיר'] - self.df['מחיר'].min()) / (self.df['מחיר'].max() - self.df['מחיר'].min())    
        self.df = self.df.drop(["מחיר מקסימלי" , "מחיר מינימלי", "תצורת ‎ 2 in 1" ] , axis = 1)
        

    def save(self):
        numeric_df = self.df[["דור מעבד" , "סוג הזכרון","תאריך כניסה לזאפ", "נפח זיכרון RAM","התאמה לגיימינג", "כונן קשיח", "קצב רענון תצוגה","כונן אופטי","מסך מגע","גודל מסך"	, "רזולוציית מסך","מודם סלולארי"]]
        # "תוספת מחיר" 
        print(sns.heatmap(numeric_df.corr()))



	

        # self.df.style.background_gradient(cmap='Blues')
        # print(self.df.corr(method=histogram_intersection))
        # self.df['יצרן'] = LabelEncoder().fit_transform(self.df['יצרן'])
        # self.df['מערכת הפעלה'] = LabelEncoder().fit_transform(self.df['מערכת הפעלה'])
        # self.df['סדרה'] = LabelEncoder().fit_transform(self.df['סדרה'])
        # self.df['סוג מעבד'] = LabelEncoder().fit_transform(self.df['סוג מעבד'])

        # self.df['דגם מעבד'] = LabelEncoder().fit_transform(self.df['דגם מעבד'])
        # self.df['מהירות כונן קשיח'] = LabelEncoder().fit_transform(self.df['מהירות כונן קשיח'])
        # self.df['סוג מסך'] = LabelEncoder().fit_transform(self.df['סוג מסך'])
        # self.df['כרטיס מסך'] = LabelEncoder().fit_transform(self.df['כרטיס מסך'])
        # self.df['אמצעי אבטחה'] = LabelEncoder().fit_transform(self.df['אמצעי אבטחה'])
        # self.df['מצלמת רשת'] = LabelEncoder().fit_transform(self.df['מצלמת רשת'])
        # self.df['חיבורים'] = LabelEncoder().fit_transform(self.df['חיבורים'])
        # self.df['רשת אלחוטית'] = LabelEncoder().fit_transform(self.df['רשת אלחוטית'])




        # sns.heatmap(self.df, annot=True)
        # self.df.to_csv('data.csv', index=False ,encoding = 'utf-8-sig')
        
# def histogram_intersection(a, b):
#     v = np.minimum(a, b).sum().round(decimals=1)
#     return v
        
