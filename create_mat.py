import pandas as pd
import csv

df1 = pd.read_csv('indiacom_matrix.txt', sep=',')
# df1 = pd.read_csv('grotal_matrix.txt', sep=',')
# df3 = pd.read_csv('google_matrix.txt', sep=',')

a = df1.sample(n=26)
random = zip(a['n12'].values.tolist(), a['n21'].values.tolist(), a['p12'].values.tolist(), a['p21'].values.tolist(), a['a12'].values.tolist(), a['a21'].values.tolist(), [0 for i in range(len(a))])

with open('match_matrix.txt', 'a+') as file:
    writer = csv.writer(file, delimiter=',')

    """""""""random data"""""""""

    # writer.writerow(['n12', 'n21', 'p12', 'p21', 'a12', 'a21', 'bin'])
    # for i in random:
    #     writer.writerow(i)

    """""""""better data"""""""""

    # count = 0
    # for i in random:
    #     if ((i[0] > 0 and i[0] < 50) or (i[1] > 0 and i[1] < 50)) and ((i[4] > 0 and i[4] < 50) or (i[5] > 0 and i[5] < 50)):
    #         writer.writerow(i)
    #         count += 1
    #     if count == 26:
    #         break

    """"""""""positive data phone"""""""""""
    # for i in random:
    #     if i[2] > 0 or i[3] > 0:
    #         writer.writerow(i)

    """""""positive data name"""""""""
    # for i in random:
    #     if (i[0] == 100.0 or i[1] == 100.0) and (i[4] > 30 or i[5] > 30) and (i[2] != 0 and i[3] != 0):
    #         writer.writerow(i)
