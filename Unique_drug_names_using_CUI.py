# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 13:05:52 2017

@author: nishal
"""
import pandas as pd
df = pd.read_excel("C:\\Users\\nisha\\RAGA\\RxNAv_output\\RxNav_output.xlsx")
df_unique=pd.DataFrame(columns=df.columns)
All_CUIs=[]
count=0
for lab,row in df.iterrows():
    if row['UMLSCUI'] in All_CUIs:
        print(count)
    else:
        All_CUIs.append(row['UMLSCUI'])
        df_unique.loc[lab]=row['Input_Name'],row["UMLSCUI"],row['UMLSName_RxNavigator']
        count+=1
        print(count)
df_unique.to_csv("C:\\Users\\nisha\\RAGA\\RxNAv_output\\Unique_drugs_RxNav_output",sep="|",index_label=None)