#!/usr/bin/env python
# coding: utf-8

# In[120]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup,NavigableString,Tag
from selenium import webdriver
from datetime import datetime,date
import urllib.request
print("all necessary packages have been imported")


# # data gathering

# In[121]:


driver=webdriver.Chrome(executable_path="chromedriver_win32/chromedriver.exe")
url="https://www.mohfw.gov.in/"
driver.get(url)
webcontent=driver.page_source
Pysoup=BeautifulSoup(webcontent,'html')
driver.quit()


# In[122]:


Pysoup


# In[123]:


#table_name=statetable table table-striped


# In[124]:


divdata=Pysoup.find('div',{'class':'data-table table-responsive'})
divdate=divdata.h5.span.text.split(",")[0].split(":")[1].strip()
divdate
format="%d %B %Y"
datetimeobj=datetime.strptime(divdate,format).date()
datetimeobj


# In[125]:


tr_head=Pysoup.find('thead').find('tr',{'class':"row2"})
tr_head


# In[126]:


headings=[th.text.strip() for th in tr_head.find_all('th')]
headings


# In[130]:


mylistoftr=Pysoup.find('tbody').find_all('tr')
mytable=[]
headings=['S.No.','Name of State/UT','Total(active_cases)',
 'Change since yesterday(active_cases)',
 'Cumulative(cured)',
 'Change since yesterday(cured)',
 'Cumulative(deaths)',
 'Change since yesterday(deaths)']
for tr in mylistoftr:
    if isinstance(tr,Tag):
        statedata=[-int(td.text.strip())                   if (td.span !=None) and (td.span.get('class') in [['down']])                   else td.text.strip()
                   for td in tr.find_all('td')]
        data=dict(zip(headings,statedata))
        mytable.append(data)
state_data=pd.DataFrame(mytable,columns=headings)
state_data


# # looking into the data set

# In[101]:


state_data.columns


# In[102]:


df=state_data.set_index('Name of State/UT')
df.drop('S.No.',axis=1,inplace=True)
df


# In[103]:


state_data.set_index('S.No.',inplace=True)


# In[104]:


df.describe()


# In[105]:



df.columns


# In[106]:


df.shape


# In[107]:


df.isnull().sum()


# In[108]:


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[109]:


plt.title("view of null values")
sns.heatmap(df.isnull(),yticklabels=False,xticklabels=True,cbar=False,cmap='viridis')


# # Removal of null values

# In[141]:


df.dropna(how='any',axis=0,inplace=True) 
df


# In[142]:


plt.title("view of null values")
sns.heatmap(df.isnull(),yticklabels=False,xticklabels=True,cbar=False,cmap='viridis')


# # State with max deaths ,max cured and max active cases

# In[157]:


li=list(df['Total(active_cases)'])
li


# In[162]:


newlist=[int(i) for i in li]
  


# In[163]:


no_max_active_cases=max(newlist)


# In[172]:


df['Total(active_cases)'].iloc[:]


# In[164]:


no_max_active_cases


# In[ ]:




