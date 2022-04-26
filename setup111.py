#!python
from setuptools import setup, Extension
import numpy
from Cython.Build import cythonize
import platform



ext_modules = [
    Extension(
        "example4",
        ["file.pyx"],
        include_dirs=[numpy.get_include()],
    )
]


setup(
    ext_modules=cythonize(ext_modules)
)
