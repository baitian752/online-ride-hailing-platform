import os
import csv


if not os.path.exists('datas'):
    os.mkdir('datas')

with open('uber-raw-data-sep14.csv', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    orders = list(reader)

header = orders[0]
orders_split = [[header] for _ in range(30)]
for order in orders[1:]:
    if order[-1] == 'B02512':
        orders_split[int(order[0].split('/')[1]) - 1].append(order)

for i in range(30):
    with open('datas/orders_9_%s_2014.csv' % (i + 1), 'w', \
        encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(orders_split[i])
