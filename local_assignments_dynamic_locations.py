import os
import random
import json
import csv

from math import floor
from geopy import distance

import matplotlib.pyplot as plt


class LocalAssignments(object):

    def __init__(self, m, orders, num_latest_orders=100):
        self.m = m
        self.n = len(orders)
        self.orders = orders
        self.num_latest_orders = num_latest_orders
        self.distance_matrix = \
            [[0 for j in range(self.n)] for i in range(self.m)]
        self.assignments = [{'orders': [], 'distance (hm)': 0} \
            for _ in range(self.m)]
        self.max_distance = 0
        self.ave_distance = 0
        self.data = None
        self.run()
        
    def run(self):
        self.read_data()
        self.set_init_positions()
        self.calc_distance_matrix()
        self.arbitrary_init()
        self.try_min_distance()
        self.update_data()
        self.write_data()

    def arbitrary_init(self):
        for order in range(self.n):
            vehicle = random.randint(0, self.m - 1)
            self.assignments[vehicle]['orders'].append(order)
            self.assignments[vehicle]['distance (hm)'] += \
                self.distance_matrix[vehicle][order]

    def find_max_distance_index(self):
        index = -1
        distance = 0
        
        for vehicle in range(self.m):
            if self.assignments[vehicle]['distance (hm)'] > distance:
                distance = self.assignments[vehicle]['distance (hm)']
                index = vehicle
        return index

    def try_min_distance(self):
        while True:
            max_distance_index = self.find_max_distance_index()
            order = self.assignments[max_distance_index]['orders'].pop()
            self.assignments[max_distance_index]['distance (hm)'] -= \
                self.distance_matrix[max_distance_index][order]
            index = 0
            distance = self.assignments[0]['distance (hm)'] + \
                self.distance_matrix[0][order]

            for vehicle in range(1, self.m):
                if distance > self.assignments[vehicle]['distance (hm)'] + \
                    self.distance_matrix[vehicle][order]:
                    distance = self.assignments[vehicle]['distance (hm)'] + \
                        self.distance_matrix[vehicle][order]
                    index = vehicle
            self.assignments[index]['orders'].append(order)
            self.assignments[index]['distance (hm)'] += \
                self.distance_matrix[index][order]

            if index == max_distance_index:
                self.max_distance = self.assignments[index]['distance (hm)']
                self.ave_distance = 0
                for vehicle in range(self.m):
                    self.ave_distance += \
                        self.assignments[vehicle]['distance (hm)']
                self.ave_distance /= self.m
                break

    def set_init_positions(self):
        if not self.data['0']['position']:
            min_lat = self.orders[0][0]
            max_lat = min_lat
            min_lon = self.orders[0][1]
            max_lon = min_lon

            for j in range(1, self.n):
                if self.orders[j][0] < min_lat:
                    min_lat = self.orders[j][0]
                if self.orders[j][0] > max_lat:
                    max_lat = self.orders[j][0]
                if self.orders[j][1] < min_lon:
                    min_lon = self.orders[j][1]
                if self.orders[j][1] > max_lon:
                    max_lon = self.orders[j][1]

            for i in range(self.m):
                split_lat = random.randint(0, 100)
                split_lon = random.randint(0, 100)
                self.data[str(i)]['position'] = [
                    min_lat + split_lat / 100 * (max_lat - min_lat),
                    min_lon + split_lon / 100 * (max_lon - min_lon)
                ]

    def calc_distance_matrix(self):
        for i in range(self.m):
            for j in range(self.n):
                self.distance_matrix[i][j] = \
                    floor(distance.geodesic(self.data[str(i)]['position'],
                                            self.orders[j]).kilometers * 10)

    def update_data(self):
        for vehicle in range(self.m):
            for order in self.assignments[vehicle]['orders']:
                self.data[str(vehicle)]['orders'].append(self.orders[order])
            historical_orders = self.data[str(vehicle)]['orders']
            num_orders = len(historical_orders)

            if num_orders > self.num_latest_orders:
                self.data[str(vehicle)]['orders'] = \
                    historical_orders[-self.num_latest_orders:]
                historical_orders = \
                    sum(historical_orders[-self.num_latest_orders:], [])
                lat = sum(historical_orders[0::2]) / self.num_latest_orders
                lon = sum(historical_orders[1::2]) / self.num_latest_orders
                self.data[str(vehicle)]['position'] = [lat, lon]
            elif num_orders > 0:
                historical_orders = sum(historical_orders, [])
                lat = sum(historical_orders[0::2]) / num_orders
                lon = sum(historical_orders[1::2]) / num_orders
                self.data[str(vehicle)]['position'] = [lat, lon]

    def read_data(self, data_path='data.json'):
        if not os.path.exists(data_path):
            data = dict()
            for i in range(self.m):
                data[i] = {
                    'position': [],
                    'orders': []
                }
            with open(data_path, 'w', encoding='UTF-8') as f:
                f.write(json.dumps(data))
        with open(data_path, 'r', encoding='UTF-8') as f:
            data = json.loads(f.read())
        self.data = data

    def write_data(self, data_path='data.json'):
        with open(data_path, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(self.data, indent=4))


if __name__ == '__main__':
    import datetime
    print(datetime.datetime.now())

    if not os.path.exists('results'):
        os.mkdir('results')
    if not os.path.exists('results/assignments'):
        os.mkdir('results/assignments')
    if not os.path.exists('results/figures'):
        os.mkdir('results/figures')
        
    max_distances = []
    ave_distances = []
    for i in range(30):

        with open('datas/orders_9_%s_2014.csv' % (i + 1), 'r', \
            encoding='UTF-8') as f:
            reader = csv.reader(f)
            lines = list(reader)[1:]
            orders = list(map(lambda line: [float(line[1]), float(line[2])], \
                lines))

        local_assignments = LocalAssignments(m=100, orders=orders)
        max_distances.append(local_assignments.max_distance)
        ave_distances.append(local_assignments.ave_distance)
        assignments = dict()

        for j, assignment in enumerate(local_assignments.assignments):
            assignments[j] = assignment

        with open('results/assignments/assignments_9_%s_2014.json' % (i + 1), \
            'w', encoding='UTF-8') as f:
            f.write(json.dumps(assignments, indent=4))

        print(i + 1)
    print(datetime.datetime.now())

    days = list(range(1, 31))

    plt.plot(days, max_distances)
    plt.xticks(days[0::5], [1, 6, 11, 16, 21, 26])
    plt.title('Maximum Distance of All Vehicles')
    plt.xlabel('days (Sep. 2014)')
    plt.ylabel('distance (hm)')
    plt.savefig('results/figures/max_distances_curve.pdf', format='pdf')
    plt.close()

    plt.plot(days, ave_distances)
    plt.xticks(days[0::5], [1, 6, 11, 16, 21, 26])
    plt.title('Average Distance of All Vehicles')
    plt.xlabel('days (Sep. 2014)')
    plt.ylabel('distance (hm)')
    plt.savefig('results/figures/ave_distances_curve.pdf', format='pdf')
    plt.close()
