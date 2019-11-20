import subprocess
import pytest
import tempfile
import shutil
import os
import tests.test_globals
import hashlib
import pathlib


def test_version():
    subprocess.check_output(
        "utf8cleaner --version",
        shell=True
    )


def test_debug():
    capture = subprocess.check_output(
        "utf8cleaner --version --debug",
        shell=True
    )
    assert b"debug mode" in capture


def test_cleans_files_ok():
    """fixes up a file exactly like the the one in the examples dir"""
    temp_dir = tempfile.mkdtemp()
    pwd = os.getcwd()

    test_case = "test.txt"
    test_source = tests.test_globals.get_example_path(test_case)
    test_temp = os.path.join(temp_dir, test_case)
    shutil.copy(test_source, test_temp)
    os.chdir(temp_dir)

    subprocess.check_output(
        f"utf8cleaner --input {test_temp}",
        shell=True
    )

    checksum_want = hashlib.md5(pathlib.Path(f"{test_source}.clean").read_bytes()).hexdigest()
    checksum_got =  hashlib.md5(pathlib.Path(f"{test_temp}.clean").read_bytes()).hexdigest()

    assert checksum_want == checksum_got

    os.chdir(pwd)
    shutil.rmtree(temp_dir)


def test_no_changes_ok():
    """doesn't alter a file thats already good"""
    temp_dir = tempfile.mkdtemp()
    pwd = os.getcwd()

    test_case = "good.txt"
    test_source = tests.test_globals.get_example_path(test_case)
    test_temp = os.path.join(temp_dir, test_case)
    shutil.copy(test_source, test_temp)
    os.chdir(temp_dir)

    subprocess.check_output(
        f"utf8cleaner --input {test_temp}",
        shell=True
    )

    checksum_want = hashlib.md5(pathlib.Path(f"{test_source}.clean").read_bytes()).hexdigest()
    checksum_got =  hashlib.md5(pathlib.Path(f"{test_temp}.clean").read_bytes()).hexdigest()

    assert checksum_want == checksum_got

    os.chdir(pwd)
    shutil.rmtree(temp_dir)
