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
count=[]
df_approved_drugs=pd.read_excel("/home/nishal/RAGA/ApprovedDrugs-DrugBank.xlsx")
Approved_drugs=tuple(df_approved_drugs['Name'])
pmids=gs.get_pmids_from_names_with_pd_filter(Approved_drugs)
#Save to db and csv file
today_date= date.today()
today_date = str(today_date.month)+"_"+str(today_date.day)+"_"+str(today_date.year)
filename_csv = "Approved_drug_to_pmid_with_pd_filter"+today_date+".csv"
filename_db = "Approved_drug_to_pmid_with_pd_filter"+today_date+".db"
#df = pd.DataFrame.from_dict(pmids,orient='index')
df=pd.Series(pmids).to_frame(name="drug_name_to_pmid")
#df=df.transpose()
df=df.fillna(0)
df=df.reset_index()
#renaming column names
df=df.rename(columns={'index':'drug_name'})
for i in range(len(df)):
    a=df.loc[i]['drug_name_to_pmid']
    count.append(len(a.split()))
df=df.assign(count=count)
df.to_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/"+filename_csv, sep='\t') #saving dataframe to .csv file
connection = sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/"+filename_db)  #establishing connection to database
cursor = connection.cursor()
df.to_sql("Approved_drug_to_pmid_with_pd_filter",connection,if_exists="replace")
#set_of_cuis = set(list_of_cuis) #this removes duplicates
#Saving list od cuis into a file
connection.close()

x=df[0:1001]
y=df[1001:2001]
z=df[2001:]
x.to_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/First_1000_Approved_drugs_with_pd_filter.csv",sep="\t")
y.to_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/Second_1000_Approved_drugs_with_pd_filter.csv",sep="\t")
z.to_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/Third_1000_Approved_drugs_with_pd_filter.csv",sep="\t")
conn_x=sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/First_1000_Approved_drugs_with_pd_filter.db")
conn_y=sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/Second_1000_Approved_drugs_with_pd_filter.db")
conn_z=sqlite3.connect("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/with_pd_filter/Third_1000_Approved_drugs_with_pd_filter.db")

x.to_sql("First_1000_approved_drugs_with_pd_filter",conn_x,if_exists="replace")
y.to_sql("Second_1000_approved_drugs_with_pd_filter",conn_y,if_exists="replace")
z.to_sql("Third_1000_approved_drugs_with_pd_filter",conn_z,if_exists="replace")
conn_x.close()
conn_y.close()
conn_z.close()