import os

# Define the license comment block to be removed
license_comment_block = """

"""


def remove_license(file_path):
    with open(file_path) as file:
        content = file.read()

    # Remove the specific license comment block
    updated_content = content.replace(
        license_comment_block.strip(), ""
    ).strip()

    with open(file_path, "w") as file:
        file.write(updated_content)


def remove_from_repo(repo_path):
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                remove_license(file_path)


if __name__ == "__main__":
    # Path to the specific directory you want to process
    repo_path = "."
    remove_from_repo(repo_path)
