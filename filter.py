import string
import pandas as pd
import statistics
import array as array
import numpy as np

safety_raw = pd.read_excel ("./data/SA_trends.xlsx")

def check_num (num):
    if type (num) == int:
        return num
    return 0

def check_str (name):
    if type (name) == str:
        return True
    return False

dic = {}
for index, row in safety_raw.iterrows():
    if check_str (row [safety_raw.columns [0]]):
        try:
            dic [row [safety_raw.columns [0]]] += check_num (row [safety_raw.columns [6]])
        except:
            dic [row [safety_raw.columns [0]]] = 0
            dic [row [safety_raw.columns [0]]] += check_num (row [safety_raw.columns [6]])

safety_xl = pd.DataFrame (columns = ['Suburb', 'crime_total'])

cnt = 0
for i in dic:
    safety_xl.loc[cnt] = [i, dic [i]]
    cnt += 1

safety_xl = safety_xl.sort_values (by = safety_xl.columns [1], ascending = False)
safety_xl = safety_xl.reset_index (drop = True)

thirty = int (safety_xl.index.stop * 0.3)
forty = thirty + int (safety_xl.index.stop * 0.4)
thirty_1 = safety_xl.index.stop

safety_low = safety_xl [0:thirty]
safety_med = safety_xl [thirty: forty]
safety_high = safety_xl [forty: thirty_1]

# print ('clssification of suburbs based on safety level')
# print ('')
# print ('suburbs with safety level low')
# print (safety_low)
# print ('')
# print ('suburbs with safety level medium')
# print (safety_med)
# print ('')
# print ('suburbs with safety level high')
# print (safety_high)
# print ('')

rent_and_owner_raw = pd.read_excel ("./data/renter and owner.xlsx")

owned = pd.DataFrame (columns = ['Suburb', 'Total_owned'])
rented = pd.DataFrame (columns = ['Suburb', 'Total_rentd'])

own_loc = 0
rent_loc = 0

for index, row in rent_and_owner_raw.iterrows():
    own = row ['Total_owned'] * 100.0
    rent = row ['Total_rented'] * 100.0
    if own > 60.00:
        owned.loc [own_loc] = [row [rent_and_owner_raw.columns [0]], own]
        own_loc += 1
    if rent > 40.00:
        rented.loc [rent_loc] = [row [rent_and_owner_raw.columns [0]], rent]
        rent_loc += 1

# print ('classification of suburbs based on rent and ownership of properties')
# print ('')
# print ('more than 60 percent of owned properties listing')
# print (owned)
# print ('')
# print ('more than 40 percent of rented properties listing')
# print (rented)
# print ('')

income_xl = pd.read_excel ("./data/income.xlsx")

def check (num):
    if num == '':
        return False
    cnt = 0
    for i in num:
        if i in string.digits:
            cnt = 1
        elif i != ',':
            return False
    if cnt == 0:
        return False
    return int (num.replace (',', ''))

cnt = 0
for index, row in income_xl.iterrows():
    num = check (row ['income'])
    if not num:
        income_xl = income_xl.drop (income_xl.index [index - cnt])
        cnt += 1
    else:
        income_xl.income [index] = num

income_xl = income_xl.sort_values (by = 'income', ascending = True)
income_xl = income_xl.reset_index (drop = True)

del income_xl ['Field1']

twenty = int (income_xl.index.stop * 0.2)
fifty = twenty + int (income_xl.index.stop * 0.5)
thirty = income_xl.index.stop

income_low = income_xl [0:twenty]
income_med = income_xl [twenty: fifty]
income_high = income_xl [fifty: thirty]

# print ('clssification of suburbs based on income level')
# print ('')
# print ('suburbs with low household income')
# print (income_low)
# print ('')
# print ('suburbs with medium household income')
# print (income_med)
# print ('')
# print ('suburbs with high household income')
# print (income_high)
# print ('')

majorProff = pd.read_excel ("./data/modified_majorProff.xlsx")
typeofchurches = pd.read_excel ("./data/Typeofchurches.xlsx")

def results (f, s, t):
    curr_set_1 = []
    if f == 'low':
        curr_set_1 = [i for i in income_low.Title]
    elif f == 'medium':
        curr_set_1 = [i for i in income_med.Title]
    elif f == 'high':
        curr_set_1 = [i for i in income_high.Title]
    elif f == 'any':
        curr_set_1 = [i for i in income_low.Title] + [i for i in income_med.Title] + [i for i in income_high.Title]
    curr_set_2 = []
    if s == 'any':
        curr_set_2 = curr_set_1
    else:
        for i in curr_set_1:
            got = majorProff.loc [majorProff ['Title'] == i]
            if len (got) and s in got and got[s].values[0]:
                curr_set_2.append (i)
    curr_set_3 = []
    for i in curr_set_2:
        got = typeofchurches.loc [typeofchurches ['Title'] == i]
        if len (got) and t in got and got[t].values[0]:
            curr_set_3.append (i)
    return curr_set_3

def filter (i, p, c, s):
    return results(i, p+' (%)', c)

