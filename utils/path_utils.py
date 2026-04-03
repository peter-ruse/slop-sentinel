import os


def filepath_to_module_fqn(file_path: str):
    file_path, _ = os.path.splitext(file_path)
    return file_path.rstrip("__init__").replace("/", ".")
