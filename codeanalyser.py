import argparse
import ast
from atc_checks import docstring_check, module_check, func_name, class_name, variable_check, argument_check, exception_check
from line_checks import length_check, whitespace_check, constructive_whitelines, identation_check, comment_check
from advanced_ast_checks import complexity_check, func_leng_check, builtin_check


line_checks = [length_check, whitespace_check, constructive_whitelines, identation_check, comment_check]

ast_checks = [docstring_check, module_check, func_name, class_name, variable_check, argument_check, exception_check, complexity_check, func_leng_check, builtin_check]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('file_name', type=str, help='Insert the file name.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Additional info.')
    parser.add_argument('-a', '--arguments', choices=['ast', 'line', 'both'], help='Choose which checks you wish to do.')

    args = parser.parse_args()

    user_file = args.file_name

    try:
        with open(user_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print('File does not exist. Please try again.')
        return 

    if args.verbose:
        print(f'Currently checking: {user_file}')
        print('~' * 40)

    code = ''.join(lines)
    tree = ast.parse(code)
    
    if args.arguments in ['line', 'both']:
       print('-----Line Check-----')
       for check in line_checks:
            check(lines)
            print('-' * 40)
 
    if args.arguments in ['ast', 'both']:
        print('-----Ast Checks-----')
        for check in ast_checks:
            check(tree)
            print('-' * 40)


if __name__ == '__main__':
    main()