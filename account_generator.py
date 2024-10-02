'''скрипт для генерации списка лицевых счетов и расчета ключа каждого лицевого счета'''
import numpy as np
import pandas as pd

wgh = np.array([7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1]) # веса
print(wgh)
sum_arr = []

# генерация массива из заданного кол-ва лицевых счетов
all_accounts = [i for i in range(47411810045370000001, 47411810045370000100)]

# приводим массив лс к виду, где каждый разряд - отдельный элемент массива
all_acc_share = []
for i in range(len(all_accounts)):
    all_acc_share.extend(map(int, str(all_accounts[i])))    # [4, 7, 4 ...]
# формируем группы по N элементов
n = 20
chunks = np.array([all_acc_share[i:i+n] for i in range(0, len(all_acc_share), n)])
# расчет ключа
sum_arr = chunks * wgh % 10 # получаем младшие разряды
keys = [(4 + sum(sub_list)) % 10 * 3 % 10 for sub_list in sum_arr]

# замена исходных ключей на расчитанные
cnt = 0
for chunk in chunks:
    chunk[8] = keys[cnt]
    cnt +=1
all_accounts = chunks.tolist()

# вывести в excel
df = pd.Dataframe(all_accounts)
writer = pd.ExcelWriter('data.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, sheet_name = 'Лицевые счета', index = False)
writer.save()
