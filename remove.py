import os
import re

def remove_comments_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            line = re.sub(r'#.*', '', line)
            file.write(line)

def remove_comments_from_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                remove_comments_from_file(os.path.join(root, file))

if __name__ == "__main__":
    remove_comments_from_directory(".")