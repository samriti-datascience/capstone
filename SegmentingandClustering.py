#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system("conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab")
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system("conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium # map rendering library


# In[4]:


get_ipython().system('pip install geopy')


# In[449]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
html = urlopen(url) 
soup = BeautifulSoup(html, 'html.parser')


# In[450]:


soup


# In[451]:


tables = soup.find_all('table')


# In[452]:


type(tables)


# In[454]:


req_table=tables[0]


# In[455]:


for i in req_table:
    rows2=req_table.find_all('td')


# In[456]:


len(rows2)


# In[458]:


pincode=[]
burough=[]
neighbourhood=[]
for i in range(0,len(rows2)):
    if(len(rows2[i].findAll('a'))==1):
        pincode.append(rows2[i].findAll('b')[0].text)
        burough.append(rows2[i].findAll('a')[0].get('title'))
        #If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.
        neighbourhood.append(rows2[i].findAll('a')[0].get('title'))
    elif(len(rows2[i].findAll('a'))>=2):
        for j in range(1,len(rows2[i].findAll('a'))):
            pincode.append(rows2[i].findAll('b')[0].text)
            burough.append(rows2[i].findAll('a')[0].get('title'))
            neighbourhood.append(rows2[i].findAll('a')[j].get('title'))
    else:
        pincode.append(rows2[i].findAll('b')[0].text)
        burough.append('0')
        neighbourhood.append('0')


# In[459]:


type(pincode)


# In[462]:


len(pincode)


# In[463]:


len(burough)


# In[465]:


len(neighbourhood)


# In[466]:


import pandas as pd
df_final = pd.DataFrame(
    {'PostalCode': pincode,
     'Borough': burough,
     'Neighborhood': neighbourhood
    })


# Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.

# In[469]:


df_fin=df_final[df_final['Borough']!='0']


# In[471]:


df2=df_fin.groupby("PostalCode").count()['Neighborhood']>1


# In[472]:


df2=df2.reset_index()


# In[473]:


df2


# In[474]:


list_pincode_single=df2[df2['Neighborhood']==False]['PostalCode'].tolist()


# In[476]:


list_pincode_multiple=df2[df2['Neighborhood']==True]['PostalCode'].tolist()


# In[492]:


cols={'PostalCode','Borough','Neighborhood'}
k=pd.DataFrame(columns=cols)
for i in range(0,len(df_fin)):
    if(df_fin.iloc[i]['PostalCode'] in list_pincode_single):
        k=k.append(df_fin.iloc[i])  


# In[482]:


len(list_pincode_multiple)


# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.

# In[483]:


pincode2=[]
burough2=[]
neighbourhood2=[]


# In[484]:


for j in range(0,len(list_pincode_multiple)):
        pincode2.append(list_pincode_multiple[j])
        #print(pincode2)
        burough2.append(df_fin[df_fin['PostalCode']==list_pincode_multiple[j]]['Borough'].iloc[0])
        str1=""
        neighbourhood2.append(str1.join(df_fin[df_fin['PostalCode']==list_pincode_multiple[j]]['Neighborhood'].tolist()))  


# In[485]:


len(pincode2)


# In[486]:


len(burough2)


# In[487]:


len(neighbourhood2)


# In[488]:


import pandas as pd
df_multipleeq = pd.DataFrame({'PostalCode': pincode2,'Borough': burough2,'Neighborhood': neighbourhood2})


# In[496]:


len(k)


# In[499]:


final=df_multipleeq.append(k)


# In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.

# In[501]:


final.shape


# In[ ]:




