# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:38:52 2015

@author: 0159056
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series,DataFrame
import time


# Basic Infomation sheet's directory
Info_sheet = r"E:\\AntiFraud\\app_pboc_s.xlsx"
# Save into DataFrame
#df = pd.read_excel(Info_sheet)
df_rule_check = df.copy()


'''
Rule: M_AFR_AP_1 ~ 8

The features of above rules as below:
1. Telephone No.
2. Company Name 
3. Company Address

The strategy of checking these rules:
1. Seperate the Feature columns out of 'Info_sheet' of aplicants
   (including primary applicant)
2. Change the column's name to ['TEL','NAME','ADDRESS']
3. Concat all the seperated dataframe into one
4. Count the other features by grouping the specific one
'''


# create a DataFrame including company phone no. and company name 
def change_col_name(dataframes):
    dataframes.columns = ['TEL','WORK_NAME','WORK_ADDRESS']
    dataframes['ori_index'] = dataframes.index
    return dataframes

# Seperate the Feature columns out of 'Info_sheet' of aplicants
# Primary applicant 
df_main_phone_company = df_rule_check[['AP_WORKUNITTEL','AP_WORKUNITNAME','AP_CORPADDR1']]
# Second applicant 
df_second_phone_company = df_rule_check[['AP_WORKUNITTEL_N1','AP_WORKUNITNAME_N1','AP_CORPADDR1_N1']]
# Third applicant
df_third_phone_company = df_rule_check[['AP_WORKUNITTEL_N2','AP_WORKUNITNAME_N2','AP_CORPADDR1_N2']]
# Forth applicant                
df_forth_phone_company = df_rule_check[['AP_WORKUNITTEL_N3','AP_WORKUNITNAME_N3','AP_CORPADDR1_N3']]
# Change the column's name to ['TEL','NAME','ADDRESS']
df_main_phone_company = change_col_name(df_main_phone_company)
df_second_phone_company = change_col_name(df_second_phone_company)
df_third_phone_company = change_col_name(df_third_phone_company)
df_forth_phone_company = change_col_name(df_forth_phone_company)


# Concat all the seperated dataframe into one                               
df_phone_company_address = pd.concat([df_main_phone_company,df_second_phone_company,df_third_phone_company,df_forth_phone_company])


# Checking M_AFR_AP_1(same telephone diff work_name)
rule = 'M_AFR_AP_1'
print ('Checking M_AFR_AP_1...')
tic = time.time()
# Select the records with notnull telephone no.
df_M_AFR_AP_1 = df_phone_company_address[df_phone_company_address.TEL.notnull()]

# Delete duplicated (TEL,WORK_NAME),remain distinct (TEL,WORK_NAME)
df_M_AFR_AP_1 = df_M_AFR_AP_1.drop_duplicates(['TEL','WORK_NAME'])
# Delete duplicated (WORK_NAME),remain distinct (WORK_NAME)
#df_M_AFR_AP_1 = df_M_AFR_AP_1.drop_duplicates(['WORK_NAME'])

# Single Telephone with lots WORK_NAME
df_M_AFR_AP_1_bad_phone_cnt = df_M_AFR_AP_1.groupby(by = 'TEL').count()['WORK_NAME']\
                        [df_M_AFR_AP_1.groupby(by = 'TEL').count()['WORK_NAME'].values>1] 
df_M_AFR_AP_1_bad_phone = df_M_AFR_AP_1_bad_phone_cnt.index
df_M_AFR_AP_1_bad = df_phone_company_address[df_phone_company_address.TEL.isin(df_M_AFR_AP_1_bad_phone)]
# find the original index
M_AFR_AP_1_bad_index = set(df_M_AFR_AP_1_bad.ori_index)
# M_AFR_AP_1's bad list
M_AFR_AP_1_bad_list = df_rule_check.loc[M_AFR_AP_1_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_1 = len(M_AFR_AP_1_bad_list)
# The number of records in black list which detectd by the rules
count_bad_M_AFR_AP_1 = len(M_AFR_AP_1_bad_list[M_AFR_AP_1_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_1 != 0:
    h_M_AFR_AP_1 = 1
else:
    h_M_AFR_AP_0 = 0
if count_bad_M_AFR_AP_1 != 0:
    c_M_AFR_AP_1 = 1
else:
    c_M_AFR_AP_1 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_1 = float(count_bad_M_AFR_AP_1)/hit_bad_M_AFR_AP_1
# input into result
in_df = {'rule':[rule],'effective':[h_M_AFR_AP_1],'hit_counts':hit_bad_M_AFR_AP_1,'is_in_bad':[c_M_AFR_AP_1],'in_bad_ratio':[ratio_M_AFR_AP_1]}
result = DataFrame(in_df)   
toc = time.time()
print ('M_AFR_AP_1 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')



# Checking M_AFR_AP_2(same work_name diff telephone)
rule = 'M_AFR_AP_2'
print ('Checking M_AFR_AP_2...')
tic = time.time()
# Select the records with notnull work name.s
df_M_AFR_AP_2 = df_phone_company_address[df_phone_company_address.WORK_NAME.notnull()]

# Delete duplicated (TEL,WORKNAME).,remain distinct (TEL,WORKNAME).
df_M_AFR_AP_2 = df_M_AFR_AP_2.drop_duplicates(['WORK_NAME','TEL'])
# Delete duplicated (TEL),remain distinct (TEL)
#df_M_AFR_AP_2 = df_M_AFR_AP_2.drop_duplicates(['TEL'])

# Single WORK_NAME with lots TELEPHONE NO.
df_M_AFR_AP_2_bad_name_cnt = df_M_AFR_AP_2.groupby(by = 'WORK_NAME').count()['TEL']\
                        [df_M_AFR_AP_2.groupby(by = 'WORK_NAME').count()['TEL'].values>1] 
df_M_AFR_AP_2_bad_name = df_M_AFR_AP_2_bad_name_cnt.index
df_M_AFR_AP_2_bad = df_phone_company_address[df_phone_company_address.WORK_NAME.isin(df_M_AFR_AP_2_bad_name)]
# find the original index
M_AFR_AP_2_bad_index = set(df_M_AFR_AP_2_bad.ori_index)
# M_AFR_AP_2's bad list
M_AFR_AP_2_bad_list = df_rule_check.loc[M_AFR_AP_2_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_2 = len(M_AFR_AP_2_bad_list)
# The number of records in black list which detectd by the rules
count_bad_M_AFR_AP_2 = len(M_AFR_AP_2_bad_list[M_AFR_AP_2_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_2 != 0:
    h_M_AFR_AP_2 = 1
else:
    h_M_AFR_AP_2 = 0
if count_bad_M_AFR_AP_2 != 0:
    c_M_AFR_AP_2 = 1
else:
    c_M_AFR_AP_2 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_2 = float(count_bad_M_AFR_AP_2)/hit_bad_M_AFR_AP_2
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_2,'hit_counts':hit_bad_M_AFR_AP_2,'is_in_bad':c_M_AFR_AP_2,'in_bad_ratio':ratio_M_AFR_AP_2}
result = result.append(in_df,ignore_index = True)  
toc = time.time()
print ('M_AFR_AP_2 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')



# Checking M_AFR_AP_3(same work_name diff telephone[:frontnum])
rule = 'M_AFR_AP_3'
print ('Checking M_AFR_AP_3...')

frontnum = 2

tic = time.time()
# Select the records with notnull work name.s
df_M_AFR_AP_3 = df_phone_company_address[df_phone_company_address.WORK_NAME.notnull()]

# Delete duplicated TELEPHONE NO.,remain distinct TELEPHONE NO.
df_M_AFR_AP_3 = df_M_AFR_AP_3.drop_duplicates(['WORK_NAME','TEL'])
# Delete duplicated (TEL),remain distinct (TEL)
#df_M_AFR_AP_3 = df_M_AFR_AP_3.drop_duplicates(['TEL'])

df_M_AFR_AP_3.TEL = df_M_AFR_AP_3.TEL.str.slice()                             
# Single WORK_NAME with lots TELEPHONE NO.
df_M_AFR_AP_3_bad_name_cnt = df_M_AFR_AP_3.groupby(by = 'WORK_NAME').count()['TEL']\
                        [df_M_AFR_AP_3.groupby(by = 'WORK_NAME').count()['TEL'].values>1] 
df_M_AFR_AP_3_bad_name = df_M_AFR_AP_3_bad_name_cnt.index
df_M_AFR_AP_3_bad = df_phone_company_address[df_phone_company_address.WORK_NAME.isin(df_M_AFR_AP_3_bad_name)]
# find the original index
M_AFR_AP_3_bad_index = set(df_M_AFR_AP_3_bad.ori_index)
# M_AFR_AP_3's bad list
M_AFR_AP_3_bad_list = df_rule_check.loc[M_AFR_AP_3_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_3 = len(M_AFR_AP_3_bad_list)
# The number of records in black list which detectd by the rules
count_bad_M_AFR_AP_3 = len(M_AFR_AP_3_bad_list[M_AFR_AP_3_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_3 != 0:
    h_M_AFR_AP_3 = 1
else:
    h_M_AFR_AP_3 = 0
if count_bad_M_AFR_AP_3 != 0:
    c_M_AFR_AP_3 = 1
else:
    c_M_AFR_AP_3 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_3 = float(count_bad_M_AFR_AP_3)/hit_bad_M_AFR_AP_3
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_3,'hit_counts':hit_bad_M_AFR_AP_3,'is_in_bad':c_M_AFR_AP_3,'in_bad_ratio':ratio_M_AFR_AP_3}
result = result.append(in_df,ignore_index = True)  
toc = time.time()
print ('M_AFR_AP_3 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')





