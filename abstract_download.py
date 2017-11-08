# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 09:53:29 2017

@author: nishal
"""

import re
import time
import requests
from pymetamap import MetaMap
import pandas as pd
class GetAbstract():
    def __init__(self,tool='nishal_eutils',email='pattannl@mail.uc.edu'):
        self.tool=tool
        self.email=email
    def abstract_download(self,pmid):
        baseUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        url = baseUrl+"efetch.fcgi?db=pubmed&id="+pmid+"&rettype=xml"+"&tool="+self.tool+"&email="+self.email
        response=requests.request("GET",url).text
        abstract=re.findall(r"(<AbstractText>)(.*)(</AbstractText>)",response)
        if len(abstract)!= 0:
            abstract = abstract[0][1]
            return abstract

getabstract=GetAbstract(tool='nishal_eutils')
with open("/home/nishal/RAGA/MetaMap/CF-Drugs-related-PubmedIDs.txt",'r') as file1:
    pmids = file1.readlines()
#print pmids
abstract_list={}
list_of_cuis=[]
index = 0 #initializing index to 0 for dataframe
#initialize dataframe as df
df = pd.DataFrame(columns=["PMID","CUI","Preferred_name","sem_group","score"])
for pmid in pmids:
    time.sleep(5)
    download=getabstract.abstract_download(pmid)
    if download is not None:
        abstract_list[int(pmid)]=download

mm = MetaMap.get_instance("/home/nishal/RAGA/MetaMap/public_mm/bin/metamap16")
for pmid in abstract_list:
    concepts,error = mm.extract_concepts(tuple(abstract_list[pmid].split('.')))
#After extracting concepts, list out all the cui's
#Loop to return cui's of abstracts.
    for i in concepts:
        if i!=None:
            classtype = str(type(i))
            if not re.match(".*ConceptAA",classtype):
                    #list_of_cuis.append(i.cui)
                    x=i.semtypes
                    y=x.strip('[')
                    y=y.strip(']')
                    y=y.split(",")
                    if len(y) > 1:
                        for semtype in y:
                            df.loc[index]=pmid,i.cui,semtype,i.score,i.preferred_name
                            index +=1
                    elif len(y)==1:
                        df.loc[index]=pmid,i.cui,y[0],i.score,i.preferred_name
                        index +=1
                    else:
                        raise "Check the code"

df.to_csv('cui_07_11.csv', sep='\t',index=False) #saving dataframe to .csv file
#set_of_cuis = set(list_of_cuis) #this removes duplicates
#Saving list od cuis into a file
"""
with open("/home/nishal/RAGA/MetaMap/CUI.txt",'w') as file1:
    for i in list_of_cuis:
        file1.write(i)
        file1.write("\n") """

