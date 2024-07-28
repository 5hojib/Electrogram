import os
import re

def remove_comments_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            # Remove comments from the line
            new_line = re.sub(r'#.*', '', line)
            file.write(new_line)

def remove_comments_from_repo(repo_path):
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                remove_comments_from_file(file_path)

if __name__ == "__main__":
    # Path to your Python package repository
    repo_path = '.'
    remove_comments_from_repo(repo_path)