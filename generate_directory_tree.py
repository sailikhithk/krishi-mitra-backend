import os


def generate_directory_tree(root_dir, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = []

    with open("directory_tree.txt", "w") as file:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Filter out directories to ignore
            dirnames[:] = [
                d for d in dirnames if d not in ignore_dirs and "venv" not in d
            ]

            level = dirpath.replace(root_dir, "").count(os.sep)
            indent = " " * 4 * (level)
            file.write(f"{indent}{os.path.basename(dirpath)}/\n")

            subindent = " " * 4 * (level + 1)
            for f in filenames:
                file.write(f"{subindent}{f}\n")


# Generate directory tree ignoring the 'venv' directory
generate_directory_tree(".", ignore_dirs=["venv", ".git"])
