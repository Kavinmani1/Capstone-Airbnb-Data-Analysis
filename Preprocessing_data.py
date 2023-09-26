#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import pandas as pd


# In[2]:


csv_file_path = 'capstone_sample_new_3.csv'


# In[3]:


data = pd.read_csv(csv_file_path)


# In[4]:


data


# In[5]:


columns_to_select= ['id', 'name', 'host_id','host_name','neighbourhood','neighbourhood_group_cleansed','latitude','longitude','room_type','price','minimum_nights','availability_365','number_of_reviews','last_review','calculated_host_listings_count','reviews_per_month','city','state','amenities','property_type'
]


# In[6]:


selected_columns = data[columns_to_select]


# In[7]:


selected_columns = selected_columns.copy()


# In[24]:


selected_columns['name'] = selected_columns['name'].str.replace('[^a-zA-Z0-9\s]', '', regex=True)


# In[25]:


selected_columns['name'] = selected_columns['name'].str.replace('[^a-zA-Z0-9\s]', '', regex=True).str.replace('\s', '_', regex=True)


# In[26]:


selected_columns['host_name'] = selected_columns['host_name'].str.replace(',', '&')


# In[8]:


selected_columns['amenities'] = selected_columns['amenities'].str.replace(',', '&')


# In[10]:


from datetime import datetime

input_format = "%d-%m-%Y"
selected_columns['last_review'] = pd.to_datetime(selected_columns['last_review'], format=input_format, errors='coerce')

output_format = "%Y-%m-%d"
selected_columns['last_review'] = selected_columns['last_review'].dt.strftime(output_format)

print(selected_columns.head())


# In[11]:


selected_columns['name'].head(50)


# In[12]:


selected_columns['host_name'].head(200)


# In[1]:


selected_columns['amenities'].head(200)


# In[ ]:


selected_columns.to_csv('capstone_sample_final.csv', index=False)

