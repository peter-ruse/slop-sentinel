import ast
import zipfile
from io import BytesIO
from typing import Generator

from utils.transforms import filepath_to_module_fqn


def get_asts(zip_buffer: BytesIO) -> Generator[tuple[str, ast.AST], None, None]:
    zip_buffer.seek(0)

    with zipfile.ZipFile(zip_buffer) as zip_file:
        for filename in zip_file.namelist():
            if filename.endswith(".py"):
                with zip_file.open(filename) as file_obj:
                    source_code = file_obj.read()
                    tree = ast.parse(source_code, filename=filename)
                    module_fqn = filepath_to_module_fqn(filename)
                    yield module_fqn, tree
