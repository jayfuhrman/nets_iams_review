# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:02:46 2019

@author: VEST
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = 'sr15_metadata_indicators_r1.1.xlsx'
meta = pd.read_excel(file, sheetname='meta')

limit_1_5 = ['Below 1.5C','1.5C high overshoot','1.5C low overshoot']  #find scenarios which limit warming to 1.5 C by 2100
meta_1_5 = meta[meta.category.isin(limit_1_5)]

scenarios_1_5 = list(meta_1_5['scenario'])


limit_2 = ['Higher 2C','Lower 2C']  #find scenarios which limit warming to 1.5 C by 2100
meta_2 = meta[meta.category.isin(limit_2)]
scenarios_2 = list(meta_2['scenario'])

above2C = ['Above 2C']
meta_above2 = meta[meta.category.isin(above2C)]

world = pd.read_csv('iamc15_scenario_data_world_r1.1.csv')
regions = pd.read_csv('iamc15_scenario_data_all_regions_r1.1.csv')

#world['Model_Scenario'] = world['Model']+world['Scenario']

meta['model_scenario'] = meta['model']+meta['scenario']

drop_cols = ['Unnamed: 0','Model','Scenario','Region','Variable','Unit']

strings = world[drop_cols]
vals = world.drop(drop_cols,axis = 1)


vals = vals.astype('float64')
vals = vals.interpolate(axis = 1)
vals

df = pd.concat([strings,vals],axis = 1)


world = df

drop_cols = ['Unnamed: 0','Model','Scenario','Region','Variable','Unit']

strings = regions[drop_cols]
vals = regions.drop(drop_cols,axis = 1)

vals = vals.astype('float64')
vals = vals.interpolate(axis = 1)
vals

df = pd.concat([strings,vals],axis = 1)


df['Cumulative 2016-2100'] = df.iloc[:, -86:-1].sum(axis=1)

regions = df

world['Peak'] = world.iloc[:, -87:-3].max(axis=1)

world['Peak_Year'] = world.iloc[:, -88:-3].idxmax(axis=1)

regions_1_5 = regions[regions.Scenario.isin(scenarios_1_5)]

DAC = regions_1_5.loc[regions_1_5['Variable'] == 'Carbon Sequestration|Direct Air Capture']


DAC = DAC.loc[DAC['Region'] == 'World']

DAC = DAC.T

DAC = DAC.drop(['Unnamed: 0','Model','Scenario','Region','Variable','Unit','Cumulative 2016-2100'])
DAC = DAC.reset_index()
DAC = DAC.rename(index=str, columns={"index": "year"})


BECCS = regions_1_5.loc[regions_1_5['Variable'] == 'Carbon Sequestration|CCS|Biomass']
BECCS = BECCS.loc[BECCS['Region'] == 'World']

BECCS = BECCS.T

BECCS = BECCS.drop(['Unnamed: 0','Model','Scenario','Region','Variable','Unit','Cumulative 2016-2100'])

BECCS = BECCS.reset_index()
BECCS = BECCS.rename(index=str, columns={"index": "year"})

AF = regions_1_5.loc[regions_1_5['Variable'] == 'Carbon Sequestration|Land Use|Afforestation']
AF = AF.loc[AF['Region'] == 'World']

AF = AF.T

AF = AF.drop(['Unnamed: 0','Model','Scenario','Region','Variable','Unit','Cumulative 2016-2100'])

AF = AF.reset_index()
AF = AF.rename(index=str, columns={"index": "year"})


#%%
plt.figure(dpi=100)

plt.style.use('ggplot')
plt.style.use('seaborn-paper')

df = DAC
df = df.astype('float64') 
df = df.interpolate()
for column in df.drop('year', axis=1):
    line1 = plt.plot(df['year'], df[column]/1000,'-', color='silver', linewidth=1, alpha=0.5)
    

df = BECCS
df = df.astype('float64') 
df = df.interpolate()
for column in df.drop('year', axis=1):
    line2 = plt.plot(df['year'], df[column]/1000,'-', color='silver', linewidth=1, alpha=0.5)
    
df = AF
df = df.astype('float64') 
df = df.interpolate()
for column in df.drop('year', axis=1):
    line3 = plt.plot(df['year'], df[column]/1000,'-', color='silver', linewidth=1, alpha=0.5)


    
plt.ylabel('GtCO$_2$ yr$^{- 1}$')
plt.legend([line1[0],line2[0],line3[0]], ('Direct Air Capture','BECCS','Afforestation'),loc = 'upper left')


positive_emissions_technology = pd.read_csv('Global_Carbon_Budget_2018.csv')
positive_emissions_technology = positive_emissions_technology.set_index('Year')



#plt.savefig('Figures/cdr_pathways.png',dpi = 1200)
plt.show()



