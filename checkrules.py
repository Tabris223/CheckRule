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
def change_col_name1(dataframes):
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
df_main_phone_company = change_col_name1(df_main_phone_company)
df_second_phone_company = change_col_name1(df_second_phone_company)
df_third_phone_company = change_col_name1(df_third_phone_company)
df_forth_phone_company = change_col_name1(df_forth_phone_company)


# Concat all the seperated dataframe into one
df_phone_company_address = pd.concat([df_main_phone_company,df_second_phone_company,df_third_phone_company,df_forth_phone_company])


'''Checking M_AFR_AP_1(same telephone diff work_name)'''

rule = 'M_AFR_AP_1'
print ('Checking M_AFR_AP_1...')
tic = time.time()
# Select the records with notnull telephone no.
df_M_AFR_AP_1 = df_phone_company_address[df_phone_company_address.TEL.notnull()]

# Delete duplicated (TEL,WORK_NAME),remain distinct (TEL,WORK_NAME)
df_M_AFR_AP_1 = df_M_AFR_AP_1.drop_duplicates(['TEL','WORK_NAME'])
# Delete duplicated WORK_NAME,remain distinct WORK_NAME
#df_M_AFR_AP_1 = df_M_AFR_AP_1[df_M_AFR_AP_1.WORK_NAME.notnull()].drop_duplicates(['WORK_NAME'])

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
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_1 = len(M_AFR_AP_1_bad_list[M_AFR_AP_1_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_1 != 0:
    h_M_AFR_AP_1 = 1
else:
    h_M_AFR_AP_1 = 0
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



'''Checking M_AFR_AP_2(same work_name diff telephone)'''
rule = 'M_AFR_AP_2'
print ('Checking M_AFR_AP_2...')
tic = time.time()
# Select the records with notnull work name.s
df_M_AFR_AP_2 = df_phone_company_address[df_phone_company_address.WORK_NAME.notnull()]

# Delete duplicated (TEL,WORKNAME).,remain distinct (TEL,WORKNAME).
df_M_AFR_AP_2 = df_M_AFR_AP_2.drop_duplicates(['WORK_NAME','TEL'])
# Delete duplicated TEL,remain distinct TEL
#df_M_AFR_AP_2 = df_M_AFR_AP_2[df_M_AFR_AP_2.TEL.notnull()].drop_duplicates(['TEL'])

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
# The number of records in black list which was detectd by the rules
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



'''Checking M_AFR_AP_3(same work_name diff telephone[:frontnum])'''
rule = 'M_AFR_AP_3'
print ('Checking M_AFR_AP_3...')
frontnum = 2
tic = time.time()
# Select the records with notnull work name.s
df_M_AFR_AP_3 = df_phone_company_address[df_phone_company_address.WORK_NAME.notnull()]
df_M_AFR_AP_3.TEL = df_M_AFR_AP_3.TEL.str.slice(0,frontnum)

# Delete duplicated (WORKNAME,TEL).,remain distinct (WORKNAME,TEL).
df_M_AFR_AP_3 = df_M_AFR_AP_3.drop_duplicates(['WORK_NAME','TEL'])
# Delete duplicated TEL,remain distinct TEL
#df_M_AFR_AP_3 = df_M_AFR_AP_3[df_M_AFR_AP_3.TEL.notnull()].drop_duplicates(['TEL'])

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
# The number of records in black list which was detectd by the rules
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


'''Checking M_AFR_AP_4(same telephone diff WORK_ADDRESS)'''
rule = 'M_AFR_AP_4'
print ('Checking M_AFR_AP_4...')
tic = time.time()
# Select the records with notnull telephone no.
df_M_AFR_AP_4 = df_phone_company_address[df_phone_company_address.TEL.notnull()]

# Delete duplicated (TEL,WORK_ADDRESS),remain distinct (TEL,WORK_ADDRESS)
df_M_AFR_AP_4 = df_M_AFR_AP_4.drop_duplicates(['TEL','WORK_ADDRESS'])
# Delete duplicated WORK_ADDRESS,remain distinct WORK_ADDRESS
#df_M_AFR_AP_4 = df_M_AFR_AP_4[df_M_AFR_AP_4.WORK_ADDRESS.notnull()].drop_duplicates(['WORK_ADDRESS'])

# Single Telephone with lots WORK_ADDRESS
df_M_AFR_AP_4_bad_phone_cnt = df_M_AFR_AP_4.groupby(by = 'TEL').count()['WORK_ADDRESS']\
                        [df_M_AFR_AP_4.groupby(by = 'TEL').count()['WORK_ADDRESS'].values>1]
df_M_AFR_AP_4_bad_phone = df_M_AFR_AP_4_bad_phone_cnt.index
df_M_AFR_AP_4_bad = df_phone_company_address[df_phone_company_address.TEL.isin(df_M_AFR_AP_4_bad_phone)]
# find the original index
M_AFR_AP_4_bad_index = set(df_M_AFR_AP_4_bad.ori_index)
# M_AFR_AP_1's bad list
M_AFR_AP_4_bad_list = df_rule_check.loc[M_AFR_AP_4_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_4 = len(M_AFR_AP_4_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_4 = len(M_AFR_AP_4_bad_list[M_AFR_AP_4_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_4 != 0:
    h_M_AFR_AP_4 = 1
else:
    h_M_AFR_AP_4 = 0
if count_bad_M_AFR_AP_4 != 0:
    c_M_AFR_AP_4 = 1
else:
    c_M_AFR_AP_4 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_4 = float(count_bad_M_AFR_AP_4)/hit_bad_M_AFR_AP_4
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_4,'hit_counts':hit_bad_M_AFR_AP_4,'is_in_bad':c_M_AFR_AP_4,'in_bad_ratio':ratio_M_AFR_AP_4}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_4 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')


'''Checking M_AFR_AP_5(SAME WORK_ADDRESS diff TELEPHONE)'''
rule = 'M_AFR_AP_5'
print ('Checking M_AFR_AP_5...')
tic = time.time()
# Select the records with notnull telephone no.
df_M_AFR_AP_5 = df_phone_company_address[df_phone_company_address.WORK_ADDRESS.notnull()]

# Delete duplicated (WORK_ADDRESS,TEL),remain distinct (WORK_ADDRESS,TEL)
df_M_AFR_AP_5 = df_M_AFR_AP_5.drop_duplicates(['WORK_ADDRESS','TEL'])
# Delete duplicated TEL,remain distinct TEL
#df_M_AFR_AP_5 = df_M_AFR_AP_5[df_M_AFR_AP_5.TEL.notnull()].drop_duplicates(['TEL'])

# Single WORK_ADDRESS with lots Telephone
df_M_AFR_AP_5_bad_add_cnt = df_M_AFR_AP_5.groupby(by = 'WORK_ADDRESS').count()['TEL']\
                        [df_M_AFR_AP_5.groupby(by = 'WORK_ADDRESS').count()['TEL'].values>1]
df_M_AFR_AP_5_bad_add = df_M_AFR_AP_5_bad_add_cnt.index
df_M_AFR_AP_5_bad = df_phone_company_address[df_phone_company_address.WORK_ADDRESS.isin(df_M_AFR_AP_5_bad_add)]
# find the original index
M_AFR_AP_5_bad_index = set(df_M_AFR_AP_5_bad.ori_index)
# M_AFR_AP_1's bad list
M_AFR_AP_5_bad_list = df_rule_check.loc[M_AFR_AP_5_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_5 = len(M_AFR_AP_5_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_5 = len(M_AFR_AP_5_bad_list[M_AFR_AP_5_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_5 != 0:
    h_M_AFR_AP_5 = 1
else:
    h_M_AFR_AP_5 = 0
if count_bad_M_AFR_AP_5 != 0:
    c_M_AFR_AP_5 = 1
else:
    c_M_AFR_AP_5 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_5 = float(count_bad_M_AFR_AP_5)/hit_bad_M_AFR_AP_5
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_5,'hit_counts':hit_bad_M_AFR_AP_5,'is_in_bad':c_M_AFR_AP_5,'in_bad_ratio':ratio_M_AFR_AP_5}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_5 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')


'''Checking M_AFR_AP_6(SAME WORK_ADDRESS diff TELEPHONE[:frontnum])'''
rule = 'M_AFR_AP_6'
print ('Checking M_AFR_AP_6...')
tic = time.time()
# Select the records with notnull telephone no.
df_M_AFR_AP_6 = df_phone_company_address[df_phone_company_address.WORK_ADDRESS.notnull()]
df_M_AFR_AP_6.TEL = df_M_AFR_AP_6.TEL.str.slice(0,frontnum)

# Delete duplicated (WORK_ADDRESS,TEL),remain distinct (WORK_ADDRESS,TEL)
df_M_AFR_AP_6 = df_M_AFR_AP_6.drop_duplicates(['WORK_ADDRESS','TEL'])
# Delete duplicated TEL,remain distinct TEL
#df_M_AFR_AP_6 = df_M_AFR_AP_6[df_M_AFR_AP_6.TEL.notnull()].drop_duplicates(['TEL'])

# Single WORK_ADDRESS with lots Telephone
df_M_AFR_AP_6_bad_add_cnt = df_M_AFR_AP_6.groupby(by = 'WORK_ADDRESS').count()['TEL']\
                        [df_M_AFR_AP_6.groupby(by = 'WORK_ADDRESS').count()['TEL'].values>1]
df_M_AFR_AP_6_bad_add = df_M_AFR_AP_6_bad_add_cnt.index
df_M_AFR_AP_6_bad = df_phone_company_address[df_phone_company_address.WORK_ADDRESS.isin(df_M_AFR_AP_6_bad_add)]
# find the original index
M_AFR_AP_6_bad_index = set(df_M_AFR_AP_6_bad.ori_index)
# M_AFR_AP_6's bad list
M_AFR_AP_6_bad_list = df_rule_check.loc[M_AFR_AP_6_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_6 = len(M_AFR_AP_6_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_6 = len(M_AFR_AP_6_bad_list[M_AFR_AP_6_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_6 != 0:
    h_M_AFR_AP_6 = 1
else:
    h_M_AFR_AP_6 = 0
if count_bad_M_AFR_AP_6 != 0:
    c_M_AFR_AP_6 = 1
else:
    c_M_AFR_AP_6 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_6 = float(count_bad_M_AFR_AP_6)/hit_bad_M_AFR_AP_6
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_6,'hit_counts':hit_bad_M_AFR_AP_6,'is_in_bad':c_M_AFR_AP_6,'in_bad_ratio':ratio_M_AFR_AP_6}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_6 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')


'''Checking M_AFR_AP_7(SAME WORK_ADDRESS & TELEPHONE diff WORK_NAME)'''
rule = 'M_AFR_AP_7'
print ('Checking M_AFR_AP_7...')
tic = time.time()
# Select the records with notnull TEL no and notnull WORK_ADDRESS .
df_M_AFR_AP_7 = df_phone_company_address[df_phone_company_address.WORK_ADDRESS.notnull() & df_phone_company_address.TEL.notnull()]

# Delete duplicated ('WORK_ADDRESS','TEL','WORK_NAME'),remain distinct ('WORK_ADDRESS','TEL','WORK_NAME')
df_M_AFR_AP_7 = df_M_AFR_AP_7.drop_duplicates(['WORK_ADDRESS','TEL','WORK_NAME'])
# Delete duplicated WORK_NAME,remain distinct WORK_NAME
#df_M_AFR_AP_7 = df_M_AFR_AP_7[df_M_AFR_AP_7.WORK_NAME.notnull()].drop_duplicates(['WORK_NAME'])

# Single (WORK_ADDRESS,TEL) with lots WORK_NAME
df_M_AFR_AP_7_bad_add_tel_cnt = df_M_AFR_AP_7.groupby(by = ['WORK_ADDRESS','TEL']).count()['WORK_NAME']\
                        [df_M_AFR_AP_7.groupby(by = ['WORK_ADDRESS','TEL']).count()['WORK_NAME'].values>1]
df_M_AFR_AP_7_bad_add_tel = df_M_AFR_AP_7_bad_add_tel_cnt.index
df_M_AFR_AP_7_bad_add_tel = DataFrame(list(df_M_AFR_AP_7_bad_add_tel),columns = ['WORK_ADDRESS','TEL'])
df_M_AFR_AP_7_bad = df_phone_company_address\
                    [df_phone_company_address.WORK_ADDRESS.isin(df_M_AFR_AP_7_bad_add_tel.WORK_ADDRESS) &\
                     df_phone_company_address.TEL.isin(df_M_AFR_AP_7_bad_add_tel.TEL)]
# find the original index
M_AFR_AP_7_bad_index = set(df_M_AFR_AP_7_bad.ori_index)
# M_AFR_AP_1's bad list
M_AFR_AP_7_bad_list = df_rule_check.loc[M_AFR_AP_7_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_7 = len(M_AFR_AP_7_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_7 = len(M_AFR_AP_7_bad_list[M_AFR_AP_7_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_7 != 0:
    h_M_AFR_AP_7 = 1
else:
    h_M_AFR_AP_7 = 0
if count_bad_M_AFR_AP_7 != 0:
    c_M_AFR_AP_7 = 1
else:
    c_M_AFR_AP_7 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_7 = float(count_bad_M_AFR_AP_7)/hit_bad_M_AFR_AP_7
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_7,'hit_counts':hit_bad_M_AFR_AP_7,'is_in_bad':c_M_AFR_AP_7,'in_bad_ratio':ratio_M_AFR_AP_7}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_7 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')



'''Checking M_AFR_AP_8(SAME WORK_NAME & TELEPHONE diff WORK_ADDRESS)'''
rule = 'M_AFR_AP_8'
print ('Checking M_AFR_AP_8...')
tic = time.time()
# Select the records with notnull TEL no and notnull WORK_ADDRESS .
df_M_AFR_AP_8 = df_phone_company_address[df_phone_company_address.WORK_ADDRESS.notnull() & df_phone_company_address.TEL.notnull()]

# Delete duplicated ('WORK_ADDRESS','TEL','WORK_NAME'),remain distinct ('WORK_ADDRESS','TEL','WORK_NAME')
df_M_AFR_AP_8 = df_M_AFR_AP_8.drop_duplicates(['WORK_ADDRESS','TEL','WORK_NAME'])
# Delete duplicated WORK_ADDRESS,remain distinct WORK_ADDRESS
#df_M_AFR_AP_8 = df_M_AFR_AP_8[df_M_AFR_AP_8.WORK_ADDRESS.notnull()].drop_duplicates(['WORK_ADDRESS'])

# Single (WORK_NAME,TEL) with lots WORK_ADDRESS
df_M_AFR_AP_8_bad_name_tel_cnt = df_M_AFR_AP_8.groupby(by = ['WORK_NAME','TEL']).count()['WORK_ADDRESS']\
                        [df_M_AFR_AP_8.groupby(by = ['WORK_NAME','TEL']).count()['WORK_ADDRESS'].values>1]
df_M_AFR_AP_8_bad_name_tel = df_M_AFR_AP_8_bad_name_tel_cnt.index
df_M_AFR_AP_8_bad_name_tel = DataFrame(list(df_M_AFR_AP_8_bad_name_tel),columns = ['WORK_NAME','TEL'])
df_M_AFR_AP_8_bad = df_phone_company_address\
                    [df_phone_company_address.WORK_NAME.isin(df_M_AFR_AP_8_bad_name_tel.WORK_NAME) &\
                     df_phone_company_address.TEL.isin(df_M_AFR_AP_8_bad_name_tel.TEL)]
# find the original index
M_AFR_AP_8_bad_index = set(df_M_AFR_AP_8_bad.ori_index)
# M_AFR_AP_1's bad list
M_AFR_AP_8_bad_list = df_rule_check.loc[M_AFR_AP_8_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_8 = len(M_AFR_AP_8_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_8 = len(M_AFR_AP_8_bad_list[M_AFR_AP_8_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_8 != 0:
    h_M_AFR_AP_8 = 1
else:
    h_M_AFR_AP_8 = 0
if count_bad_M_AFR_AP_8 != 0:
    c_M_AFR_AP_8 = 1
else:
    c_M_AFR_AP_8 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_8 = float(count_bad_M_AFR_AP_8)/hit_bad_M_AFR_AP_8
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_8,'hit_counts':hit_bad_M_AFR_AP_8,'is_in_bad':c_M_AFR_AP_8,'in_bad_ratio':ratio_M_AFR_AP_8}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_8 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')



'''
Rule: M_AFR_AP_9 ~ 10

The features of above rules as below:
1. Home Phone No.
2. Home Address

The strategy of checking these rules:
1. Seperate the Feature columns out of 'Info_sheet' of aplicants
   (including primary applicant)
2. Change the column's name to ['HOME_TEL','HOME_ADDRESS']
3. Concat all the seperated dataframe into one
4. Count the other features by grouping the specific one
'''

# create a DataFrame including HOME_PHONE and HOMEADDR
def change_col_name2(dataframes):
    dataframes.columns = ['HOME_PHONE','HOMEADDR']
    dataframes['ori_index'] = dataframes.index
    return dataframes

# Seperate the Feature columns out of 'Info_sheet' of aplicants
# Primary applicant
df_main_home_phone_add = df_rule_check[['AP_HOMEPHONE','AP_HOMEADDR1']]
# Second applicant
df_second_home_phone_add = df_rule_check[['AP_HOMEPHONE_N1','AP_HOMEADDR1_N1']]
# Third applicant
df_third_home_phone_add = df_rule_check[['AP_HOMEPHONE_N2','AP_HOMEADDR1_N2']]
# Forth applicant
df_forth_home_phone_add = df_rule_check[['AP_HOMEPHONE_N2','AP_HOMEADDR1_N2']]
# Change the column's name to ['TEL','NAME','ADDRESS']
df_main_home_phone_add = change_col_name2(df_main_home_phone_add)
df_second_home_phone_add = change_col_name2(df_second_home_phone_add)
df_third_home_phone_add = change_col_name2(df_third_home_phone_add)
df_forth_home_phone_add = change_col_name2(df_forth_home_phone_add)


# Concat all the seperated dataframe into one
df_home_phone_add = pd.concat([df_main_home_phone_add,df_second_home_phone_add,df_third_home_phone_add,df_forth_home_phone_add])

'''Checking M_AFR_AP_9(same HOMEADDR diff HOME_PHONE)'''
rule = 'M_AFR_AP_9'
print ('Checking M_AFR_AP_9...')
tic = time.time()
# Select the records with notnull HOMEADDR
df_M_AFR_AP_9 = df_home_phone_add[df_home_phone_add.HOMEADDR.notnull()]

# Delete duplicated (HOMEADDR,HOME_PHONE).,remain distinct (HOMEADDR,HOME_PHONE).
df_M_AFR_AP_9 = df_M_AFR_AP_9.drop_duplicates(['HOMEADDR','HOME_PHONE'])
# Delete duplicated HOME_PHONE,remain distinct HOME_PHONE
#df_M_AFR_AP_9 = df_M_AFR_AP_9[df_M_AFR_AP_9.HOME_PHONE.notnull()].drop_duplicates(['HOME_PHONE'])

# Single HOMEADDR with lots HOME_PHONE.
df_M_AFR_AP_9_bad_add_cnt = df_M_AFR_AP_9.groupby(by = 'HOMEADDR').count()['HOME_PHONE']\
                        [df_M_AFR_AP_9.groupby(by = 'HOMEADDR').count()['HOME_PHONE'].values>1]
df_M_AFR_AP_9_bad_add = df_M_AFR_AP_9_bad_add_cnt.index
df_M_AFR_AP_9_bad = df_home_phone_add[df_home_phone_add.HOMEADDR.isin(df_M_AFR_AP_9_bad_add)]
# find the original index
M_AFR_AP_9_bad_index = set(df_M_AFR_AP_9_bad.ori_index)
# M_AFR_AP_9's bad list
M_AFR_AP_9_bad_list = df_rule_check.loc[M_AFR_AP_9_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_9 = len(M_AFR_AP_9_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_9 = len(M_AFR_AP_9_bad_list[M_AFR_AP_9_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_9 != 0:
    h_M_AFR_AP_9 = 1
else:
    h_M_AFR_AP_9 = 0
if count_bad_M_AFR_AP_9 != 0:
    c_M_AFR_AP_9 = 1
else:
    c_M_AFR_AP_9 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_9 = float(count_bad_M_AFR_AP_9)/hit_bad_M_AFR_AP_9
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_9,'hit_counts':hit_bad_M_AFR_AP_9,'is_in_bad':c_M_AFR_AP_9,'in_bad_ratio':ratio_M_AFR_AP_9}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_9 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')


'''Checking M_AFR_AP_10(same HOME_PHONE diff HOMEADDR)'''
rule = 'M_AFR_AP_10'
print ('Checking M_AFR_AP_10...')
tic = time.time()
# Select the records with notnull HOME_PHONE
df_M_AFR_AP_10 = df_home_phone_add[df_home_phone_add.HOME_PHONE.notnull()]

# Delete duplicated (HOMEADDR,HOME_PHONE).,remain distinct (HOMEADDR,HOME_PHONE).
df_M_AFR_AP_10 = df_M_AFR_AP_10.drop_duplicates(['HOMEADDR','HOME_PHONE'])
# Delete duplicated HOMEADDR,remain distinct HOMEADDR
#df_M_AFR_AP_10 = df_M_AFR_AP_10[df_M_AFR_AP_10.HOMEADDR.notnull()].drop_duplicates(['HOMEADDR'])

# Single HOME_PHONE with lots HOMEADDR.
df_M_AFR_AP_10_bad_phone_cnt = df_M_AFR_AP_10.groupby(by = 'HOME_PHONE').count()['HOMEADDR']\
                        [df_M_AFR_AP_10.groupby(by = 'HOME_PHONE').count()['HOMEADDR'].values>1]
df_M_AFR_AP_10_bad_phone = df_M_AFR_AP_10_bad_phone_cnt.index
df_M_AFR_AP_10_bad = df_home_phone_add[df_home_phone_add.HOME_PHONE.isin(df_M_AFR_AP_10_bad_phone)]
# find the original index
M_AFR_AP_10_bad_index = set(df_M_AFR_AP_10_bad.ori_index)
# M_AFR_AP_10's bad list
M_AFR_AP_10_bad_list = df_rule_check.loc[M_AFR_AP_10_bad_index]
# Counts the numbers
# The number of records hit the rules
hit_bad_M_AFR_AP_10 = len(M_AFR_AP_10_bad_list)
# The number of records in black list which was detectd by the rules
count_bad_M_AFR_AP_10 = len(M_AFR_AP_10_bad_list[M_AFR_AP_10_bad_list.bad == 1])
# Flags
if hit_bad_M_AFR_AP_10 != 0:
    h_M_AFR_AP_10 = 1
else:
    h_M_AFR_AP_10 = 0
if count_bad_M_AFR_AP_10 != 0:
    c_M_AFR_AP_10 = 1
else:
    c_M_AFR_AP_10 = 0
# Cover ratio of Black list
ratio_M_AFR_AP_10 = float(count_bad_M_AFR_AP_10)/hit_bad_M_AFR_AP_10
# input into result
in_df = {'rule':rule,'effective':h_M_AFR_AP_10,'hit_counts':hit_bad_M_AFR_AP_10,'is_in_bad':c_M_AFR_AP_10,'in_bad_ratio':ratio_M_AFR_AP_10}
result = result.append(in_df,ignore_index = True)
toc = time.time()
print ('M_AFR_AP_10 finished')
print ('cost time: %.2fs' %(toc-tic))
print ('\n')

