import subprocess
import pytest

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


def test_bad_command():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(
            "utf8cleaner --bad-command",
            shell=True
        )