import lark
import sys
from lark import Lark, Transformer, v_args
from lark.indenter import Indenter


@lark.v_args(inline=True)
class MainTransformer(Transformer):
    boilerplate = """######## rene boilerplate ########
import numpy as np

def array_of_zeros(*dimensions, dtype=np.int32):
    return np.zeros([x + 1 for x in dimensions], dtype)
table_of_zeros = array_of_zeros

def array_from_iterable(it):
    arr = np.array(tuple(it))
    padded = np.zeros([1 + x for x in arr.shape], dtype=arr.dtype)
    padded[tuple([slice(1, None) for _ in arr.shape])] = arr
    return padded

INFINITY = float("inf")
NEGATIVE_INFINITY = -INFINITY
######## end rene boilerplate ########

"""

    def __init__(self):
        self.indent = 1

    def ws(self, amount=None):
        return "    " * (self.indent if amount is None else amount)

    def start(self, *statements):
        return self.boilerplate + "\n".join(statements)

    def assignment(self, lhs, expr):
        return f"{lhs} = {expr}"

    def identifier(self, identifier):
        return str(identifier)

    def paren_expr(self, expr):
        return f"({expr})"

    def binary_operator(self, val):
        return str(val).replace("||", "or").replace("&&", "and")

    def binary_operation(self, left_expr, val, right_expr):
        return f"{left_expr} {val} {right_expr}"

    def number(self, value):
        return str(value)

    def string(self, value):
        return str(value)

    def func_call(self, name, *exprs):
        return f"{name}({', '.join(exprs)})"

    def array_access(self, name, *exprs):
        return f"{name}{''.join([f'[{x}]' for x in exprs])}"

    def import_(self, name):
        return f"import {name}"

    def from_import(self, name, *modules):
        return f"from {name} import {', '.join(modules)}"

    def array_assignment(self, name, *args):
        *exprs, expr = args
        return f"{name}{''.join([f'[{x}]' for x in exprs])} = {expr}"

    def comment(self, comment_open, comment, newline):
        space = "" if comment.startswith(comment_open) else " "
        return f"#{space}{comment.value}"

    def block(self, indent, *statements):
        return "\n".join([self.ws() + x for x in statements[:-1]])

    def return_statement(self, expr):
        return f"return {expr}"

    def indent_(self):
        self.indent += 1
        return ""

    def dedent(self):
        self.indent -= 1
        return ""

    def if_block(self, if_, expr, colon, block, *args):
        indent = self.ws(self.indent - 1)
        result = [f"if {expr}:\n{block}"]

        for i, x in enumerate(args):
            if isinstance(x, lark.lexer.Token):
                if x.value == "elseif":
                    elseif_expr = args[i+1]
                    elseif_block = args[i+3]
                    elseif = f"{indent}elif {elseif_expr}:\n{elseif_block}"
                    result.append(elseif)
                elif x.value == "else":
                    else_block = args[i+2]
                    result.append(f"{indent}else:\n{else_block}")
        
        return "\n".join(result)

    def for_block(self, name, expr_start, expr_end, block):
        return f"for {name} in range({expr_start}, ({expr_end}) + 1):\n{block}"

    def blank_line(self):
        return ""

    def type_(self, value):
        return str(value)

    def func_def(self, func_name, *args):
        *params, block = args
        arrs = []

        for name, type_ in zip(params[::2], params[1::2]):
            if type_ == "Array":
                arrs.append(f"{self.ws()}{name} = array_from_iterable({name})")
        
        arrs = "\n".join(arrs)
        return f"def {func_name}({', '.join(params[::2])}):\n{arrs}\n{block}"


class MainIndenter(Indenter):
    NL_type = "_NL"
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 4


def generate_code(source_file, out_file=None):
    parser = Lark.open(
        "rene.lark",
        rel_to=__file__,
        parser="lalr",
        postlex=MainIndenter(),
    )

    with open(source_file) as f:
        tree = parser.parse(f.read())

    py_code = MainTransformer().transform(tree)

    if out_file is not None:
        with open(out_file, "w") as f:
            f.write(py_code)

    return py_code


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("usage: python3 rene.py source_file.rene [out_file.py]")
        sys.exit()
    
    if len(sys.argv) < 3:
        print(generate_code(sys.argv[1]))
    else:
        generate_code(sys.argv[1], sys.argv[2])

