import pandas as pd


def translate_names(df):
    translated_df = pd.DataFrame()
    translation = {
   "יצרן":"Brand",
   "תאריך כניסה לזאפ":"Zap Enter Date",
   "התאמה לגיימינג":"Gaming Compability",
   "מערכת הפעלה":"Operating System",
   "תצורת ‎ 2 in 1":"Two in One",
   "משקל":"Weight",
   "סדרה":"Series",
   "סוג מעבד":"CPU type",
  "נפח זיכרון RAM":"RAM Capacity",
   "מהירות מעבד":"CPU speed",
   "דגם מעבד":"CPU modal",
   "דור מעבד":"CPU generation",
   "כונן קשיח":"Hard drive capacity",
   "מהירות כונן קשיח":"Hard drive Type",
  "כונן אופטי":"Optical Drive",
   "גודל מסך":"Screen Size",
   "רזולוציית מסך":"Screen Resolution",
   "סוג מסך":"Screen Type",
   "קצב רענון תצוגה":"FPS",
   "מסך מגע":"Touch Screen",
   "כרטיס מסך":"GPU",
   "מצלמת רשת":"Web camera",
   "אמצעי אבטחה":"Secutiry",
   "חיבורים":"Connectors",
   "רשת אלחוטית":"Wifi modal",
   "מודם סלולארי":"Cellular modem",
   "מחיר מינימלי":"Min price",
   "מחיר מקסימלי":"Max price",
   "Page Number": "Page number",
   "סוג הזכרון": "Memory type"}

    for key, value in translation.items():
        translated_df[value] = df[key]

    return translated_df



laptops_df = pd.read_csv('test3.csv')
print(laptops_df.head(10))
translated_df = translate_names(laptops_df)
print(translated_df.head(10))
translated_df.to_csv('laptops_data.csv', index=False ,encoding = 'utf:"8:"sig')