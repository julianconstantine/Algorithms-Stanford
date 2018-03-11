class Heap:
    def __init__(self):
        self.key_array = []

    def __repr__(self):
        return str(self.key_array)

    def __getitem__(self, item):
        if item is None:
            return float('-inf')
        else:
            return self.key_array[item]

    def __setitem__(self, key, value):
        self.key_array[key] = value

    def get_parent(self, x):
        if x == 0:
            return None
        else:
            return (x - 1)// 2

    def get_children(self, x):
        left = 2*x + 1  # Left child
        right = left + 1  # Right child

        if left > len(self.key_array) - 1:
            return None, None
        elif left < len(self.key_array) - 1 < right:
            return left, None
        else:
            return left, right

    def bubble_down(self, current, left, right):
        if left is None and right is None:
            bubble_down = False
        elif left is None and right is not None:
            if self[current] < self[right]:
                bubble_down = True
            else:
                bubble_down = False
        elif right is None and left is not None:
            if self[current] > self[left]:
                bubble_down = True
            else:
                bubble_down = False
        else:
            if self[current] > self[left] or self[current] < self[right]:
                bubble_down = True
            else:
                bubble_down = False

        return bubble_down

    def insert(self, x):
        self.key_array.append(x)

        current = len(self.key_array) - 1

        parent = self.get_parent(current)

        while self[current] < self[parent]:
            # Swap current with parent
            self[current], self[parent] = self[parent], self[current]

            # Set new current node to old parent node
            # NOTE: The key of current will remain the same, since we swapped it with parent
            current = parent

            parent = self.get_parent(current)

    def extract_min(self):
        # Swap root node with last node
        self[0], self[-1] = self[-1], self[0]

        # Remove the root node (now in the last position)
        root_key = self.key_array.pop()

        # Initiliaze current node to position 0
        current = 0

        # left = 2*(current + 1)  # Left child
        # right = left + 1  # Right child
        left, right = self.get_children(current)

        # current_key = self[current]
        # left_key = self[left]
        # right_key = self[right]

        # Bubble down
        print(left, current, right)

        while self.bubble_down(current, left, right):

            if self[current] > self[left]:
                self[current], self[left] = self[left], self[current]
                print(self.key_array)
                current = left
            else:
                self[current], self[right] = self[right], self[current]
                print(self.key_array)
                current = right

            # left = 2 * (current + 1)
            # right = left + 1
            left, right = self.get_children(current)

            print(left, current, right)

            # current_key = self.key_array[current]
            # left_key = self.key_array[left]
            # right_key = self.key_array[right]

        return root_key


class DirectedGraph:
    def __init__(self, adjacency_list):
        self.adj_list = adjacency_list
        self.explored = {key: False for key in self.adj_list.keys()}
        self.vertices = set([v for v in self.adj_list])

    def __getitem__(self, item):
        return self.adj_list[item]

    def __repr__(self):
        return str(self.adj_list)

    def exploreVertex(self, vertex):
        # Mark vertex as explored
        self.explored[vertex] = True

    def isExplored(self, vertex):
        # Check if vertex has been explored
        return self.explored[vertex]


# TEST CASES: HEAP
import heapq

# Test the Insert() method by comparing to Python's heapq.heappush()
hq = []                     # []
heapq.heappush(hq, 0)
hq                          # [0]
heapq.heappush(hq, 1)
hq                          # [0, 1]
heapq.heappush(hq, 2)
hq                          # [0, 1, 2]
heapq.heappush(hq, 9)
hq                          # [0, 1, 2, 9]
heapq.heappush(hq, 5)
hq                          # [0, 1, 2, 9, 5]
heapq.heappush(hq, 12)
hq                          # [0, 1, 2, 9, 5, 12]
heapq.heappush(hq, 6)
hq                          # [0, 1, 2, 9, 5, 12, 6]
heapq.heappush(hq, 3)
hq                          # [0, 1, 2, 3, 5, 12, 6, 9]
heapq.heappush(hq, 15)
hq                          # [0, 1, 2, 3, 5, 12, 6, 9, 15]
heapq.heappush(hq, 4)
hq                          # [0, 1, 2, 3, 4, 12, 6, 9, 15, 5]
heapq.heappush(hq, 7)
hq                          # [0, 1, 2, 3, 4, 12, 6, 9, 15, 5, 7]
heapq.heappush(hq, 8)
hq                          # [0, 1, 2, 3, 4, 8, 6, 9, 15, 5, 7, 12]

heapq.heappop(hq)

h = Heap()
h                           # []
h.insert(0)
h                           # [0]
h.insert(1)
h                           # [0, 1]
h.insert(2)
h                           # [0, 1, 2]
h.insert(9)
h                           # [0, 1, 2, 9]
h.insert(5)
h                           # [0, 1, 2, 9, 5]
h.insert(12)
h                           # [0, 1, 2, 9, 5, 12]
h.insert(6)
h                           # [0, 1, 2, 9, 5, 12, 6]
h.insert(3)
h                           # [0, 1, 2, 3, 5, 12, 6, 9]
h.insert(15)
h                           # [0, 1, 2, 3, 5, 12, 6, 9, 15]
h.insert(4)
h                           # [0, 1, 2, 3, 4, 12, 6, 9, 15, 5]
h.insert(7)
h                           # [0, 1, 2, 3, 4, 12, 6, 9, 15, 5, 7]
h.insert(8)
h                           # [0, 1, 2, 3, 4, 8, 6, 9, 15, 5, 7, 12]

h.extract_min()