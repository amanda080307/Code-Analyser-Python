import ast
import re
from decorators import func_running, count_issues

class DocstringChecker(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_FunctionDef(self, node):
        if ast.get_docstring(node) is None:
            print(f'Line {node.lineno}: missing doctring in function {node.name}')
            self.found = True
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if ast.get_docstring(node) is None:
            print(f'Line {node.lineno}: missing doctring in class {node.name}')
            self.found = True
        self.generic_visit(node)

@func_running
@count_issues
def docstring_check(tree):
    checker = DocstringChecker()
    checker.visit(tree)

    if not checker.found:
        print("Doctring check: done, everything is correct.")


class ModuleChecker(ast.NodeVisitor):
    def __init__(self):
        self.found = False
        self.imports = set()
        self.used = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used.add(node.id)
        self.generic_visit(node)


@func_running
@count_issues   
def module_check(tree):
    checker = ModuleChecker()
    checker.visit(tree)

    unused = checker.imports - checker.used
    for i in unused:
        print(f'Module {i} is not used.')
        checker.found = True

    if not checker.found:
        print('Module check: done, everything is correct.')


class FuncnameChecker(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_FunctionDef(self, node):
        if not re.fullmatch(r'[a-z_][a-z0-9_]*', node.name):
            print(f'Line {node.lineno}: function name should not have uppercase letters.')
            self.found = True
        self.generic_visit(node)


@func_running
@count_issues
def func_name(tree):
    checker = FuncnameChecker()
    checker.visit(tree)

    if not checker.found:
        print('Function name check: done, everything is correct.')


class ClassnameChecker(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_ClassDef(self, node):
        if node.name[0].islower():
            print(f"Line {node.lineno}: class name should begin with a capital letter.")
            self.found = True
        self.generic_visit(node)


@func_running
@count_issues
def class_name(tree):
    checker = ClassnameChecker()
    checker.visit(tree)

    if not checker.found:
        print('Class name check: done, everything is correct.')


class VariableCheck(ast.NodeVisitor):
    def __init__(self):
        self.found = False
        self.variables = set()
        self.used = set()
    
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
                self.found = True
            elif isinstance(target, (ast.List, ast.Tuple)):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.variables.add(elt.id)
                        self.found = True
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        target = node.target
        if isinstance(target, ast.Name):
            self.variables.add(target.id)
            self.found = True
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)


@func_running
@count_issues
def variable_check(tree):
    checker = VariableCheck()
    checker.visit(tree)
    unused = checker.variables - checker.used  

    for i in unused:
        print(f'{i} has not been used.')
    
    if not checker.found:
        print('Variable check: done, everything is correct.')


class ArgumentsCheck(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_FunctionDef(self, node):
        total = len(node.args.args)
        if node.args.vararg:
            total += 1
        if node.args.kwarg:
            total += 1

        if total > 5:
            print(f"{node.lineno}: too many arguments on this function.")
            self.found = True
        self.generic_visit(node)


@func_running
@count_issues
def argument_check(tree):
    checker = ArgumentsCheck()
    checker.visit(tree)

    if not checker.found:
        print('Argument check: done, everything is correct.')

class ExceptionCheck(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_ExceptHandler(self, node):
        if node.type is None:
            print(f'Line {node.lineno}: exception has been defined but its type is not specified.')
            self.found = True
        self.generic_visit(node)

@func_running
@count_issues
def exception_check(tree):
    checker = ExceptionCheck()
    checker.visit(tree)

    if not checker.found:
        print('Exception check: done, everything is correct.')