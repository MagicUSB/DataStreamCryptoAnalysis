from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "arithmetic_encoding",
        sorted(glob("src/*.cpp")),  # Sort source files for reproducibility
    ),
]

setup(name = "an_example_pypi_project", ext_modules=ext_modules)
