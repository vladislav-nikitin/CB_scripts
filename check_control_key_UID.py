"""скрипт для расчета контрольного ключа УИД в кредитном договоре"""

import re
import numpy as np

uid_number = input("Введите номер УИД кредитного договора: ")
mask = r"[0-9a-f]{8}[-][0-9a-f]{4}[-][0-9a-f]{4}[-][0-9a-f]{4}[-][0-9a-f]{12}[-][0-9a-f]{1}"
values = {"a": "10", "b": "11", "c": "12", "d": "13", "e": "14", "f": "15"}
wgh = []  # список для весовых коэффициентов
# проверка номера УИД на корректность
uid_match = re.fullmatch(mask, uid_number)
print(
    "UID correct" if uid_match else "UID incorrect! Please, write correct UID number!"
)


def uid_transform(uid=uid_number):
    uid_num_without_ = uid_number.replace("-" "")
    uid_num_without_ = uid_num_without_[:-1]
    uid_number_after_change = "".join(
        [values[i] if i in values.keys() else i for i in uid_num_without_]
    )
    # print(type(uid_number_after_change), uid_number_after_change)
    return uid_number_after_change


uid_number_after_change = np.array(
    [int(i) for i in uid_transform()]
)  # УИД для расчетов
# наполняю список весов
counter = 1
for i in range(len(uid_number_after_change) + 1):
    while counter <= 10:
        wgh.append(counter)
        counter += 1
    if counter > 10:
        counter = 1
wgh = np.array(wgh[0 : len(uid_number_after_change)])  # веса для расчетов

control_key = sum(uid_number_after_change * wgh) % 16  # расчет контрольного символа
if control_key < 10:
    uid_number = uid_number[:-1] + str(control_key)
elif control_key >= 10:
    uid_number = uid_number[:-1] + "".join(
        [key for key, val in values.items() if val == str(control_key)]
    )

print("Correct UID number: ", uid_number)
