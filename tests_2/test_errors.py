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
from src_2.zip import zip_command, unzip_command
from src_2.tar import tar_command, untar_command
from src_2.grep import grep_command


def test_ls_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        ls_command(["nonexistent_dir"], Path.cwd())
        ls_command([""], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_cd_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        current = Path.cwd()
        cd_command(["nonexistent_directory"], current)
        cd_command([""], current)
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_cat_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        cat_command(["nonexistent_file.txt"], Path.cwd())
        cat_command([""], Path.cwd())
        os.makedirs("test_dir", exist_ok=True)
        cat_command(["test_dir"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_cp_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        cp_command(["nonexistent.txt", "copy.txt"], Path.cwd())
        cp_command(["file1.txt"], Path.cwd())
        cp_command([], Path.cwd())
        os.makedirs("dir1", exist_ok=True)
        cp_command(["dir1", "dir2"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_mv_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        mv_command(["nonexistent.txt", "new.txt"], Path.cwd())
        mv_command(["file1.txt"], Path.cwd())
        mv_command([], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_rm_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        rm_command(["nonexistent.txt"], Path.cwd())
        rm_command([""], Path.cwd())
        rm_command([], Path.cwd())
        os.makedirs("test_dir", exist_ok=True)
        rm_command(["test_dir"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_zip_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        zip_command(["nonexistent_dir", "archive.zip"], Path.cwd())
        zip_command(["file.txt"], Path.cwd())
        zip_command([], Path.cwd())
        Path("file.txt").write_text("test")
        zip_command(["file.txt", "archive.zip"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_unzip_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        unzip_command(["nonexistent.zip"], Path.cwd())
        unzip_command([""], Path.cwd())
        unzip_command([], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_tar_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        tar_command(["nonexistent_dir", "archive.tar.gz"], Path.cwd())
        tar_command(["file.txt"], Path.cwd())
        tar_command([], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_untar_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        untar_command(["nonexistent.tar.gz"], Path.cwd())
        untar_command([""], Path.cwd())
        untar_command([], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_grep_errors():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        grep_command(["pattern", "nonexistent.txt"], Path.cwd())
        grep_command(["pattern"], Path.cwd())
        grep_command([], Path.cwd())
        grep_command(["", "file.txt"], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_rm_protection():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        rm_command(["/"], Path.cwd())
        rm_command([".."], Path.cwd())
        rm_command(["."], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def test_empty_commands():
    test_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        os.chdir(test_dir)
        ls_command([], Path.cwd())
        cd_command([], Path.cwd())
    finally:
        os.chdir(old_dir)
        shutil.rmtree(test_dir)


def run_error_tests():
    tests = [
        test_ls_errors,
        test_cd_errors,
        test_cat_errors,
        test_cp_errors,
        test_mv_errors,
        test_rm_errors,
        test_zip_errors,
        test_unzip_errors,
        test_tar_errors,
        test_untar_errors,
        test_grep_errors,
        test_rm_protection,
        test_empty_commands
    ]

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")


if __name__ == "__main__":
    run_error_tests()