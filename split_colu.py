import pandas as pd
data = pd.read_csv('./mycsv.csv')


df_1 = data.drop(['15','16'], axis = 1)
# df_1 = data.drop(['17','18'], axis = 1)
print(df_1)
df_1.to_csv('mycsv.csv',header=False,index=False)
# df_1.to_csv('mycsv.csv')