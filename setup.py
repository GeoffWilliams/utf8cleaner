import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utf8cleaner",
    version="0.0.2",
    author="Geoff Williams",
    author_email="geoff@declarativesystems.com",
    description="remove non-UTF8 bytes from an input file and write a cleaned up version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeoffWilliams/utf8cleaner.git",
    packages=setuptools.find_packages(),
    # pick from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": (['utf8cleaner=utf8cleaner.cli:main'],)
    },
    include_package_data=True,
    install_requires=[]
)
