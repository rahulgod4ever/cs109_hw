
# coding: utf-8

# In[4]:

get_ipython().magic(u'matplotlib inline')

import pandas as pd
import matplotlib.pyplot as plt


# In[5]:

countries_url = 'https://github.com/cs109/2014_data/raw/master/countries.csv'
countries_raw = pd.read_csv(countries_url)
countries = set([country for country in countries_raw['Country']])


# In[6]:

ppp_url = 'http://spreadsheets.google.com/pub?key=phAwcNAVuyj1jiMAkmq1iMg&output=xls'
ppp = pd.read_excel(ppp_url)


# In[7]:

years = []
for i in range(1,len(ppp.columns)):
    years.append(ppp.columns[i])


# In[8]:

data = pd.DataFrame(columns = countries, index = years)

#index by country
ppp.index = ppp['gdp pc 2011 ppp']

ppp.head()
#create data
for country in countries:
    for year in years:
        if country in ppp.index:
            data[country][year]=ppp[year][country]
            


# In[9]:

import math
from pylab import *
import numpy as np

def TextPlot(value,labels):
    max_value = max(value)
    max_label_length = max([len(s) for s in labels])
    for i in range(len(value)):
        print labels[i].ljust(max_label_length)," " ,"═"*int(value[i]*100/max_value)
    
def plotforyear(year):
    lcountry = []
    lincome = []
    
    for country in data.columns:
        if not math.isnan(data[country][year]):
            lcountry.append(country)
            lincome.append(data[country][year])
    TextPlot(lincome,lcountry)  
plotforyear(2000)


# In[10]:

from scipy.stats import norm

def ratioNormals(diff,a):
    #diff: difference in means
    #a: cut-off values
    
    return (1-norm(diff,1).cdf(a))/(1-norm(0,1).cdf(a))



# In[84]:

import BeautifulSoup
import requests

population_url = 'http://en.wikipedia.org/wiki/List_of_countries_by_past_and_future_population'

html = requests.get(population_url).content
soup = BeautifulSoup.BeautifulSoup(html)


# In[102]:

def gettables():
    table_arr=[]
    for table in soup.findAll('table'):
        if table.get('class')=='sortable wikitable':
            table_arr.append(table)
    return table_arr

def getyears(table):
    years = []
    for year in table.findAll('tr')[0].findAll('th'):
        try:
            years.append(int(year.contents[0]))
        except:
            pass
    return years


tables = gettables()

#Only look at table 3
table = tables[2]
years = getyears(table)
countries = [country for country in data.columns]
population_data = pd.DataFrame(columns=countries,index=years)


# In[108]:

#Fill population_data df
def isint(x):
    try:
        int(x)
        return True
    except:
        return False

def fillpopdata():
#Create mask and map
    mask = []
    year = []
    i=0
    for th in table.findAll('th'):
        if isint(th.contents[0]):
            mask.append(True)
            year.append(int(th.contents[0]))
        else:
            mask.append(False)
            year.append(0)
    
    for tr in table.findAll('tr'):
        td_list =  [td for td in tr.findAll('td')]
        if len(td_list)>0:
            country = td_list[0].findAll('a')[0].contents[0]
            for i in range(1,len(td_list)):
                if(mask[i]):
                    pop = int(td_list[i].contents[0].replace(',',''))
                    if country in population_data.columns:
                        population_data[country][year[i]] = pop
                    

fillpopdata()



# In[140]:

avgAsia = 0
avgSA = 0
totalPopAsia = 0
totalPopSA = 0

pAsia = 0
tAsia = 0
pSA =0
tSA = 0
#Portion of countries with income higher than 10000 and total number of countries taken into account

year = 2005
#get weighted averages for 2005
for i,r in countries_raw.iterrows():
    country = r['Country']
    region = r['Region']
    if country in population_data.columns:
        if isint(population_data[country][year]) and isint(data[country][year]):
            if region == "ASIA" or region == "OCEANIA":
                avgAsia = avgAsia + data[country][year]*population_data[country][year]
                totalPopAsia = totalPopAsia + population_data[country][year]
                if data[country][year] > 15000:
                    pAsia = pAsia + 1
                tAsia = tAsia + 1
            elif region == "SOUTH AMERICA":
                avgSA = avgSA + data[country][year]*population_data[country][year]
                totalPopSA = totalPopSA + population_data[country][year]
                if data[country][year] > 15000:
                    pSA = pSA + 1
                tSA = tSA + 1
avgAsia = avgAsia/totalPopAsia
avgSA = avgSA/totalPopSA

pAsia = float(pAsia)/tAsia
pSA = float(pSA)/tSA
print "Average income for Asia is ", avgAsia
print "Average income for South America is ",avgSA
print ""
print "Proportion of countries in Asia with income higher than 10000 is ",pAsia
print "Proportion of countries in South America with income higher than 10000 is ",pSA


# In[ ]:



