import os

def print_tree(start_path, skip_dirs=None, prefix=''):
    if skip_dirs is None:
        skip_dirs = ['venv', '__pycache__']
    
    entries = sorted(os.listdir(start_path))
    print(entries)
    entries = [e for e in entries if e not in skip_dirs]
    
    for index, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        connector = '└── ' if index == len(entries) - 1 else '├── '
        print(prefix + connector + entry)
        
        if os.path.isdir(path) and entry not in skip_dirs:
            extension = '    ' if index == len(entries) - 1 else '│   '
            print_tree(path, skip_dirs, prefix + extension)

# Example usage
print_tree('.', skip_dirs=['venv', '__pycache__'])
