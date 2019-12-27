import random


class LocalAssignments(object):

    def __init__(self, cost_matrix):
        self.cost_matrix = cost_matrix
        self.m = len(cost_matrix)
        self.n = len(cost_matrix[0])
        self.assignments = [{'jobs': [], 'costs': 0} for _ in range(self.m)]
        self.run()
        
    def run(self):
        self.arbitrary_init()
        self.try_min_cost()

    def arbitrary_init(self):
        for job in range(self.n):
            worker = random.randint(0, self.m - 1)
            self.assignments[worker]['jobs'].append(job)
            self.assignments[worker]['costs'] += self.cost_matrix[worker][job]

    def find_max_cost_index(self):
        index = -1
        cost = 0
        for worker in range(self.m):
            if self.assignments[worker]['costs'] > cost:
                cost = self.assignments[worker]['costs']
                index = worker
        return index

    def try_min_cost(self):
        while True:
            max_cost_index = self.find_max_cost_index()
            job = self.assignments[max_cost_index]['jobs'].pop()
            self.assignments[max_cost_index]['costs'] -= \
                self.cost_matrix[max_cost_index][job]
            index = 0
            cost = self.assignments[0]['costs'] + self.cost_matrix[0][job]
            for worker in range(1, self.m):
                if cost > self.assignments[worker]['costs'] + \
                    self.cost_matrix[worker][job]:
                    cost = self.assignments[worker]['costs'] + \
                        self.cost_matrix[worker][job]
                    index = worker
            self.assignments[index]['jobs'].append(job)
            self.assignments[index]['costs'] += self.cost_matrix[index][job]
            if index == max_cost_index:
                break


if __name__ == '__main__':
    cost_matrix = [
        [82, 83, 69, 92, 47, 87],
        [77, 37, 49, 92, 56, 7],
        [11, 69, 5, 86, 19, 66],
        [8, 9, 98, 23, 22, 42]
    ]
    local_assignments = LocalAssignments(cost_matrix=cost_matrix)
    print(local_assignments.assignments)
