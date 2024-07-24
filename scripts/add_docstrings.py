import os
import re
from typing import List

def add_docstring_to_function(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    inside_function = False
    for i, line in enumerate(lines):
        # Check if the line is a function definition
        if re.match(r'^\s*def\s+\w+\(.*\)\s*->\s*.*:\s*$', line):
            inside_function = True
            function_start = i

        # If inside a function and the next line is not a docstring
        if inside_function and (i == function_start + 1 and not re.match(r'^\s*"""', lines[i])):
            # Add a docstring template
            indent = re.match(r'^\s*', line).group(0)
            docstring = f'{indent}"""\n{indent}TODO: Add a description.\n{indent}"""\n'
            modified_lines.append(docstring)
            inside_function = False

        modified_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

def scan_and_add_docstrings(root_dir: str) -> None:
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                add_docstring_to_function(file_path)
                print(f"Processed {file_path}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    scan_and_add_docstrings(project_root)
    print("Docstring addition complete.")
