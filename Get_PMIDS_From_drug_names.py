# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 02:12:05 2017

@author: nishal
"""
import sqlite3
from Bio.Entrez import read,efetch,email,tool
from metapub import PubMedFetcher
import pandas as pd
import requests
from datetime import  date
import xml.etree.ElementTree as ET
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from AbstractUtils import AbstractUtils
gs = AbstractUtils()
Abstract_data = pd.DataFrame(columns=["name","pmid","abstract"])
df_approved_drugs=pd.read_excel("/home/nishal/RAGA/ApprovedDrugs-DrugBank.xlsx")
Approved_drugs=tuple(df_approved_drugs['Name'])
pmids=gs.get_pmids_from_names(Approved_drugs)
count=[]
#Save to db and csv file
today_date= date.today()
today_date = str(today_date.month)+"_"+str(today_date.day)+"_"+str(today_date.year)
filename_csv = "cui_approved_drug_to_pmid"+today_date+".csv"
filename_db = "cui_approved_drug_to_pmid"+today_date+".db"
#df = pd.DataFrame.from_dict(pmids,orient='index')
df=pd.Series(pmids).to_frame(name="drug_name_to_pmid")
#df=df.transpose()
df=df.fillna(0)
#renaming column names
df=df.reset_index()
df=df.rename(columns={'index':'drug_name'})
for i in range(len(df)):
    count.append(len(df.loc[i]['drug_name_to_pmid'].split()))
df=df.assign(count=count)
df.to_csv("/home/nishal/RAGA/MetaMap/RAGA/"+filename_csv, sep='\t') #saving dataframe to .csv file
connection = sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/"+filename_db)  #establishing connection to database
cursor = connection.cursor()
df.to_sql("cui_approved_drug_to_pmid",connection,if_exists="replace",index=False)
#set_of_cuis = set(list_of_cuis) #this removes duplicates
#Saving list od cuis into a file
connection.close()

x=df[0:1001]
y=df[1001:2001]
z=df[2001:]
x.to_csv("/home/nishal/RAGA/MetaMap/RAGA/First_1000_Approved_drugs.csv",sep="\t")
y.to_csv("/home/nishal/RAGA/MetaMap/RAGA/Second_1000_Approved_drugs.csv",sep="\t")
z.to_csv("/home/nishal/RAGA/MetaMap/RAGA/Third_1000_Approved_drugs.csv",sep="\t")
conn_x=sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/First_1000_Approved_drugs.db")
conn_y=sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/Second_1000_Approved_drugs.db")
conn_z=sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/Third_1000_Approved_drugs.db")

x.to_sql("First_1000_approved_drugs",conn_x,if_exists="replace")
y.to_sql("Second_1000_approved_drugs",conn_y,if_exists="replace")
z.to_sql("Third_1000_approved_drugs",conn_z,if_exists="replace")
conn_x.close()
conn_y.close()
conn_z.close()