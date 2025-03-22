class KHeap:
    def __init__(self, k):
        self.k = k  # Número de filhos por nó
        self.heap = []  # Lista para armazenar os elementos (tuplas: (prioridade, valor))
        self.position = {}  # Mapeia um valor para sua posição no heap (usado por decrease_key)

        # Contadores das operações
        self.sift_up_count = 0
        self.sift_down_count = 0
        self.insert_count = 0
        self.deletemin_count = 0
        self.update_count = 0

    def parent(self, i):
        """Retorna o índice do nó pai."""
        return (i - 1) // self.k

    def children(self, i):
        """Retorna os índices dos filhos do nó na posição i."""
        return [self.k * i + j + 1 for j in range(self.k) if self.k * i + j + 1 < len(self.heap)]

    def swap(self, i, j):
        """Troca dois elementos no heap e atualiza suas posições."""
        self.position[self.heap[i][1]] = j
        self.position[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def heapify_up(self, i):
        """Sobe o elemento para manter a propriedade do heap."""
        self.sift_up_count += 1  # Contador para sift-up
        while i > 0 and self.heap[i][0] < self.heap[self.parent(i)][0]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def heapify_down(self, i):
        """Desce o elemento para manter a propriedade do heap."""
        self.sift_down_count += 1  # Contador para sift-down
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
        """Insere um elemento no heap."""
        self.insert_count += 1  # Contador para push
        self.heap.append((priority, value))
        self.position[value] = len(self.heap) - 1
        self.heapify_up(len(self.heap) - 1)

    def pop(self):
        """Remove e retorna o menor elemento do heap."""
        self.deletemin_count += 1  # Contador para deletemin
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self.position[last[1]] = 0
            self.heapify_down(0)
        if root[1] in self.position:
            del self.position[root[1]]
        return root

    def decrease_key(self, value, new_priority):
        """Diminui a chave de um valor específico no heap."""
        self.update_count += 1  # Contador para update
        if value not in self.position:
            raise KeyError(f"Value {value} not found in heap")
        i = self.position[value]
        if new_priority < self.heap[i][0]:  # Se a nova prioridade for menor
            self.heap[i] = (new_priority, value)
            self.heapify_up(i)

    def is_empty(self):
        """Retorna True se o heap estiver vazio."""
        return len(self.heap) == 0

    def print_operation_counts(self):
        """Imprime o número de vezes que cada operação foi chamada."""
        print(f"Operações de 'push': {self.insert_count}")
        print(f"Operações de 'pop': {self.deletemin_count}")
        print(f"Operações de 'decrease_key': {self.update_count}")
        print(f"Operações de 'heapify_up': {self.sift_up_count}")
        print(f"Operações de 'heapify_down': {self.sift_down_count}")
