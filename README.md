# rene

## What?

Unofficial Georgia Tech CS6515 Graduate Algorithms pseudocode to Python 3 transpiler.

## Why?

CS6515 requires you to use 1-based indexing and a heavily-constrained pseudocode to write dynamic programming problems on homework and exams. Naturally, students can't resist writing and running code for homework and practice. Most students practice DP problems with Python and subsequently lose points on homework and exams for using forbidden features, lack of fluency with the pseudocode during crunch time or outright ignoring requirements. Rene makes it easy to transpile pseudocode to Python to get the best of both worlds (or shoot yourself in the foot less horribly, hopefully; see disclaimer below).

I also wanted an excuse to mess with Lark.

## Name

This language is named Rene after a frog that appeared in some homework problems when I took the course. Everyone loves Rene.

## Disclaimer

No guarantees expressed or implied. Use this software at your own risk.

When I took the course, the instructional team did not condone anything other than hand-writing and hand-executing your pseudocode. Relying on Rene may harm your grade, which is completely your responsibility.

## Syntax

Rene is a heavily constrained Python-like (whitespace significant) language that attempts to disallow any features or syntax that isn't allowed on homework or exams. Notably:

- All you get are variables, ints, fixed-size arrays, loops, conditions and function calls. You can call plain Python functions like `print` but not object methods.
  - You should restrict your function calls to `max`, `min`, `abs` and that ilk.
- No augmented assignments like `+=` or `++`. Use `foo = foo + 1`.
- No dicts or dynamic arrays/lists exist. Use fixed arrays.
- No `len(iterable)`. Pass explicit length variables into the function header and use those.
- No `for i in range(0, n):`. Use `for i = 1 -> n:`, where `n` is inclusive and translates to `for i in range(1, n + 1)`.
- No `and` and `or` keywords. Use `&&` and `||`.
- 4-space indentation only.
- Only `/` is allowed for division. `//` is a comment. If you need floor division, add `from math import floor` and use `floor()` explicitly, but you probably won't need this, or floating point anything for that matter.

Some syntactical restrictions are due to my own ignorance. Please PR if you can fix these.
- Blank lines are allowed, but the spaces in the lines need to match the current indentation level.
- `else if`, `elif` and `elsif` are `elseif` in this language. `else if` is probably safer for your submissions, so you can manaully make that adjustment. That said, you probably won't need to use `else if`.

You can infer the rest of the syntax from the example and from the grammar.

There is no semantic analyzer in Rene, only parsing errors, so it's up to you to debug everything else in Python.

### Arrays and 1-indexing

Rene uses an `Array` type as a macro for making an `np.array`, prefixes an extra row on every dimension, giving you the option to index at 0 and supporting 1-based indexing otherwise.

There are two function calls that make 1-indexed arrays:
- `array_of_zeros(*dimensions)` (alias: `table_of_zeros`): although this array is zero-initialized, it's a very good idea to write loops to initialize it explicitly.
- `array_from_iterable(it)`: converts an iterable to a 1-indexable iterable. You should probably never call this, but the transpiler will call it on any `Array` parameters. Even if you're calling the function with strings, declare them as `Array` in the Rene parameter list for your function header.

This design decision adds a dependency on NumPy but cuts down on boilerplate and makes it easier to debug code. Feel free to suggest a better approach if you know of one.

Rene will translate any iterable parameters, including strings, into `np.array`s. Rene does support plain strings but they're not 1-indexed and should only be used for debugging rather than DP logic.

See `lcs.rene` for example code.

## Usage

### Dependencies

Python 3, Lark and NumPy (`pip install lark-parser numpy`).

### To stdout

```
python3 rene.py lcs.rene
```

### To file

```
python3 rene.py lcs.rene lcs.py
```

If you want to run your code in a test harness, see the `lcs_test.py` example. It might be smart to write your code to .py as well so you can look at it for line numbers for debugging errors (yes, this is not fancy).

### Running tests

Coming soon

## TODO

- improve comments
- add tests

## Issues and PRs

Yes, please

