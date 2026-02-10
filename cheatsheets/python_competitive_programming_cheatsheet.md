# Python Built-in Packages for Competitive Programming

A comprehensive guide to the most useful built-in Python packages for competitive programming contests.

---

## 📦 **collections**

Essential data structures beyond basic lists and dicts.

### **Counter**
```python
from collections import Counter

freq = Counter([1, 2, 2, 3, 3, 3])  # {3: 3, 2: 2, 1: 1}
freq.most_common(2)  # [(3, 3), (2, 2)]
freq['missing_key']  # Returns 0 instead of KeyError
```
**Use cases:** Frequency counting, finding most/least common elements

### **defaultdict**
```python
from collections import defaultdict

graph = defaultdict(list)  # No need to check if key exists
graph[1].append(2)

count = defaultdict(int)  # Auto-initializes to 0
count['a'] += 1
```
**Use cases:** Graphs, grouping, counting without initialization

### **deque**
```python
from collections import deque

dq = deque([1, 2, 3])
dq.appendleft(0)  # O(1) - [0, 1, 2, 3]
dq.popleft()      # O(1) - [1, 2, 3]
dq.rotate(1)      # [3, 1, 2]

# Fixed size deque - automatically removes from opposite end
dq = deque(maxlen=3)
dq.extend([1, 2, 3])  # deque([1, 2, 3])
dq.append(4)          # deque([2, 3, 4]) - 1 auto-removed from left
dq.appendleft(0)      # deque([0, 2, 3]) - 4 auto-removed from right
```
**Use cases:** Queue, BFS, sliding window, double-ended operations, fixed-size buffers

### **OrderedDict**
```python
from collections import OrderedDict

od = OrderedDict([('a', 1), ('b', 2)])
od.move_to_end('a')  # {'b': 2, 'a': 1}
od.popitem(last=False)  # Remove from beginning
```
**Use cases:** LRU cache implementation, maintaining insertion order (pre-Python 3.7)

---

## 🔄 **itertools**

Efficient iteration tools for combinatorics and sequences.

### **Combinatorics**
```python
from itertools import permutations, combinations, combinations_with_replacement, product

list(permutations([1, 2, 3], 2))              # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
list(combinations([1, 2, 3], 2))              # [(1,2), (1,3), (2,3)]
list(combinations_with_replacement([1, 2], 2)) # [(1,1), (1,2), (2,2)]
list(product([1, 2], [3, 4]))                 # [(1,3), (1,4), (2,3), (2,4)]
```
**Use cases:** Generating all possible arrangements, subset enumeration

### **Iteration Tools**
```python
from itertools import accumulate, chain, groupby, islice, cycle, repeat

list(accumulate([1, 2, 3, 4]))        # [1, 3, 6, 10] - cumulative sums
list(chain([1, 2], [3, 4]))           # [1, 2, 3, 4] - flatten iterables
list(islice(range(10), 2, 8, 2))      # [2, 4, 6] - slice iterator
list(zip(*[iter([1,2,3,4])]*2))       # [(1,2), (3,4)] - chunk into pairs

# groupby - group consecutive identical elements
from itertools import groupby
for key, group in groupby('AAABBBCC'):
    print(key, list(group))  # A ['A','A','A'], B ['B','B','B'], C ['C','C']
```
**Use cases:** Prefix sums, run-length encoding, chunking, infinite sequences

---

## 🏔️ **heapq**

Min-heap implementation for priority queues.

### **Basic Property**
**Min-heap:** Binary tree where each parent ≤ its children. The **smallest element is always at the root** (index 0).
- Stored as array: Parent at `i`, children at `2*i+1` and `2*i+2`
- **Push:** Add element at end, "bubble up" to maintain heap property - O(log n)
- **Pop:** Remove root (min), move last element to root, "bubble down" - O(log n)

```python
import heapq

heap = []
heapq.heappush(heap, 3)    # Insert: [3]
heapq.heappush(heap, 1)    # Insert: [1, 3] - 1 bubbles up
heapq.heappush(heap, 2)    # Insert: [1, 3, 2]

heapq.heappop(heap)        # 1 (always min) - 2 moves to root, bubbles down
heap[0]                    # Peek at min without popping

heapq.heapify([3, 1, 2])   # Convert list to heap in-place O(n)

# For max-heap, negate values
heapq.heappush(heap, -value)
max_val = -heapq.heappop(heap)

# Get k largest/smallest
heapq.nlargest(3, [1, 5, 2, 9, 3])   # [9, 5, 3]
heapq.nsmallest(3, [1, 5, 2, 9, 3])  # [1, 2, 3]
```

### **Merge K Sorted Lists Example**
```python
def merge_k_sorted(lists):
    heap = []
    result = []

    # Initialize heap with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))  # (value, list_idx, elem_idx)

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result

# Example usage
lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
merge_k_sorted(lists)  # [1, 1, 2, 3, 4, 4, 5, 6]
```

**Use cases:** Dijkstra's algorithm, merge k sorted arrays, finding k-th element, priority tasks

---

## 🔍 **bisect**

Binary search and insertion in sorted sequences.

### **Efficient Sorting First**
```python
# Sort a list efficiently - O(n log n)
arr = [3, 1, 4, 1, 5]
sorted_arr = sorted(arr)        # Returns new sorted list: [1, 1, 3, 4, 5]
arr.sort()                      # Sort in-place: [1, 1, 3, 4, 5]

# Sort with key function
sorted(['abc', 'a', 'abcd'], key=len)  # ['a', 'abc', 'abcd']
sorted([3, -1, -5, 2], key=abs)        # [-1, 2, 3, -5]

# Reverse sort
sorted(arr, reverse=True)       # [5, 4, 3, 1, 1]
```

### **Binary Search with Bisect**
```python
import bisect

arr = [1, 3, 4, 4, 6]

bisect.bisect_left(arr, 4)   # Returns index 2 (leftmost position where 4 exists)
bisect.bisect_right(arr, 4)  # Returns index 4 (rightmost position + 1)
bisect.bisect(arr, 4)        # Same as bisect_right

bisect.insort_left(arr, 5)   # Insert maintaining sorted order
# arr = [1, 3, 4, 4, 5, 6]

# Custom binary search
def count_occurrences(arr, x):
    left = bisect.bisect_left(arr, x)    # Returns index
    right = bisect.bisect_right(arr, x)  # Returns index
    return right - left
```
**Use cases:** Binary search, finding insertion point, range queries on sorted data

---

## 🧮 **math**

Mathematical functions and constants.

```python
import math

# Common functions
math.gcd(48, 18)              # 6 - Greatest Common Divisor
math.lcm(4, 6)                # 12 - Least Common Multiple (Python 3.9+)
math.factorial(5)             # 120
math.comb(5, 2)               # 10 - Combinations (Python 3.8+)
math.perm(5, 2)               # 20 - Permutations (Python 3.8+)

# Powers and logs
math.isqrt(17)                # 4 - Integer square root (Python 3.8+)
math.sqrt(16)                 # 4.0
math.pow(2, 10)               # 1024.0
math.log2(8)                  # 3.0

# Rounding
math.ceil(3.2)                # 4
math.floor(3.8)               # 3

# Constants
math.pi                       # 3.141592653589793
math.e                        # 2.718281828459045
math.inf                      # Infinity
```
**Use cases:** Number theory, geometry, probability calculations

---

## ⚡ **functools**

Higher-order functions and memoization.

### **lru_cache (Memoization)**
```python
from functools import lru_cache

@lru_cache(maxsize=None)  # Unlimited cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci.cache_info()     # View cache statistics
fibonacci.cache_clear()    # Clear cache
```

### **Other Tools**
```python
from functools import reduce, cmp_to_key

# reduce - apply function cumulatively
reduce(lambda x, y: x * y, [1, 2, 3, 4])  # 24

# Custom comparison for sorting
def compare(a, b):
    return (a > b) - (a < b)

sorted([3, 1, 2], key=cmp_to_key(compare))
```
**Use cases:** Dynamic programming, custom sorting, functional programming

---

## 💬 **re** (Regular Expressions)

Pattern matching and text processing.

```python
import re

re.findall(r'\d+', 'a1b22c333')           # ['1', '22', '333']
re.split(r'\s+', 'a  b   c')              # ['a', 'b', 'c']
re.sub(r'\d+', 'X', 'a1b2c3')             # 'aXbXcX'

# Check if matches
re.match(r'^\d+$', '123')                 # Matches at start
re.search(r'\d+', 'abc123')               # Searches anywhere
re.fullmatch(r'\d+', '123')               # Must match entire string

# Common patterns
# \d - digit, \w - word char, \s - whitespace
# + - one or more, * - zero or more, ? - zero or one
# ^ - start, $ - end
```
**Use cases:** Parsing input, string validation, tokenization

---

## ⌨️ **sys**

System-specific parameters and I/O optimization.

```python
import sys

# Fast input (crucial for large inputs)
input = sys.stdin.readline  # Much faster than input()

# Fast output (for multiple prints)
print = sys.stdout.write    # Use with '\n' manually

# Read all at once
lines = sys.stdin.read().splitlines()

# Set recursion limit (for deep DFS)
sys.setrecursionlimit(10**6)

# Exit with code
sys.exit(0)

# Max integer
sys.maxsize  # 2^63 - 1 on 64-bit systems
```
**Use cases:** Speed optimization, handling large I/O, deep recursion

---

## 🔤 **string**

String constants and utilities.

```python
import string

string.ascii_lowercase       # 'abcdefghijklmnopqrstuvwxyz'
string.ascii_uppercase       # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
string.ascii_letters         # 'abcd...xyzABCD...XYZ'
string.digits                # '0123456789'
string.hexdigits             # '0123456789abcdefABCDEF'
string.punctuation           # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
string.whitespace            # ' \t\n\r\x0b\x0c'

# Quick character checks
char in string.ascii_letters
char.isalpha() / char.isdigit() / char.isalnum()
```
**Use cases:** Character set checking, alphabet mappings

---

## 📊 **array**

Space-efficient arrays for numeric types.

```python
from array import array

# 'i' for signed int, 'd' for double, 'b' for byte
arr = array('i', [1, 2, 3, 4])

arr.append(5)
arr.extend([6, 7])
arr.pop()

# More memory efficient than lists for large numeric arrays
```
**Use cases:** Memory optimization for large numeric data

---

## 🎯 **operator**

Standard operators as functions.

```python
from operator import add, mul, itemgetter, attrgetter

# Useful with reduce/map
from functools import reduce
reduce(mul, [1, 2, 3, 4])  # 24

# Sorting by multiple keys
students = [('Alice', 25), ('Bob', 20), ('Charlie', 25)]
sorted(students, key=itemgetter(1, 0))  # Sort by age, then name
```
**Use cases:** Functional programming, custom sorting

---

## 📝 **Quick Tips**

### Template for Fast I/O
```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    # Your solution here

if __name__ == "__main__":
    main()
```

### Common Patterns
```python
# Reading multiple test cases
for _ in range(int(input())):
    # solve each test case

# Grid input
grid = [list(input().strip()) for _ in range(n)]

# Multiple integers on one line
a, b, c = map(int, input().split())

# Infinity values
INF = float('inf')
NEG_INF = float('-inf')
```

---

## 🏆 **Pro Tips**

1. **Use `bisect` instead of manual binary search** - Less error-prone
2. **`collections.Counter`** beats manual frequency dictionaries
3. **`functools.lru_cache`** for instant DP memoization
4. **`sys.stdin.readline`** for competitive programming I/O
5. **`itertools.accumulate`** for prefix sums in one line
6. **`collections.deque`** for O(1) operations on both ends
7. **Negative values in heapq** for max-heap behavior
8. **`math.gcd` can take multiple args** with `reduce(math.gcd, [a, b, c])`

Happy coding! 🚀
