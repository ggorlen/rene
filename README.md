# rene

## What?

Unofficial Georgia Tech CS6515 Graduate Algorithms pseudocode to Python 3 transpiler.

## Why?

CS6515 requires you to use 1-based indexing and a heavily-constrained pseudocode to write dynamic programming problems on homework and exams. Naturally, students can't resist writing and running code for homework and practice. Most students practice DP problems with Python and subsequently lose points on homework and exams for using forbidden features or outright ignoring requirements. Rene makes it easier write pseudocode as you would on exams without sacrificing testability.

## Name

This language is named Rene after a frog that appears in some problems that were given when I took the course.

## Caution

Absolutely no guarantees expressed or implied. Use this software at your own risk.

When I took the course, the instructional team did not condone anything other than hand-writing and hand-executing your pseudocode, so relying on Rene may harm your grade, which is completely your responsibility.

## Syntax

Rene is a heavily constrained Python-like (whitespace significant) language that attempts to disallow any syntax that isn't allowed on homework or exams. Notably:

- All you get are variables, strings, numbers, arrays, loops, conditions and function calls.
  - You probably should restrict your function calls to `max`, `min`, `abs` and that ilk.
- No augmented assignments like `+=` or `++`. Use `foo = foo + 1`.
- No dicts or dynamic arrays/lists exist. Use fixed arrays.
- No `and` and `or` keywords. Use `&&` and `||`.
- No `for i in range(0, n):`. Use `for i = 1 -> n:`.
- All array accesses are 1-indexed. `T[5]` will be translated as `T[4]` and `for i = 1 -> n:` will be translated as `for i in range(0, n):`.
- -1 out of bounds indexing is allowed for base cases on the special 1-indexed array structure.
- 4-space indentation must be respected.

A couple of syntactical restrictions are due to my own ignorance in using Lark properly. Please PR if you can fix these.
- Blank lines are allowed, but the spaces in the lines need to match a current indentation level.
- `else if`, `elif` and `elsif` are `elseif` in this language. `else if` is probably what you'd use on exams and homeworks. That said, you probably won't need to use `else if` much, if ever.

You can infer the rest of the syntax from the example and from the grammar.

There is no semantic analyzer, only lexing errors, so it's up to you to debug out of bounds array accesses (and pretty much everything else) from the Python interpreter.

## Usage

### Dependencies

Python 3 and Lark (`pip install lark`).

### Print code to stdout

```
python3 rocko.py lcs.rocko
```

## Examples

### To file

```
python3 rocko.py lcs.rocko > lcs.py
```
If you want to use your code in a test harness, `import lcs` in your test suite as follows:



## Testing

```
python3 test/tests.py
```


## Issues and PRs

Yes, please.

