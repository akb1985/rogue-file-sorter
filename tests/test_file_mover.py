import os
import shutil
import tempfile
import pytest
from src.sorter.file_mover import FileMover

@pytest.fixture
def temp_env():
    src = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()
    yield src, dest
    shutil.rmtree(src)
    shutil.rmtree(dest)

def test_get_safe_destination(temp_env):
    _, dest = temp_env
    open(os.path.join(dest, "test.txt"), 'w').close()
    
    safe_path = FileMover.get_safe_destination(dest, "test.txt")
    assert safe_path == os.path.join(dest, "test (1).txt")
    
    open(os.path.join(dest, "test (1).txt"), 'w').close()
    safe_path = FileMover.get_safe_destination(dest, "test.txt")
    assert safe_path == os.path.join(dest, "test (2).txt")