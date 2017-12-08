# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:37:42 2017

@author: nishal
"""

import pandas as pd
#from httplib import IncompleteRead
#import AbstractUtils
import numpy as np
import time
from datetime import date
import sqlite3
from metapub import PubMedFetcher
AbstractFetch=PubMedFetcher()
from Bio import Entrez
Entrez.email = 'pattannl@mail.uc.edu' #give mail id to Entrez eutils
Entrez.tool='nishal_eutils'
connection=sqlite3.connect("C:\\Users\\nisha\\RAGA\\First_1000_Approved_drugs.db")
drug_to_pmid_to_abstract=pd.DataFrame(columns=["DRUG","PMID","Abstract"])
df1=pd.read_sql("SELECT * from First_100",connection,index_col=None,columns=["drug_name","drug_name_to_pmid","count"])
#df1=pd.read_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/Without_Filter_names_to_pmids/First_1000_Approved_drugs.csv",sep="\t")
#df2=pd.read_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/Second_1000_Approved_drugs.csv",sep="\t")
#df3=pd.read_csv("/home/nishal/RAGA/MetaMap/RAGA/Latest_code/Third_1000_Approved_drugs.csv",sep="\t")

#cleaning and filling missing data
df1=df1.fillna(0)
#df2=df2.fillna(0)
#df3=df3.fillna(0)
if "Unnamed: 0" in df1.columns:
    df1=df1.drop("Unnamed: 0",axis=1)
#elif "Unnamed: 0" in df2.columns:
   # df2=df2.drop(columns=["Unnamed: 0"])
#elif "Unnamed: 0" in df3.columns:
    #df3=df3.drop(columns=["Unnamed: 0"])
df1=df1[df1['count']!=0] #taking only those drugs which have pmids and leaving remaining
df1=df1.drop(labels="index",axis=1) #remove duplicate index if available as a column
index=0
t1=time.time()
missed_drugs=[]
df1=df1[0:10]
for lab,row in df1.iterrows() :
    print(row['drug_name'])
    try:
        pmids_list= row['drug_name_to_pmid'].split() #taking all pmids from dataframe,column 'drug_name_to_pmid'
        handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pmids_list)),   #fetching pubmed ids   
                       rettype="xml", retmode="text")
        records = Entrez.read(handle)
        abstracts = [pubmed_article['MedlineCitation']['Article']['Abstract']['AbstractText'][0]  
                     if 'Abstract' in pubmed_article['MedlineCitation']['Article'].keys() 
                     else pubmed_article['MedlineCitation']['Article']['ArticleTitle'] 
                     for pubmed_article in records['PubmedArticle']]
        abstract_dict = dict(zip(pmids_list, abstracts))
        for pmid in abstract_dict.keys():
            drug_to_pmid_to_abstract.loc[index]= row['drug_name'],pmid,abstract_dict[pmid]
            index+=1
    except:
        print("exception")
        missed_drugs.append({ row['drug_name']:pmids_list})
        continue
t2=time.time()
print ("Time Complexity",t2-t1)
today_date= date.today()
today_date = str(today_date.month)+"_"+str(today_date.day)+"_"+str(today_date.year)
filename_csv = "approved_drug_to_pmid_to_abstract"+today_date+".csv"
filename_db = "approved_drug_to_pmid_to_abstract"+today_date+".db"
connection_abstract = sqlite3.connect("C:\\Users\\nisha\\RAGA\\"+filename_db)
drug_to_pmid_to_abstract.to_sql("approved_drug_to_pmid_to_abstract",connection_abstract,if_exists="append")
drug_to_pmid_to_abstract.to_csv("C:\\Users\\nisha\\RAGA\\"+filename_csv, sep='|') #saving dataframe to .csv file
connection.close()
connection_abstract.close()
"""
for i in range(len(df1)):
    pmids_list=df1.loc[i][1].split()
    #unique.remove(df1.loc[i][0])
    for pmid in pmids_list:
        if pmid != 0 and len(pmids_list) != 0:
            try:
                article = AbstractFetch.article_by_pmid(pmid)
                abstract = article.abstract
                if abstract is None:
                    abstract = article.title
                elif article.book_abstracts is not None:
                    abstract = article.book_abstracts
                if abstract is not None:
                    drug_to_pmid_to_abstract.loc[index]=df1.loc[i][0],pmid,abstract
                index+=1
            except:
                print "Connection Refused"
                time.sleep(5)
                continue
        else:
            drug_to_pmid_to_abstract.loc[index]=df1.loc[i][0],pmid,"-"
            index+=1
#drug_to_pmid_to_abstract.to_csv()
            """