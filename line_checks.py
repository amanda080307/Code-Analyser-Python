from decorators import func_running, count_issues, skip_empty_file

@skip_empty_file
@func_running
@count_issues
def length_check(lines):
    found = False
    for i, line in enumerate(lines, start=1):    
        if len(line.rstrip('\n')) > 80:
            print(f'Line {i}: length has exceeded 80 characters.')
            found = True
    if not found:
        print('Line check: done, everything is correct.')


@skip_empty_file
@func_running
@count_issues
def whitespace_check(lines):
    found = False
    for i, line in enumerate(lines, start=1):
        if line.rstrip() != line:
            print(f'Line {i} has unnecessary whitespace at the end of it.')
            found = True
    if not found:
        print('Whitespace check: done, everything is correct.')


@skip_empty_file
@func_running
@count_issues
def constructive_whitelines(lines):
    found = False
    blank = 0
    for i, line in enumerate(lines, start=1):
        if line.strip() == '':
            blank += 1
            if blank > 2:
                print(f'Careful! You have exceeded the number of constructive blank lines allowed(2) in line {i}.')
                found = True
        else:
            blank = 0
    if not found:
        print('Contructive white lines check: done, everything is correct.')


@skip_empty_file
@func_running
@count_issues
def identation_check(lines):
    found = False
    for i, line in enumerate(lines, start=1):
        if line.startswith('\t'):
            print(f'Line {i}: identation done with tabs, use spaces.')
            found = True
    if not found:
        print('Identation check: done, everything is correct.')


@skip_empty_file
@func_running
@count_issues
def comment_check(lines):
    found = False
    for i, line in enumerate(lines, start=1):
        if line.strip().startswith('#') and len(line.rstrip('\n')) > 80:
            print(f'Line {i}: comment limit has been exceeded.')
            found = True
    if not found:
        print('Comment check: done, everything is correct.')