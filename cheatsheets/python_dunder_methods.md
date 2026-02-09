Operation 	Dunder Method Call 	Returns
T(a, b=3) 	T.__init__(x, a, b=3) 	None
repr(x) 	x.__repr__() 	    str
x == y 	    x.__eq__(y) 	    Typically bool 


@functools.total_ordering
Given a class defining one or more rich comparison ordering methods, this class decorator supplies the rest. This simplifies the effort involved in specifying all of the possible rich comparison operations:
The class must define one of __lt__(), __le__(), __gt__(), or __ge__(). In addition, the class should supply an __eq__() method.

Orderability ⚖️

Python's comparison operators (<, >, <=, >=) can all be overloaded with dunder methods as well. The comparison operators also power functions that rely on the relative ordering of objects, like sorted, min, and max.
Operation 	Dunder Method Call 	Returns
< 	__lt__ 	Typically bool
> 	__gt__ 	Typically bool
<= 	__le__ 	Typically bool
>= 	__ge__ 	Typically bool

If you plan to implement all of these operators in the typical way (where x < y would be the same as asking y > x) then the total_ordering decorator from Python's functools module will come in handy.


Operation 	Dunder Method Call 	Returns
x == y 	    x.__eq__(y) 	Typically bool
x != y 	    x.__ne__(y) 	Typically bool
hash(x) 	x.__hash__() 	int

Hashable objects can be used as keys in dictionaries or values in sets. 
All objects in Python are hashable by default, but if you've written a custom __eq__ method then your objects won't be hashable without a custom __hash__ method. 
But the hash value of an object must never change or bad things will happen so typically only immutable objects implement __hash__.

Type conversions and string formatting ⚗️

Python has a number of dunder methods for converting objects to a different type.
Function 	Dunder Method Call 	Returns
str(x) 	    x.__str__() 	str
bool(x) 	x.__bool__() 	bool
int(x) 	    x.__int__() 	int
float(x) 	x.__float__() 	float
bytes(x) 	x.__bytes__() 	bytes
complex(x) 	x.__complex__() 	complex
f"{x:s}" 	x.__format__(s) 	str
repr(x) 	x.__repr__() 	str

Containers and collections 🗃️
Collections (a.k.a. containers) are essentially data structures or objects that act like data stuctures. Lists, dictionaries, sets, strings, and tuples are all examples of collections.

Operation 	Dunder Method Call 	Return Type 	Implemented
len(x) 	    x.__len__() 	integer 	Very common
iter(x) 	x.__iter__() 	iterator 	Very common
for item in x: ... 	x.__iter__() 	iterator 	Very common
x[a] 	    x.__getitem__(a) 	any object 	Common
x[a] = b 	x.__setitem__(a, b) 	None 	Common
del x[a] 	x.__delitem__(a) 	None 	Common
a in x 	    x.__contains__(a) 	bool 	Common
reversed(x) x.__reversed__() 	iterator 	Common
next(x) 	x.__next__() 	any object 	Uncommon

Operation 	Dunder Method Call 	Return Type
x(a, b=c) 	x.__call__(a, b=c) 	any object

These are the binary mathematical arithmetic operators:
Operation 	Left-Hand Method  	Description
x + y 	__add__ 	     	Add / Concatenate
x - y 	__sub__ 	     	Subtract
x * y 	__mul__ 	     	Multiply
x / y 	__truediv__ 	 	Divide
% 	    __mod__ 	     	Modulo
x // y 	__floordiv__ 	 	Integer division
** 	    __pow__ 	     	Exponentiate
x @ y 	__matmul__ 	     	Matrix multiply

These are the binary bitwise arithmetic operators:
Operation 	Left-Hand Method 	Description
x & y 	__and__ 	 	AND
x | y 	__or__ 	 	    OR
x ^ y 	__xor__ 	 	XOR
x >> y 	__rshift__ 	 	Right-shift
x << y 	__lshift__ 	 	Left-shift

These are Python's unary arithmetic operators:
Operation 	Dunder Method 	Variety 	Description
-x 	__neg__ 	Mathematical 	Negate
+x 	__pos__ 	Bitwise 	Affirm
~x 	__invert__ 	Bitwise 	Invert

Built-in math functions 🧮

Python also includes dunder methods for many math-related functions, both built-in functions and some functions in the math library.
Operation 	Dunder Method Call 	Returns
divmod(x, y) 	x.__divmod__(y) 	2-item tuple
divmod(x, y) 	y.__rdivmod__(x) 	2-item tuple
abs(x) 	        x.__abs__() 	float
sequence[x] 	x.__index__() 	int
round(x) 	    x.__round__() 	Number
math.trunc(x) 	x.__trunc__() 	Number
math.floor(x) 	x.__floor__() 	Number
math.ceil(x) 	x.__ceil__() 	Number

Library-specific dunder methods 🧰

Some standard library modules define custom dunder methods that aren't used anywhere else:

dataclasses support a __post_init__ method
Python's copy module will use the __copy__, __deepcopy__, and __replace__ methods if present
sys.getsizeof relies on the __sizeof__ method to get an object's size (in bytes)



Dunder attributes 📇

In addition to dunder methods, Python has many non-method dunder attributes.

Here are some of the more common dunder attributes you'll see:

    __name__: name of a function, classes, or module
    __module__: module name for a function or class
    __doc__: docstring for a function, class, or module
    __class__: an object's class (call Python's type function instead)
    __dict__: most objects store their attributes here (see where are attributes stored?)
    __slots__: classes using this are more memory efficient than classes using __dict__
    __match_args__: classes can define a tuple noting the significance of positional attributes when the class is used in structural pattern matching (match-case)
    __mro__: a class's method resolution order used when for attribute lookups and super() calls
    __bases__: the direct parent classes of a class
    __file__: the file that defined the module object (though not always present!)
    __wrapped__: functions decorated with functools.wraps use this to point to the original function
    __version__: commonly used for noting the version of a package
    __all__: modules can use this to customize the behavior of from my_module import *
    __debug__: running Python with -O sets this to False and disables Python's assert statements

Those are only the more commonly seen dunder attributes. Here are some more:

    Functions have __defaults__, __kwdefaults__, __code__, __globals__, and __closure__
    Both functions and classes have __qualname__, __annotations__, and __type_params__
    Classes have __static_attributes__ and __firstlineno__ attributes (Python 3.13+)
    Instance methods have __func__ and __self__
    Modules may also have __loader__, __package__, __spec__, and __cached__ attributes
    Packages have a __path__ attribute
    Exceptions have __traceback__, __notes__, __context__, __cause__, and __suppress_context__
    Descriptors use __objclass__
    Metaclasses use __classcell__
    Python's weakref module uses __weakref__
    Generic aliases have __origin__, __args__, __parameters__, and __unpacked__
    The sys module has __stdout__ and __stderr__ which point to the original stdout and stderr versions

Additionally, these dunder attributes are used by various standard library modules: __covariant__, __contravariant__, __infer_variance__, __bound__, __constraints__. And Python includes a built-in __import__ function which you're not supposed to use (importlib.import_module is preferred) and CPython has a __builtins__ variable that points to the builtins module (but this is an implementation detail and builtins should be explicitly imported when needed instead). Also importing from the __future__ module can enable specific Python feature flags and Python will look for a __main__ module within packages to make them runnable as CLI scripts.