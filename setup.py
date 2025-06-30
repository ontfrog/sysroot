from setuptools import setup, find_packages

setup(
    name="sysroot",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sysroot=sysroot.cli:main"
        ]
    },
    description="Native systemless root CLI tool for Android",
    author="YourName",
    license="MIT",
)
