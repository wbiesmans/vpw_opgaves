Important String Functions and Techniques


    Important character/string manipulation functions

    Most string manipulation functions (that change string) return a new string and do not change the original string. So make sure that it is assigned to a variable.
    ord function takes a single string character as input and returns its Unicode code presentation. Unicode code presentation is the integer representation of the character in Python’s Unicode table (similar to the ASCII table).


```python
# For removing whitespace
s = " utsav programs "
sls = s.lstrip() # Removes space from left end
srs = s.rstrip() # Removes space from right end
ss = s.strip() # Removes space from both ends but not from the middle

# For splitting string into list based on delimiter
s = "I am learning python. I can do it in a day."
l = s.split() # default delimiter is space
l = s.split(".")

# Joining list of strings to single string
# Without any delimeter
x = "".join(["I", "am", "learning", "python"]) # Returns "Iamlearningpython"
# With delimeter
x = " ".join(["I", "am", "learning", "python"]) # Returns "I am learning python"

# Converting to lower and upper case
# Returns new string without changing original string
s = "utsav"
lower_case_s = s.lower()
upper_case_s = s.upper()

# All is___ kind of function returns boolean value

# To check if string has all characters as either digit or alphabet
x = s.isalnum()

# To check if string has all alphabets
x = s.isalpha()

# To check if string has all digits
x = s.isnum()

# To check if string has all spaces
x = isspace()

# Get unicode/ascii representation of character
x = ord("b") # Returns 98
```
    
String : Behaviour as list of characters


```python
s = "utsav"

# Iterating
for char in s:
    print(char)

# Iterating with index
for i, char in enumerate(s):
    print(f"Index : {i}, Char: {char}")

# Slicing
x = s[2:4] # Return "sa"

# Sorting
x = sorted(s) # Returns ['a', 's', 't', 'u', 'v']
x = sorted(s, reverse=True) # Returns ['v', 'u', 't', 's', 'a']

# Membership check
"a" in "utsav" # Returns True
```

    Counting frequency of characters



    Counter is very similar to a dictionary. So it allows functions like keys(), values(),items() and iterating as well as checking membership like a dictionary.
    Once Counter object is prepared, it is detached from its origin (i.e. string). So we can update the frequency of characters or even remove characters just like a dictionary.


```python
from collections import Counter

c = Counter("utsavvv") # Counter({'v': 3, 'u': 1, 't': 1, 's': 1, 'a': 1})
for k, v in c.items():
    print(f"Char: {k}, Frequency: {v}")

# Membership checking
x = "v" in c

# Updating frequency

c["v"] = 1

# Removing character

del c["v"]
   
```
    String comparison and substrings

    Comparison operators allow comparing strings based on the lexicographic order of strings.
    find() returns the start index of the FIRST INSTANCE of the substring and returns -1 if the substring is not found.


```python
# Comparison operators
s1 = "hello"
s2 = "world"

s1 == s2 # Returns False

s1 != s2 # Returns True
s1 < s2 # Returns True
s1 <= s2 # Returns True
s1 > s2 # Returns False
s1 >= s2 # Returns False

# Prefix and Suffix Check
s = "prefix"

# To check if string contains pre as prefix
x = s.startswith("pre") #Returns True

# To check if string contains fix as suffix
x = s.endswith("fix") #Returns True

# Finding substring
s1 = "hello world programming"
subs1 = "world"
start_index = s1.find(subs1) # Returns 6
if start_index != -1:
  substr = s1[start_index:start_index+len(subs1)]
else:
  print(f"{subs1} is not found in {s1}")
```

Important Number Functions and Techniques

```python
# Finding minimum and maximum
x = min(1,2,3) # Returns 1
x = min([1,2,3]) # Returns 1
y = max(1,2,3) # Returns 3
y = max([1,2,3]) # Returns 3

# Sum only accepts list
s = sum([1,2,3]) # Returns 6

# Absolute value
s = abs(-1) # Returns 1

# Swapping values of two variables
a, b = 5, 3
a, b = b,a

```
    Math functions


```python
import math

# Find power / exponential
base = 2
power = 2
p = math.pow(base, power) # Returns 4.0 (float)
p = 2**2

# Round up to nearest integer
x = math.ceil(2.6) # Returns 3

# Round down to nearest integer
x = math.floor(2.6) # Returns 2

# Find square root
x = math.sqrt(2) # Returns 1.4142135623730951

# Find factorial (useful for permutation and combination formulas)
x = math.factorial(5) # Returns 120

n, r = 5, 2

num_perms = math.factorial(n) / math.factorial(n-r)
num_combs = math.factorial(n) / (math.factorial(n-r) * math.factorial(r))
```
    Random functions


```python
import random

# Returns random integer between 1 and 10 (including 1 and 10)
x = random.randint(1,10)

# Returns randomly selected element from list
choices = ["apple", "banana", "cherry"]
x = random.choice(choices)
```
    Bitwise operators

```python
a = 5  # 0101 in binary
b = 3  # 0011 in binary

# Bitwise AND
x = a & b  # Output: 1 (0001 in binary)

# Bitwise OR
x = a | b  # Output: 7 (0111 in binary)

# Bitwise XOR
x = a ^ b  # Output: 6 (0110 in binary)

# Bitwise NOT / Flipping all bits / two's complement
x = ~a  # Output: -6 = -a-1 (1010 in binary)

# Bitwise LEFT SHIFT / Divide by 2
x = a << 1 # Output: 10 (1010 in binary)

# Bitwise RIGHT SHIFT / Multiply by 2
x = a >> 1  # Output: 2 (0010 in binary)

# Check if number is ODD
if a & 1 == 1:
  print(f"{a} is odd")
else:
  print(f"{a} is even")
```


    Division operators

    The / operator performs true divisionand returns a floating-point result.
    The // operator performs floor divisionand returns the largest integer less than or equal to the result.
    The result of the modulo operation has the same sign as the divisor (i.e. denominator). The formula to determine the result is: a % b = a - (a // b) * b

```python
x = 5/2  # 2.5
x = int(5/2) # 2
x = 4/2  # 2.0

x = 5//2 # 2
x = 4//2 # 2
x = 5.0//2 # 2.0

x = 5/-2 # -2.5
x = -5/2 # -2.5

x = 5//-2 # -3 (since -3 is less than -2.5)
x = -5//2 # -3 (since -3 is less than -2.5)

x = 5 % -2   # -1 (because 5 - (-3 * -2) = 5 - 6 = -1)
x = -5 % 2   # 1 (because -5 - (-3 * 2) = -5 - (-6) = 1)

# Get quotient and remainder/modulo in a single operation


quotient, modulo = divmod(23, 10) # Returns (2,3)
quotient, modulo = 23//10, 23%10
```
Important List Functions


    Defining and accessing list



    Slicing (: operator) always returns a new copy of the list. That means it has the complexity of O(n). So use it cautiously.
    Remember, in slicing (e.g. l[si: ei]), an element at start_index is INCLUDED and an element at end_index is EXCLUDED.
    (Amortized) Time complexity for insert and pop function is O(n) unless insertion or removal is done at/from the end. This is because we need to shift elements after forward/backward for these operations.


```python
# Defining empty list
l = []
l = list()

# Adding a single element at the end

l.append(1)

# Extending an existing list
l.extend([2,3]) # Changes l to [1,2,3]

# Inserting an element at specific index
l.insert(1, 100)

# Removing a single element from the end
x = l.pop()

# Removing an element from specific index
x = l.pop(2)

# Merging two lists (does not change existing list)
x = l + [4,5] # Returns [1,2,3,4,5]

# Removing first occurance of an element

l.remove(2)

# Getting sublist
l = [0,1,2,3,4,5,6]
l1 = l[2:4]  # Returns [2,3]

# Quickly make a copy of list
l1 = l[:]

# Swapping two elements

l[0], l[2] = l[2], l[0]
```
Remember, the Opposite of `insert` is `pop` and not `remove` because `insert` and `pop` works at the index level while `remove` works at the value level.


    Initializing list


```python
# Initializing
l = list({"a"}) # From set -> ["a"]

d = {"a": 1, "c": 2}
l = list(d) # From dict keys -> ["a", "c"]
l = list(d.keys()) # From dict keys -> ["a", "c"]
l = list(d.values()) # From dict values -> [1,2]
l = list(d.items()) # From dict key-values -> [("a", 1), ("c", 2)]
l = [1]*n # List with 1 repeated n times
l = list(range(10)) # Returns [0,1,2,3..,8,9]

# List comprehension : Preparing list from another iterable
l = [x+1 for x in nums]
```

    Iterating over list

    Traverse the list in reverse by using ~i as ~i = -i-1 (0 -> -1, 1 -> -2 ..)
    If two lists have different lengths then zip iterates till a shorter length.

```python
nums = [5,1,4,9,8]

# Iterating over list
for n in nums:
  print(n)

# Iterating with index
for i, n in enumerate(nums):
    print(f"Index: {i} , number: {n}")

# Iterating over range
for i in range(n):
    print(i)

# Iterating over range with step size = 2
for i in range(0,n,2):
    print(i)

# Iterating in reverse

# Option 1
for i in range(len(nums)):
    print(nums[~i])

# Option 2
for i in range(len(nums), -1, -1):
    print(nums[i])
    
# Two pointer (left and right end) iteration
for i in range(len(nums)//2):
    print(i) # 0,1,2
    print(~i) # -1 (i.e. 4), -2 (i.e. 3), -3(i.e. 2)

# Iterate over two lists
for x, y in zip(l1, l2):
    print(x)
    print(y)
for i, (x, y) in enumerate(zip(l1,l2)):
    print(f"Index: {i}, x: {x}, y: {y}")

# Safely removing element from list while iterating
nums = [1,2,3,4]
for n in nums[:]:
    if n % 2 == 0:
        nums.remove(n)
```
NEVER remove an element while iterating over a list. If required, copy a list and then remove it from the original one

    Sorting list

    sort is an in-place sorting and sorted returns copy.
    Both sort and sorted supports reverse and key arguments.
```python
nums = [5,1,4,9,8]

# In-place sorting
nums.sort() # Ascending order
nums.sort(reverse=True) # Descending order

# Getting new sorted list
new_nums = sorted(nums) # Ascending order
new_nums = sorted(nums, reverse=True) # Descending order

# Sorting list with custom lambda function (supported by sort and sorted)

# Example 1
nums = [1,-1,3,2,-3,-4]
nums.sort(key=abs) # Sort based on absolute value

# Example 2
nums = ["apple", "banana", "cherry"]
nums.sort(key=len) # Sort based on length

# Example 3 (list of tuples)
nums = [(0,1), (3,1), (1,2)]
nums.sort(key = lambda x : x[1]) # Sorts based on first element

# Example 4 (list of dictionaries)
nums = [{"age": 18, "name": "x"}, {"age": 12, "name": "y"}]
nums.sort(key = lambda x: x["age"]) # Sorts based age
```
    Counting frequency of elements

    It is a useful approach when you want to create frequency hashtable from a list quickly.
    Counter is very similar to a dictionary. So it allows functions like keys(), values(),items() and iterating as well as checking membership like a dictionary.
    Once Counter object is prepared, it is detached from its origin (i.e. list). So we can update the frequency of elements or even remove elements just like a dictionary.
```python
from collections import Counter

c = Counter([1,2,4,1,2,5]) # Counter({1: 2, 2: 2, 4: 1, 5: 1})
for k, v in c.items():
    print(f"Element: {k}, Frequency: {v}")

# Membership checking
x = 1 in c

# Updating frequency
c[1] = 1

# Removing character
del c[1]
```
    Binary Search

    bisect_left and bisect_right only works on a sorted list.
    bisect_left and bisect_right both return an index where the element should be inserted.
    If the element is already present in the list, bisect_left returns index before (to the left of) any existing entries and bisect_right returns index after (to the right of) any existing entries.
    If the element is already present then bisect_left returns index of the first occurrence of that element and bisect_right returns 1 + index of the last occurrence of that element.
    If you search for an element greater than the greatest element then both functions return index = length of list
    Get Utsav Chokshi’s stories in your inbox

    Join Medium for free to get updates from this writer.
    If you search for an element smaller than the smallest element then both functions return index = 0
```python
from bisect import bisect_left, bisect_right

l = [1,2,2,3,4]
x = bisect_left(l, -1) # Returns 0
x = bisect_right(l, -1) # Returns 0

x = bisect_left(l, 10) # Returns 5
x = bisect_right(l, 10) # Returns 5

x = bisect_left(l, 2) # Returns 1 (index of first occurence of 2)
x = bisect_right(l, 2) # Returns 3 (1 + index of last occurence of 2)

# For normal binary search usecases, use following code
target = 3
x = bisect_left(l, target)
if x != len(l) and l[x] == target:
    print(f"Target : {target} is found at index : {x}")
```
    Miscelleneous Operators/Functions on List/Iterables

    all returns True if all values passed to it are: TRUTHY (i.e. True, 1, non-empty list/string/tuple/dictionary)
    any returns True if at least one value passed to it is : TRUTHY
```python
# Check if list has all even numbers
output = all(x%2 == 0 for x in nums)

# Check if list has one or more zero value
output = any(x == 0 for x in nums)

# Check if string is palindrome
is_pal = all(s[i] == s[~i] for i in range(len(s)//2)
```
    Each combination/permutation is a tuple.
    Combination: Order does not matter.
    Permutation: Order matters.
```python
from itertools import permutations, combinations

items = ["A", "B", "C"]

# Iterate over all combinations of length 2
# This is same as nC2 : Picking 2 elements out of given elements
for c in combinations(items, 2):
    print(c) # Prints ("A", "B"), ("A", "C"), ("B", "C")

# Iterate over all permutations
for p in permutations(items):
    print(p)

# Iterate over all permutations of length 2
for p in permutations(items, 2):
    print(p)
```
Important Dict & DefaultDict Functions

    From python 3.7 onwards, Dictionary acts as OrderedDict so it maintains Insertion Order.
    Every key of dict & defaultdict has to be hashable. So list can not be used as a key but tuple can be.

    Defining and accessing dict
```python
# Defining empty dict
d = {}
d = dict()

# Add/Update value against key
d["a"] = 1

# Get value of key
x = d["a"] # Raises KeyError if key is not present
x = d.get("a", None) # Returns default value if key is not present

# Get a value and delete key
if "a" in d:
   x = d.pop("a")

# Delete key
if "a" in d:
  del d["a"]

# Sorting returns sorted keys
sorted_Keys = sorted({"x": 1, "a": 2}) # Returns ["a", "x"]

# Pop first inserted key
d.pop(next(iter(d)))
```
    Initializing dict & defaultdict

    defaultdict returns a default value if the key is not present rather than raising KeyError
    Argument passed to defaultdicthas to be callable. If the function is passed then that function has to take ZERO arguments.
```python
from collections import defaultdict

# initializes non-present key with value 0
d = defaultdict(int)

# initializes non-present key with value 1
d = defaultdict(lambda : 1)

# initializes non-present key with empty list ([])
d = defaultdict(list)

# initializes non-present key with empty dict ({})
d = defaultdict(dict)

# Dictionary comprehension : Preparing dict from another iterable
d = { x : x%2 == 0 for x in nums }

# Create a dictionary from list/tuple of 2 length strings
d = dict(['()', '[]', '{}']) # Returns {'(': ')', '[': ']', '{': '}'}
```
    Iterating over dictionary

    For iteration, defaultdict's behavior is the same as dict
```python
d = {"a": 1, "b": 1}

# Iterating over key-value pairs
for k, v in d.items():
    print(f"Key: {k}, Value: {v}")

# Iterating over keys
for k in d.keys():
    print(f"Key: {k}")

# Iterating over values
for v in d.values():
    print(f"Value: {v}")

# Iterating with index
for i, (k,v) in enumerate(d.items()):
    print(f"Key: {k}, Value: {v}")

for i, k in enumerate(d.keys()):
    print(f"Key: {k}")

for i, v in enumerate(d.values()):
    print(f"Value: {v}")

# Safely removing key from dict while iterating
for k in list(d.keys()):
    if k == "a"
        del d["a"]
```
NEVER remove a key while iterating over a dict. If required, copy keys as a list and then remove it from the original one
Important Tuple Functions

    Tuples are immutable and can be used as dictionary keys or set elements.
    Whenever a function returns multiple values, it is returned as a tuple of values. Hence, the caller can unpack those values.
    From the functions aspect, Tuple supports the same functions as List.
```python
# Initialize tuple
t = (1, 2, 3)

# Make sure to add a comma to initialize single element tuple correctly
# Otherwise it is treated as integer
t = (1,)

# As tuples are immutable, this will raise a TypeError
t[0] = 4

# Allowed
d = {(1, 2): 'value'} # Tuple as dict keys
s = {(1, 2), (3, 4)}  # Tuple as set elements

# Unpacking
def multi_value_func():
    return 1, 2, 3
x, y, z = multi_value_func()
```
Important Set Functions and Techniques

    A set stores unique elements.
    Set in Python are implemented using hash tables. So insertion, lookup, and deletion have (amortized) have time complexity of O(1).
    Unlike `remove`, `discard` removes an element if exists in the set otherwise it DOES NOT throw an error.
    From python 3.7 onwards, Set maintains insertion order. So iterating over it returns elements in the same order as they were inserted.

    Defining and accessing set
```python
s = set() # Defining an empty set
s.add(1) # Adding element
size = len(s) # Getting size of set

# Adding multiple elements to set
s.update([1,2,3])

# Removing already added element
if 1 in s:
  s.remove(1)
else:
  print("Removing an element that does not exist in set, throws KeyError.")

# Removing element irrespective of whether it exists in set or not
s.discard(1)

# Checking whether set is empty
if len(s) == 0:
  print("Set is empty")
if not s:
  print("Set is either empty or s is None")

# Looking for an element
if 1 in s:
  print("1 is part of set")

# Iterating over set
s = set([1,2])
for i, x in enumerate(s):
    print(f"Insertion Index {i} : Element : {x}")

    Initialising set

# Initialising set
s = {1,2}  # From raw values
s = set([1,2]) # From list
s = set((1,2,)) # From tuple
s = set({"a": "1"}) # From dictionary. Considers only keys
```
    Important functions on multiple sets and their behaviour

    Union ( | ) : O(len(s1) + len(s2))
    Intersection ( & ) : O(min(len(s1), len(s2))
    Difference ( — ) : O(len(s1))
    Symmetric Difference ( ^ ) : O(len(s1) + len(s2))
    Subset Test ( ≤ ) : O(len(s1))
    Superset Test ( ≥ ) : O(len(s2))
```python
s1 = {1,2,3}
s2 = {3,4,5}

union_set = s1 | s2 # {1,2,3,4,5}

intersection_set = s1 & s2 # {3}

diff_set = s1 - s2 # {1,2}

sym_diff_set = s1 ^ s2 # {1,2,4,5} (Just like XOR,returns what is not present in both)

s1 = {1,2,3}
s2 = {1,2,3,4}

s1 <= s2 # Subset test (True)
s1 >= s2 # Superset test (False)
```
Important Stack Functions

    In python, List can be used as Stack.
```python
# Initializing
stack = []

stack.append(1) # Push
x = stack[-1] # Top / Peek
x = stack.pop() # Pop
size = len(stack) # # Getting size of stack

if len(stack) == 0:
   print("Stack is empty")
```
Important Deque Functions and Techniques

    Deque stands for Double-Ended Queue and allows accessing elements from both ends (rear and front).

    Defining and accessing deque

    For most algorithms (e.g. BFS), one would use either append and popleft or appendleft and pop for accessing elements from deque.
    Deque allows accessing elements using an index just like a list.
```python
from collections import deque

dq = deque() # Defining an empty deque

# Appending element at rear/back
dq.append(1)

# Appending element at front/head
dq.appendleft(1)

# Removing and getting element from rear/back
x = dq.pop()

# Removing and getting element from front/head
x = dq.popleft()

size = len(dq) # Getting length/size of deque

x = dq[-1] # Accessing element at rear
x = dq[0] # Accessing element at front
x = dq[3] # Accessing element at any index

# Checking whether deque is empty
if len(dq) == 0:
  print("Deque is empty")

# Looking for an element
if 1 in dq:
  print("1 is part of deque")

# Iterating over deque
for i, x in enumerate(dq):
    print(f"Index {i} : Element : {x}")

l1 = sorted(dq) # Sorted operation returns new list which is sorted
```
    Initialising deque
```python
from collections import deque

# Initializing from list
dq = deque([1,2,3,4]) # deque([1, 2, 3, 4])

# Initializing from string
dq = deque("abcd") # deque(['a', 'b', 'c', 'd'])

# Initializing from dictionary
d1 = {"one":1, "two": 2, "three": 3, "four": 4}
dq = deque(d1.items()) # deque([('one', 1), ('two', 2), ('three', 3), ('four', 4)])
```
    Deque with fixed size

    If deque is defined with a fixed length then every time the append operation is performed and length is exceeded, an element from the opposite direction (of append operation) is removed.
```python
from collections import deque

dq = deque(maxlen=4) # Defining deque with maximum length of 4

dq = deque([-1,1,2,3,4], maxlen=4) # -1 is not included

dq.append(5) # 1 is removed as append has been performed on rear end

dq = deque([1,2,3,4], maxlen=4)

dq.appendleft(0) # 4 is removed as append has been performed on front end
```