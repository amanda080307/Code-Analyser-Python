from functools import wraps
from contextlib import redirect_stdout
import io

def func_running(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Currently running: {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper

def count_issues(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f = io.StringIO()
        with redirect_stdout(f):
            result = func(*args, **kwargs)

        output = f.getvalue()
        output_lines = output.split('\n')

        count = 0
        for line in output_lines:
            line = line.strip().lower()
            if line and 'correct' not in line:
                count += 1

        print(output, end="")
        print(f'{func.__name__}: {count} issues found.')
        return result
    return wrapper
      
def skip_empty_file(func):
    @wraps(func)
    def wrapper(lines, *args, **kwargs):
        if not lines:
            print(f"{func.__name__} not running: empty lines.")
            return
        result = func(lines, *args, **kwargs)
        return result
    return wrapper