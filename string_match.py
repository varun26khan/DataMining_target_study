import string
import stop_words
import pandas as pd
import ast
import csv

"""""""""string_match retuens a matrix of matching percents"""""""""


def string_match(str1, str2):
    count = 0
    try:                                     # removes punctuations, stop words and splits the string
        list1 = [m for m in ''.join([m for m in str1.lower() if m not in string.punctuation]).split(' ') if m not in stop_words.scrapper]
        list2 = [m for m in ''.join([m for m in str2.lower() if m not in string.punctuation]).split(' ') if m not in stop_words.scrapper]
    except AttributeError:
        list2 = str2
        try:
            list1 = str1.split()
        except AttributeError:
            list1 = str1
    list1 = [x for x in list1 if x]
    list2 = [x for x in list2 if x]
    print(list1)
    print(list2)
    for n in list1:
        if n in list2:
            count += 1
    try:
        match_12 = (count / len(list1)) * 100
        match_21 = (count / len(list2)) * 100
    except ZeroDivisionError:
        match_12 = match_21 = 0.0
    return round(match_12, 2), round(match_21, 2)


df1 = pd.read_csv('google.txt', sep=',')     # two csv files to match the data
df2 = pd.read_csv('target_study.txt', sep='\t')

"""""""""arr is a list of lists of 6 percents"""""""""

arr = []
for i in range(len(df1)):
    for j in range(len(df2)):
        address1 = str(ast.literal_eval(df1['address'][i])['line1']) + ',' + str(ast.literal_eval(df1['address'][i])['line2'])
        address2 = ast.literal_eval(df2['address'][j])['address line 1'] + ',' + ast.literal_eval(df2['address'][j])['address line 2']
        a, b = string_match(df1['name'][i], df2['name'][j])
        e, f = string_match(address1, address2)
        c, d = string_match(str(df1['contact_no']))
        # c, d = string_match(ast.literal_eval(df1['phone'][i])['phone'], ast.literal_eval(df2['phones'][j])['phone'])
        ret_arr = [a, b, c, d, e, f]
        arr.append(ret_arr)

"""""""""uploading data to a csv file"""""""""

with open('google_matrix.txt', 'w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['n12', 'n21', 'p12', 'p21', 'a12', 'a21'])
    for list1 in arr:
        writer.writerow(list1)
