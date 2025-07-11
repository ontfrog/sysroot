from setuptools import setup, find_packages

setup(
    name="sysroot",
    version="1.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sysroot=sysroot.cli:main"
        ]
    },
    description="Native CLI systemless root tool for Android",
    author="YourName",
    license="Unlicense",
    classifiers=[
        "License :: OSI Approved :: The Unlicense",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: Android",
    ],
    install_requires=[],
)
