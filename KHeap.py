import numpy as np


class KHeap:
    def __init__(self, k, num_nodes):
        self.k = k  # Número de filhos por nó
        self.heap = []  # Lista para armazenar os elementos (tuplas: (prioridade, valor))

        # Usa um dicionário esparso para reduzir uso de memória em grafos muito grandes
        self.position = {} if num_nodes > 10 ** 7 else np.full(num_nodes, -1, dtype=np.int32)

        # Contadores das operações
        self.sift_up_count = 0
        self.sift_down_count = 0
        self.insert_count = 0
        self.deletemin_count = 0
        self.update_count = 0
        self.memory_usage = 0

    def parent(self, i):
        return (i - 1) // self.k

    def children(self, i):
        return [self.k * i + j + 1 for j in range(self.k) if self.k * i + j + 1 < len(self.heap)]

    def swap(self, i, j):
        self.position[self.heap[i][1]] = j
        self.position[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def heapify_up(self, i):
        self.sift_up_count += 1
        while i > 0 and self.heap[i][0] < self.heap[self.parent(i)][0]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def heapify_down(self, i):
        self.sift_down_count += 1
        while True:
            smallest = i
            for child in self.children(i):
                if self.heap[child][0] < self.heap[smallest][0]:
                    smallest = child
            if smallest == i:
                break
            self.swap(i, smallest)
            i = smallest

    def push(self, priority, value):
        self.insert_count += 1
        self.heap.append((priority, value))
        self.position[value] = len(self.heap) - 1
        self.heapify_up(len(self.heap) - 1)
        self.memory_usage += 1

    def pop(self):
        self.deletemin_count += 1
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self.position[last[1]] = 0
            self.heapify_down(0)
        if isinstance(self.position, dict):
            self.position.pop(root[1], None)
        else:
            self.position[root[1]] = -1  # Marca como removido
        self.memory_usage -= 1
        return root

    def decrease_key(self, value, new_priority):
        self.update_count += 1
        if value not in self.position or self.position[value] == -1:
            return  # Ignora valores antigos
        i = self.position[value]
        if new_priority < self.heap[i][0]:
            self.heap[i] = (new_priority, value)
            self.heapify_up(i)

    def is_empty(self):
        return len(self.heap) == 0

    def print_operation_counts(self):
        print(f"Operações de 'push': {self.insert_count}")
        print(f"Operações de 'pop': {self.deletemin_count}")
        print(f"Operações de 'decrease_key': {self.update_count}")
        print(f"Operações de 'heapify_up': {self.sift_up_count}")
        print(f"Operações de 'heapify_down': {self.sift_down_count}")
        print(f"Uso de memória (elementos no heap): {self.memory_usage}")
