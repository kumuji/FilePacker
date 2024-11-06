from setuptools import find_packages, setup

setup(
    name="FilePacker",
    version="0.2.0",
    description="A small and simple API for packing an arbitrary directory tree into a 'filepack'.",
    author="Ali Athar",
    author_email="athar@vision.rwth-aachen.de",
    url="https://github.com/ali2500/filepacker",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "filepacker = file_packer.main:main",
        ],
    },
)
