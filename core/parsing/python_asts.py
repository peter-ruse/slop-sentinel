import ast
import logging
import zipfile
from io import BytesIO
from typing import Generator

from utils.transforms import filepath_to_module_fqn

logger = logging.getLogger(__name__)


def get_asts(zip_buffer: BytesIO) -> Generator[tuple[str, ast.AST], None, None]:
    zip_buffer.seek(0)

    with zipfile.ZipFile(zip_buffer) as zip_file:
        for filename in zip_file.namelist():
            if not filename.endswith(".py"):
                continue

            try:
                with zip_file.open(filename) as file_obj:
                    source_code = file_obj.read()
                    tree = ast.parse(source_code, filename=filename)
                    module_fqn = filepath_to_module_fqn(filename)
                    yield module_fqn, tree
            except SyntaxError as e:
                logger.warning(f"Skipping {filename} due to error: {e}")
            except Exception as e:
                logger.error(
                    f"An unexpected error occurred while parsing {filename}: {e}"
                )
