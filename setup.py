# coding:utf8
from setuptools import setup, find_packages

from chiral_client import version

setup(
    name="chiral-client",
    version=version,
    description="Python Client for Chiral Computing Cloud",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="Qin Wan",
    author_email="rogerwq@gmail.com",
    url="https://github.com/chiral-data/chiral-client-python",
    packages=find_packages(),
    install_requires=[
    ],
    license="MIT",
    # https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[],
)