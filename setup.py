from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    version="0.1",
    name="pylognet",
    include_package_data=True,
    package_dir={"": "./src"},
)
