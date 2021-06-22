# rene

## What?

This is a pseudocode to Python 3 transpiler for the OMSCS course [CS6515 Graduate Algorithms](http://omscs.wikidot.com/courses:cs6515).

## Why?

CS6515 requires you to use 1-based indexing and a heavily-constrained pseudocode to write dynamic programming problems on homework and exams. Many students practice DP problems in Python and lose points on homework and exams due to use of forbidden syntax and language features, lack of fluency with the pseudocode or 1-indexing or simply ignoring requirements.

Rene transpiles the pseudocode to Python, enforcing the correct syntax.

## Name

This language is named Rene after a frog that appeared in some homework problems when I took the course. Everyone loves Rene.

## Syntax

See [`lcs.rene`](lcs.rene) for example code and [`rene.lark`](rene.lark) for the grammar.

This is a heavily constrained Python-like (whitespace significant) toy language that attempts to disallow any features or syntax that isn't allowed on homework or exams. Notably:

- All you get are variables, numbers, fixed-size arrays, loops, conditions and function calls. You can call plain Python functions like `print` but not instance methods.
  - You should restrict your function calls to `max`, `min`, `abs` and that ilk.
- No augmented assignments like `+=` or `++`. Use `foo = foo + 1`.
- No dicts or dynamic arrays/lists. Use fixed arrays.
- No `len(iterable)`. Add explicit length variables to the function header.
- No `for i in range(0, n):`. Use `for i = 1 -> n:`, where `n` is inclusive and transpiles to `for i in range(1, n + 1)`.
- No `and` and `or`. Use `&&` and `||`.
- 4-space indentation only.
- Only `/` is allowed for division. `//` is a comment. If you need floor division, add `from math import floor` and call `floor()` explicitly, but you probably won't need this, or floating point anything.

Some syntactical restrictions are due to my own ignorance. Please PR if you can fix these:
- Blank lines are allowed, but the spaces in the lines need to match the current indentation level.
- `else if`, `elif` and `elsif` are `elseif` in this language. `else if` is probably safer for your submissions. That said, you probably won't need to use `else if`.

There is no semantic analyzer in Rene, only parsing errors, so it's up to you to debug in Python, which will mostly look like the Rene code other than line numbers and a few extra array conversion calls.

### Arrays and 1-indexing

Rene uses an `Array` type as a wrapper for making [NumPy `array`s](https://numpy.org/doc/stable/reference/generated/numpy.array.html). `Array` prepends an extra row of uninitialized values on every dimension, giving you the option to index at 0 and enabling 1-based indexing otherwise.

There are two function calls that make 1-indexed arrays:
- `Array(*dimensions)` (alias: `Table`): this array is uninitialized so you'll need to write explicit loops to set values. You can use `INFINITY` and `NEGATIVE_INFINITY` instead of `float("inf")` to keep .
- `array_from_iterable(it)`: converts an iterable to a 1-indexed iterable. You won't need to call this; the transpiler will insert calls for you on any `Array` parameters. Currently, Rene doesn't generate code to stop you from illegally accessing index 0 on these parameters since it's the same structure as your arrays/tables, so take care.

Rene does support strings but they're not 1-indexed. You could call `s = array_from_iterable(s)`, but strings are mainly available for debugging messages rather than DP logic. Use an `Array` parameter if your function receives a string.

## Usage

### Dependencies

Python 3, [Lark](https://github.com/lark-parser/lark) and [NumPy](https://numpy.org). `pip install lark-parser numpy` and download or clone this repo.

### To stdout

```
python3 rene.py lcs.rene
```

### To file

```
python3 rene.py lcs.rene lcs.py
```

### As a module

```python
import rene

# from source file to string
py_code = rene.generate_code(source_file="lcs.rene")

# from source file to out file and string
py_code = rene.generate_code(source_file="lcs.rene", out_file="lcs.py")

# from source code string to out file and string
py_code = rene.generate_code(source_string='print("hello")\n', out_file="hello.py")

# from source code string to string
py_code = rene.generate_code(source_string='print("hello")\n')
```

### Using a test harness

If you want to run your code in a test harness, see [`lcs_test.py`](lcs_test.py) and run it with `python3 lcs_test.py`. It might be smart to write your code to file when you run tests so you can look at it to debug errors (yes, this is not fancy).

### Leetcode

Not really intended, but easy enough. Leetcode has NumPy, so you can run `python3 rene.py lcs.rene` and pipe to clipboard, paste into Leetcode's editor and call your solution from their stub:

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        return lcs(len(text1), len(text2), text1, text2)
```

There are also command-line tools for LC but I haven't tried them. Efficiency might be impaired due to NumPy but I haven't checked.

## Testing Rene

Coming soon

## TODO

- improve comment and multiline string support
- support unary minus?
- add tests
- support named parameters for function calls
- make into a package for easier install

## Disclaimer

No guarantees expressed or implied. Use this software entirely at your own risk.

## Issues and PRs

Yes, please and thanks!

