import ast
from decorators import func_running, count_issues

class ComplexityChecker(ast.NodeVisitor):
    def __init__(self):
        self.occurrence = 0

    def visit_If(self, node):
        self.occurrence += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.occurrence += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.occurrence += 1
        self.generic_visit(node)

class FunctionComplexityChecker(ast.NodeVisitor):
    def __init__(self):
        self.threshold = 10
        self.found = False

    def visit_FunctionDef(self, node):
        checker = ComplexityChecker()
        for stmt in node.body:
            checker.visit(stmt)
        if checker.occurrence > self.threshold:
            print(f'Line {node.lineno}: the function <{node.name}>is too complex.')
            self.found = True
        self.generic_visit(node)

@func_running
@count_issues
def complexity_check(tree):
    checker = FunctionComplexityChecker()
    checker.visit(tree)

    if not checker.found:
        print('Complex function check: done, everything is correct.')


class FuncLineCheck(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_FunctionDef(self, node):
        if hasattr(node, 'end_lineno'):
            length = node.end_lineno - node.lineno + 1
            if length > 40:
                print(f'{node.name} is too long({length} lines).')
                self.found = True
        else:
            print('Cannot do line check on this program due to python version.')
        self.generic_visit(node)

@func_running
@count_issues
def func_leng_check(tree):
    checker = FuncLineCheck()
    checker.visit(tree)

    if not checker.found:
        print('Line check: done, everything is correct.')


builtin = {"len", "list", "str", "int", "print", "dict", "sum", "max", "min", "set", "float", "input", "type", "id"}

class BuiltinCheck(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            if node.id in builtin:
                print(f'{node.id}: cannot use built in python variables or functions.')
                self.found = True
        self.generic_visit(node)

@func_running
@count_issues
def builtin_check(tree):
    checker = BuiltinCheck()
    checker.visit(tree)
    if not checker.found:
        print('Built in name usage check: done, everything is correct.')