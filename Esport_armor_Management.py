#!/usr/bin/env python
# coding: utf-8

# In[12]:


#ESport_Final_Project
#what is the secret receipe?
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore') #we are suppressing the warnings


# In[5]:


armour_data = pd.read_csv("E:\\UOL\\Data Analysis for Esport\\Final Project\\archive\\esea_meta_demos.part2.csv", index_col=0)
armour_data_2 = pd.read_csv("E:\\UOL\\Data Analysis for Esport\\Final Project\\archive\\mm_master_demos.csv", index_col=0)


# In[6]:


#Round_type Count
armour_data.round_type.value_counts()


# In[7]:


#Round Type Analysis
sns.set_theme(style="darkgrid")

data = sns.countplot(x="round_type", data=armour_data)


# In[8]:


#Analysis of Spending as per teams
fig = plt.figure(figsize=(10, 5))
sns.kdeplot(armour_data['ct_eq_val'].rename('Counter-Terrorists vs Terrorists'),color="red")
sns.kdeplot(armour_data['t_eq_val'].rename('Counter-Terrorists vs Terrorists'),color="Green")
plt.suptitle("Spending as per Team")


# In[9]:


match_level_data = armour_data.groupby('file').head()


# In[7]:


match_level_data


# In[10]:


#Analysis for Additional spend help in winning round
df = pd.DataFrame().assign(winner=match_level_data['winner_side'], point_diff=match_level_data['ct_eq_val'] - match_level_data['t_eq_val'])
df = df.assign(point_diff=df.apply(lambda srs: srs.point_diff if srs.winner[0] == 'C' else -srs.point_diff, axis='columns'), winner=df.winner.map(lambda v: True if v[0] == 'C' else False))

df = (df
     .assign(point_diff_cat=pd.qcut(df.point_diff, 10))
     .groupby('point_diff_cat')
     .apply(lambda df: df.winner.sum() / len(df.winner))
)
df.index = df.index.values.map(lambda inv: inv.left + (inv.right - inv.left) / 2).astype(int)

fig = plt.figure(figsize=(10, 5))
df.plot.line()
plt.suptitle("Additional Spend Analysis")
ax = plt.gca()
ax.axhline(0.5, color='red')
ax.set_ylim([0, 1])
ax.set_xlabel('Spending by the team')
ax.set_ylabel('Games Won')


# In[53]:


fig = plt.figure(figsize=(10, 5))

sns.kdeplot(match_level_data.query('winner_side == "CounterTerrorist"').pipe(lambda df: df.ct_eq_val - df.t_eq_val).rename('Winning Matches Vs All Matches'),color="red")
sns.kdeplot(match_level_data.pipe(lambda df: df.ct_eq_val - df.t_eq_val).rename('Winning Matche Vs All Matches'),color="green")

plt.suptitle("Total Weapon value of the Team")


# In[11]:


#Weapon Wise Spend Analysis
g = sns.FacetGrid(armour_data_2.assign(
    total_val=armour_data_2['ct_eq_val'] + armour_data_2['t_eq_val']
), col="wp_type", col_wrap=4)
g.map(sns.distplot, 'total_val',color="red")


# In[29]:


weapon_events_2['wp_type'].head()


# In[ ]:




