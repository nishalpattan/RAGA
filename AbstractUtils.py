# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:08:10 2017

@author: nishal
"""
from Bio.Entrez import read,efetch,email,tool
from metapub import PubMedFetcher
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

fetch = PubMedFetcher()
class AbstractUtils():
    def __init__(self,Email="pattannl@mail.uc.edu",Tool="nishal_eutils"):
        self.Email = Email
        self.Tool=Tool
    def get_pmids_from_names(self,list_of_names,max_pmids=1500):
        self.max_pmids=max_pmids
        """ 
            This method returns query_name to pubmed ids in a dictionary format
        """
        name_to_pmids = {}
        for name in list_of_names:
            try:
                pmids = fetch.pmids_for_query(name, retmax=self.max_pmids)
            except:
                time.sleep(5)
                continue
            if len(pmids) != 0 and len(pmids)>=1:
                #name_to_pmids[name]=tuple(pmids)
                name_to_pmids[name]=" ".join(pmids)
            else:
                try:
                    name1 = name
                    while(len(pmids) == 0 and len(name1) != 0):
                        name1 = name1.split()
                        name1.pop()
                        name1=" ".join(name1)
                        #print name1
                        #pmids = fetch.pmids_for_query(name1, retmax=self.max_pmids)
                        if name1 != "" and name1 != " " :
                            pmids = fetch.pmids_for_query(name1, retmax=self.max_pmids)
                        else:
                            pmids=[] #as the drug name with /pd has no articles
                    name_to_pmids[name]=" ".join(pmids)
                except:
                    name_to_pmids[name]=" ".join(pmids)
                    continue
        return name_to_pmids
    def get_pmids_from_names_with_pd_filter(self,list_of_names,max_pmids=1000):
        self.max_pmids=max_pmids
        """ 
            This method returns query_name to pubmed ids in a dictionary format
        """
        name_to_pmids = {}
        for name in list_of_names:
            try:
                pmids = fetch.pmids_for_query(name+"/pd",retmax=self.max_pmids)
            except:
                time.sleep(5)
                continue
            if len(pmids) != 0 and len(pmids)>=1:
                #name_to_pmids[name]=tuple(pmids)
                name_to_pmids[name]=" ".join(pmids)
            else:
                try:
                    name1 = name
                    while(len(pmids) == 0 and len(name1) != 0):
                        name1 = name1.split()
                        name1.pop()
                        name1=" ".join(name1)
                        #print name1
                        #pmids = fetch.pmids_for_query(name1, retmax=self.max_pmids)
                        if name1 != "" and name1 != " " :
                            pmids = fetch.pmids_for_query(name1+"/pd", retmax=self.max_pmids)
                        else:
                            pmids=[] #as the drug name with /pd has no articles
                    name_to_pmids[name]=" ".join(pmids)
                except:
                    name_to_pmids[name]=" ".join(pmids)
                    continue
        return name_to_pmids
    def abstract_download(self,dict_pmids):
        index=0
        Abstract_data = pd.DataFrame(columns=["name","pmid","abstract"])
        #baseUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        for names in dict_pmids:
            for pmid in dict_pmids[names]:
                try:
                    article = fetch.article_by_pmid(pmid)
                    abstract = article.abstract
                    if abstract is None:
                        abstract = article.title
                    elif article.book_abstracts is not None:
                        abstract = article.book_abstracts
                    if abstract is not None:
                        Abstract_data.loc[index]=names,pmid,abstract
                    index+=1
                except:
                    print "Connection Refused"
                    time.sleep(5)
                    continue
        return Abstract_data
    """
    def abstract_download(self,dict_pmids):
      
            This method returns abstract for a given pmid and add to the abstract data
        index=0
        baseUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        for names in dict_pmids:
            for pmid in dict_pmids[names]:
                try:
                    abstract = []
                    url = baseUrl+"efetch.fcgi?db=pubmed&id="+pmid+"&rettype=xml"+"&tool="+self.Tool+"&email="+self.Email
                    response=requests.request("GET",url,timeout=500).text
                    response=response.encode('utf-8')
                    root=ET.fromstring(response)
                    root_find=root.findall('./PubmedArticle/MedlineCitation/Article/Abstract/')
                    if len(root_find)==0:
                        root_find=root.findall('./PubmedArticle/MedlineCitation/Article/ArticleTitle')
                    for i in range(len(root_find)):
                        if root_find[i].text != None:
                            abstract.append(root_find[i].text)
                    if abstract is not None:
                        Abstract_data.loc[index]=names,pmid,"".join(abstract)
                    index+=1
                except:
                    print "Connection Refused"
                    time.sleep(5)
                    continue
        return Abstract_data
        """
    """
    def get_abstracts_from_pmids(self,dict_pmids):
        index=0
        for names in dict_pmids:
            for pmid in dict_pmids[names]:
                handle = efetch(db='pubmed', id=pmid, retmode='xml')
                xml_data = read(handle)
                print xml_data
                try:
                    article = xml_data['PubmedArticle'][0]['MedlineCitation']['Article']
                    print article
                    abstract = "".join(article['Abstract']['AbstractText'])
                    Abstract_data.loc[index]=names,pmid,abstract
                    index+=1
                except KeyError:
                    continue
        return Abstract_data
        
gs = AbstractUtils()
Abstract_data = pd.DataFrame(columns=["name","pmid","abstract"])
df_approved_drugs=pd.read_excel("/home/nishal/RAGA/ApprovedDrugs-DrugBank.xlsx")
Approved_drugs=tuple(df_approved_drugs['Name'])
pmids=gs.get_pmids_from_names(Approved_drugs)
Abstract_data=gs.abstract_download(pmids)
"""