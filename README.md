# rene

## What?

Unofficial Georgia Tech CS6515 Graduate Algorithms pseudocode to Python 3 transpiler.

## Why?

CS6515 requires you to use 1-based indexing and a heavily-constrained pseudocode to write dynamic programming problems on homework and exams. Naturally, students can't resist writing and running code for homework and practice. Many students practice DP problems with Python and subsequently lose points on homework and exams for using forbidden features, lack of fluency with the pseudocode during crunch time in an exam or outright ignoring requirements. Rene makes it easy to transpile pseudocode to Python to get the best of both worlds (or shoot yourself in the foot less horribly, hopefully; see disclaimer below).

I also wanted an excuse to mess with Lark.

## Name

This language is named Rene after a frog that appeared in some homework problems when I took the course. Everyone loves Rene.

## Disclaimer

No guarantees expressed or implied. Use this software at your own risk.

When I took the course, the instructional team did not condone anything other than hand-writing and hand-executing your pseudocode. Relying on Rene may harm your grade, which is completely your responsibility.

## Syntax

Rene is a heavily constrained Python-like (whitespace significant) toy language that attempts to disallow any features or syntax that isn't allowed on homework or exams. Notably:

- All you get are variables, ints, fixed-size arrays, loops, conditions and function calls. You can call plain Python functions like `print` but not instance methods.
  - You should restrict your function calls to `max`, `min`, `abs` and that ilk.
- No augmented assignments like `+=` or `++`. Use `foo = foo + 1`.
- No dicts or dynamic arrays/lists exist. Use fixed arrays.
- No `len(iterable)`. Pass explicit length variables into the function header and use those.
- No `for i in range(0, n):`. Use `for i = 1 -> n:`, where `n` is inclusive and transpiles to `for i in range(1, n + 1)`.
- No `and` and `or`. Use `&&` and `||`.
- 4-space indentation only.
- Only `/` is allowed for division. `//` is a comment. If you need floor division, add `from math import floor` and use `floor()` explicitly, but you probably won't need this, or floating point anything for that matter.

Some syntactical restrictions are due to my own ignorance. Please PR if you can fix these:
- Blank lines are allowed, but the spaces in the lines need to match the current indentation level.
- `else if`, `elif` and `elsif` are `elseif` in this language. `else if` is probably safer for your submissions, so you can manaully make that adjustment. That said, you probably won't need to use `else if`.

You can infer the rest of the syntax from the example `lcs.rene` and grammar `rene.lark`.

There is no semantic analyzer in Rene, only parsing errors, so it's up to you to debug everything else in Python, which will mostly look like the Rene code other than line numbers and a few extra array conversion calls.

### Arrays and 1-indexing

Rene uses an `Array` type as a macro for making an `np.array`. `Array` prepends an extra row of zeroes on every dimension, giving you the option to index at 0 and enabling 1-based indexing otherwise.

There are two function calls that make 1-indexed arrays:
- `array_of_zeros(*dimensions)` (alias: `table_of_zeros`): although this array is zero-initialized, it's a very good idea to write loops to initialize it explicitly.
- `array_from_iterable(it)`: converts an iterable to a 1-indexable iterable. You should probably never call this, but the transpiler will insert calls for you on any `Array` parameters to make them 1-indexed NumPy arrays. 

This design decision adds a dependency on NumPy but cuts down on boilerplate and makes it easier to debug code (NumPy arrays print nicely, for example). Feel free to suggest a better approach if you know of one.

Rene will translate any iterable parameters, including strings, into `np.array`s. Your parameters will pretty much always be `Int`s and `Array`s. Rene does support plain strings but they're not 1-indexed and should only be used for debugging rather than DP logic.

See `lcs.rene` for example code.

## Usage

### Dependencies

Python 3, [Lark](https://github.com/lark-parser/lark) and [NumPy](https://numpy.org) (`pip install lark-parser numpy`).

### To stdout

```
python3 rene.py lcs.rene
```

### To file

```
python3 rene.py lcs.rene lcs.py
```

### As a module

```
import rene

# from source file to string
py_code = rene.generate_code(source_file="lcs.rene")

# from source file to out file and string
py_code = rene.generate_code(source_file="lcs.rene", out_file="lcs.py")

# from source code string to out file and string
py_code = rene.generate_code(source_string='print("hello")', out_file="hello.py")

# from source code string to string
py_code = rene.generate_code(source_string='print("hello")')
```

### Using a test harness

If you want to run your code in a test harness, see the `lcs_test.py` example. It might be smart to write your code to .py as well so you can look at it for line numbers for debugging errors (yes, this is not fancy).

### Testing Rene

Coming soon

## TODO

- improve comment support
- add tests

## Issues and PRs

Yes, please

