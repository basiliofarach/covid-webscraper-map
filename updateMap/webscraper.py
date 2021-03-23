#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re
import pandas as pd
import folium
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142'}

req = requests.get('https://www.worldometers.info/coronavirus/', headers=headers)
req.request.headers
{'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
cont=req.content
country_location = pd.read_csv('updateMap/countries_location.csv')

soup=BeautifulSoup(cont,"html.parser")
def to_int(number, european=False):
    if european:
        number = number.replace('.', '')
    else:
        number = number.replace(',', '')
    return int(number)


# Classes sorting_1

# In[2]:


web_list = []
table_body=soup.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    data={}
    cols=row.find_all('td')
    cols=[x.text.strip() for x in cols]
    if cols[0] != "":
        data["Country"]=cols[1]
        data["Total Cases"]=to_int(cols[2])

        try:
            data["New Cases"]=to_int(cols[3])
        except:
            data["New Cases"]=0

        try:
            data["Total Deaths"]=to_int(cols[4])
        except:
            data["Total Deaths"]=0

        try:
            data["New Deaths"]=to_int(cols[5])
        except:
            data["New Deaths"]=0


        try:
            data["Total Recovered"]=to_int(cols[6])
        except:
            data["Total Recovered"]=0

        try:
            data["Active Cases"]=to_int(cols[7])
        except:
            data["Active Cases"]=0

        try:
            data["Serious"]=to_int(cols[8])
        except:
            data["Serious"]=0

        try:
            data["Tot Cases Per Million"]=to_int(cols[9])
        except:
            data["Tot Cases Per Million"]=None

        try:
            data["Deaths per Million"]=to_int(cols[10])
        except:
            data["Deaths per Million"]=None

        try:
            data["Total Tests"]=to_int(cols[11])
        except:
            data["Total Tests"]=None

        try:
            data["Tests per Million"]=to_int(cols[13])
        except:
            data["Tests per Million"]=None

        try:
            data["Population"]=to_int(cols[14])
        except:
            data["Population"]=None

        web_list.append(data)



# In[3]:


dataframe=pd.DataFrame(data=web_list)

dataframe.replace('USA', "United States of America", inplace = True)
dataframe.replace('Tanzania', "United Republic of Tanzania", inplace = True)
dataframe.replace('Democratic Republic of Congo', "Democratic Republic of the Congo", inplace = True)
dataframe.replace('Congo', "Republic of the Congo", inplace = True)
dataframe.replace('Lao', "Laos", inplace = True)
dataframe.replace('Syrian Arab Republic', "Syria", inplace = True)
dataframe.replace('Serbia', "Republic of Serbia", inplace = True)
dataframe.replace('Czechia', "Czech Republic", inplace = True)
dataframe.replace('UAE', "United Arab Emirates", inplace = True)
dataframe.replace('UK', "United Kingdom", inplace = True)

# In[5]:


dataframe = dataframe.replace('','', regex=True)
dataframe = dataframe.replace('\+','', regex=True)


# In[8]:


dataframe = dataframe.astype({'Total Cases': 'int64'})


# In[8]:


for (columnName) in dataframe.iteritems():
    if columnName[0] == "Country":
        dataframe[columnName[0]]=dataframe[columnName[0]].astype("string")
    try:
        if columnName[0] != "Country":
            dataframe[columnName[0]]=dataframe[columnName[0]].astype("float")
    except:
        pass



# In[9]:


dataframe.to_csv("updateMap/output.csv")
