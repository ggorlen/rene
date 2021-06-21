"""
TODO 
- 1-indexing for array accesses
- boilerplate for creating a 1-indexable array with base case
- support comma array access or introduce comma for exprs
"""

import lark
from lark import Lark, Transformer, v_args
from lark.indenter import Indenter


class MainIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []#["LPAR", "LBRACE"]
    CLOSE_PAREN_types = []#["RPAR", "RBRACE"]
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

@v_args(inline=True)
class MainTransformer(Transformer):
    def __init__(self):
        self.indent = 1

    def ws(self, amount=None):
        return "    " * (self.indent if amount is None else amount)

    def start(self, *statements):
        return "\n".join(statements)

    def assignment(self, lhs, expr):
        return f"{lhs} = {expr}"

    def identifier(self, identifier):
        return str(identifier)

    def paren_expr(self, expr):
        return f"({expr})"

    def binary_operator(self, val):
        return str(val)

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

    def array_assignment(self, name, *args):
        *exprs, expr = args
        return f"{name}{''.join([f'[{x}]' for x in exprs])} = {expr}"

    def comment(self, comment_open, comment, newline):
        space = "" if comment.startswith(comment_open) else " "
        return f"{comment_open.value}{space}{comment.value}"

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
        return f"for {name} in range({expr_start}, {expr_end}):\n{block}"

    def blank_line(self):
        return ""

    def func_def(self, name, *args):
        *params, block = args
        return f"def {name}({', '.join(params)}):\n{block}"


grammar = r"""
?start: statement*

?statement: expr _NL
          | blank_line
          | comment
          | for_block
          | if_block
          | func_def
          | assignment
          | array_assignment
          | return_statement

func_def: "function" NAME "(" ((NAME ",")* NAME)? "):" block
return_statement: "return" expr _NL
assignment: NAME "=" expr _NL
array_assignment: NAME ("[" expr "]")+ "=" expr _NL
!comment: "#" /[^\n]+/x _NL
!if_block: "if" expr ":" block ("elseif" expr ":" block)* ("else" ":" block)?
for_block: "for" NAME "=" expr "->" expr ":" block

?expr: string
     | number
     | identifier
     | array_access
     | func_call
     | binary_operation
     | paren_expr

string: STRING
number: NUMBER
identifier: NAME
array_access: NAME ("[" expr "]")+
func_call: NAME "(" ((expr ",")* expr)? ")"
binary_operation: expr binary_operator expr
paren_expr: "(" expr ")"

!binary_operator: "+" | "-" | "/" | "*" | "%" | ">" | ">=" | "<" | "<=" | "==" | "||" | "or" | "&&" | "and" | "&" | "|"
?block: _NL indent statement+ dedent
indent: _INDENT -> indent_
dedent: _DEDENT

%import common.CNAME -> NAME
%import common.ESCAPED_STRING -> STRING
%import common.NUMBER
%import common.WS_INLINE

%declare _INDENT _DEDENT

%ignore WS_INLINE

_NL: /\r?\n(    )*/
blank_line: _NL
//%import common.NEWLINE -> _NL
"""
parser = Lark(grammar, parser="lalr", postlex=MainIndenter())
#python_parser3 = Lark.open('python3.lark', rel_to=__file__, start='file_input',
#                           parser='lalr', postlex=PythonIndenter(),
#                           transformer=Compile(), propagate_positions=False)
#

if __name__ == "__main__":
    test_input = """
# convert 1-index to 0-index

function lcs(n, x, y):
    T = zeroed_array_of_dimensions(n, n)
    
    for i = 0 -> n:
        T[i][0] = 0
    
    for j = 0 -> n:
        T[0][j] = 0
    
    for i = 1 -> n:
        for j = 1 -> n:
            if x[i] == y[j]:
                T[i][j] = T[i-1][j-1] + 1
            elseif 42 == 34:
                print("OK")
            elseif 42 || ((5 < 6) and 55 >= 2):
                if asd() <= 42 | 6:
                    print("OK")
                print("OK")
            else:
                T[i][j] = max(T[i-1][j], T[i][j-1])
    
    return T[n][n]
"""
    tree = parser.parse(test_input)
    print(MainTransformer().transform(tree))

