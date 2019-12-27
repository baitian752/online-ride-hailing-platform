import numpy as np


class Hungary(object):

    def __init__(self, cost_matrix):
        self.cost_matrix = np.asarray(cost_matrix).copy()
        self.square_cost_matrix()
        self.n = self.cost_matrix.shape[0]
        self.assignments = None
        self.run()

    def square_cost_matrix(self):
        m, n = self.cost_matrix.shape
        if m < n:
            rows = np.zeros(shape=(n - m, n))
            self.cost_matrix = np.row_stack((self.cost_matrix, rows))
        elif m > n:
            cols = np.zeros(shape=(m, m - n))
            self.cost_matrix = np.column_stack((self.cost_matrix, cols))

    def run(self):
        self.step1()
        self.step2()
        self.step3()

    def step1(self):
        self.cost_matrix -= self.cost_matrix.min(axis=1)[:, np.newaxis]

    def step2(self):
        self.cost_matrix -= self.cost_matrix.min(axis=0)

    def step3(self):
        marked = np.zeros(shape=(self.n, self.n))
        zeros_row = np.sum(self.cost_matrix == 0, axis=1)
        zeros_col = np.sum(self.cost_matrix == 0, axis=0)
        while True:
            repeat = False
            for i in range(self.n):
                if zeros_row[i] == 1:
                    for j in range(self.n):
                        if self.cost_matrix[i, j] == 0 and \
                            marked[i, j] not in [1, -1]:
                            marked[i, j] = 1
                            zeros_row[i] -= 1
                            zeros_col[j] -= 1
                            for k in range(self.n):
                                if self.cost_matrix[k, j] == 0 and \
                                    marked[k, j] not in [1, -1]:
                                    marked[k, j] = -1
                                    zeros_row[k] -= 1
                                    zeros_col[j] -= 1
            for j in range(self.n):
                if zeros_col[j] == 1:
                    for i in range(self.n):
                        if self.cost_matrix[i, j] == 0 and \
                            marked[i, j] not in [1, -1]:
                            marked[i, j] = 1
                            zeros_row[i] -= 1
                            zeros_col[j] -= 1
                            for k in range(self.n):
                                if self.cost_matrix[i, k] == 0 and \
                                    marked[i, k] not in [1, -1]:
                                    marked[i, k] = -1
                                    zeros_row[i] -= 1
                                    zeros_col[k] -= 1
            for i in range(self.n):
                if zeros_row[i] >= 2:
                    repeat = True
                    for j in range(self.n):
                        if self.cost_matrix[i, j] == 0 and \
                            marked[i, j] not in [1, -1]:
                            marked[i, j] = 1
                            zeros_row[i] -= 1
                            zeros_col[j] -= 1
                            for k in range(self.n):
                                if self.cost_matrix[k, j] == 0 and \
                                    marked[k, j] not in [1, -1]:
                                    marked[k, j] = -1
                                    zeros_row[k] -= 1
                                    zeros_col[j] -= 1
                            for m in range(self.n):
                                if self.cost_matrix[i, m] == 0 and \
                                    marked[i, m] not in [1, -1]:
                                    marked[i, m] = -1
                                    zeros_row[i] -= 1
                                    zeros_col[m] -= 1
            for j in range(self.n):
                if zeros_col[j] >= 2:
                    repeat = True
                    for i in range(self.n):
                        if self.cost_matrix[i, j] == 0 and \
                            marked[i, j] not in [1, -1]:
                            marked[i, j] = 1
                            zeros_row[i] -= 1
                            zeros_col[j] -= 1
                            for k in range(self.n):
                                if self.cost_matrix[k, j] == 0 and \
                                    marked[k, j] not in [1, -1]:
                                    marked[k, j] = -1
                                    zeros_row[k] -= 1
                                    zeros_col[j] -= 1
                            for m in range(self.n):
                                if self.cost_matrix[i, m] == 0 and \
                                    marked[i, m] not in [1, -1]:
                                    marked[i, m] = -1
                                    zeros_row[i] -= 1
                                    zeros_col[m] -= 1
            if not repeat:
                break
        if np.sum(marked == 1) == self.n:
            self.assignments = np.argwhere(marked == 1)
        else:
            unmarked_rows = set([item[0] for item in \
                np.argwhere(np.sum(marked == 1, axis=1) == 0)])
            marked_cols = set()
            while True:
                marked_lines_changed = False
                for row in unmarked_rows:
                    for j in range(self.n):
                        if self.cost_matrix[row, j] == 0:
                            if j not in marked_cols:
                                marked_lines_changed = True
                                marked_cols.add(j)
                for col in marked_cols:
                    for i in range(self.n):
                        if marked[i, col] == 1:
                            if i not in unmarked_rows:
                                marked_lines_changed = True
                                unmarked_rows.add(i)
                if not marked_lines_changed:
                    break
            marked_rows = set(range(self.n)).difference(unmarked_rows)
            self.step4(marked_rows, marked_cols)

    def step4(self, marked_rows, marked_cols):
        unmarked_rows = set(range(self.n)).difference(marked_rows)
        unmarked_cols = set(range(self.n)).difference(marked_cols)
        min_cost = self.cost_matrix[list(unmarked_rows), :][:, \
            list(unmarked_cols)].min()
        self.cost_matrix[list(unmarked_rows), :] -= min_cost
        self.cost_matrix[:, list(marked_cols)] += min_cost
        self.step3()


if __name__ == '__main__':
    cost_matrix = [
        [82, 83, 69, 92],
        [77, 37, 49, 92],
        [11, 69, 5, 86],
        [8, 9, 98, 23]
    ]
    hungary = Hungary(cost_matrix=cost_matrix)
    print(hungary.assignments)
