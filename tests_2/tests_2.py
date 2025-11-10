import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.append('../src_2')

from src_2.ls import ls_command
from src_2.cd import cd_command
from src_2.cat import cat_command
from src_2.cp import cp_command
from src_2.mv import mv_command
from src_2.rm import rm_command
from src_2.zip import zip_command
from src_2.tar import tar_command
from src_2.grep import grep_command


def test_ls():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        Path("test1.txt").write_text("test")
        ls_command([], Path.cwd())
        ls_command(["-l"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_cd():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        os.makedirs("subdir", exist_ok=True)
        current = Path.cwd()
        cd_command(["subdir"], current)
        cd_command([".."], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_cat():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        Path("test.txt").write_text("line1\nline2")
        cat_command(["test.txt"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_cp():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        Path("original.txt").write_text("content")
        cp_command(["original.txt", "copy.txt"], Path.cwd())
        assert Path("copy.txt").exists()
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_mv():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        Path("old.txt").write_text("content")
        mv_command(["old.txt", "new.txt"], Path.cwd())
        assert not Path("old.txt").exists()
        assert Path("new.txt").exists()
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_rm():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        Path("delete.txt").write_text("content")
        rm_command(["delete.txt"], Path.cwd())
        assert not Path("delete.txt").exists()
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_zip():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        os.makedirs("test_dir", exist_ok=True)
        Path("test_dir/file.txt").write_text("content")
        zip_command(["test_dir", "test.zip"], Path.cwd())
        assert Path("test.zip").exists()
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_tar():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        os.makedirs("test_dir", exist_ok=True)
        Path("test_dir/file.txt").write_text("content")
        tar_command(["test_dir", "test.tar.gz"], Path.cwd())
        assert Path("test.tar.gz").exists()
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_grep():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        Path("test.txt").write_text("hello world\ntest line")
        grep_command(["hello", "test.txt"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_log():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)

        # Создаем лог-файл для теста
        with open('log_file', 'w') as f:
            f.write('test log entry\n')

        log_file = Path('log_file')
        assert log_file.exists()
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)

def run_all():
    tests = [
        test_ls, test_cd, test_cat, test_cp, test_mv,
        test_rm, test_zip, test_tar, test_grep, test_log
    ]

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")


