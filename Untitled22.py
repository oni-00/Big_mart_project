
# coding: utf-8

# In[4]:

import pandas as pd
import numpy as np


train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

train['/home/germain/big mart project/train.csv']='train'
test['/home/germain/big mart project/test.csv']='test'
data = pd.concat([train, test],ignore_index=True)
print (train.shape), (test.shape), (data.shape)


# In[5]:

data.apply(lambda x: sum(x.isnull()))


# In[4]:

data.describe()


# In[5]:

data.apply(lambda x: len(x.unique()))


# In[8]:

categorical_columns = [x for x in data.dtypes.index if data.dtypes[x]=='object']
categorical_columns = [x for x in categorical_columns if x not in ['Item_Identifier','Outlet_Identifier','source']]
for col in categorical_columns:
    print ('\nFrequency of Categories for varible %s'%col)
    print (data[col].value_counts())


# In[7]:

item_avg_weight = data.pivot_table(values='Item_Weight', index='Item_Identifier')
miss_bool = data['Item_Weight'].isnull() 
print ('Orignal #missing: %d'% sum(miss_bool))
data.loc[miss_bool,'Item_Weight'] = data.loc[miss_bool,'Item_Identifier'].apply(lambda x: item_avg_weight[x])
print ('Final #missing: %d'% sum(data['Item_Weight'].isnull()))


# In[20]:

from scipy.stats import mode

outlet_size_mode = data.pivot_table(values='Outlet_Size', columns='Outlet_Type',aggfunc=(lambda x:mode(x).mode[0]) )
print ('Mode for each Outlet_Type:')
print (outlet_size_mode)

miss_bool = data['Outlet_Size'].isnull() 

print ('\nOrignal #missing: %d'% sum(miss_bool))
data.loc[miss_bool,'Outlet_Size'] = data.loc[miss_bool,'Outlet_Type'].apply(lambda x: outlet_size_mode[x])
print sum( data['Outlet_Size'].isnull())



# In[3]:

data.pivot_table(values='Item_Outlet_Sales',index='Outlet_Type')


# In[10]:

visibility_avg=data.pivot_table(values='Item_Visibility', index='Item_Identifier')

miss_bool=(data['Item_Visibility'] == 0)

print ('Number of 0 values initially: %d'%sum(miss_bool))
data.loc[miss_bool,'Item_Visibility'] = data.loc[miss_bool,'Item_Identifier'].apply(lambda x: visibility_avg[x])
print ('Number of 0 values after modification: %d'%sum(data['Item_Visibility'] == 0))


# In[11]:

data['Item_Visibility_MeanRatio'] = data.apply(lambda x: x['Item_Visibility']/visibility_avg[x['Item_Identifier']], axis=1)
print (data['Item_Visibility_MeanRatio'].describe())


# In[ ]:



