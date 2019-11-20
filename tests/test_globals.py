import os


def get_example_path(filename):
    return os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        "../examples",
        filename
    )