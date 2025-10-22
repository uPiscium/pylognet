from setuptools import setup, find_packages

setup(
    name="pylognet",
    version="0.1.0",
    packages=find_packages(include=["src*"]),
    install_requires=[],
    include_package_data=True,
)
