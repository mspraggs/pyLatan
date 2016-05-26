from Cython.Build import cythonize
from Cython.Compiler.Errors import CompileError
from setuptools import Extension, setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='pylatan',
    version='0.0-alpha',
    packages=find_packages(exclude=["*test*"]),
    url='http://github.com/mspraggs/pylatan/',
    author='Matt Spraggs',
    author_email='matthew.spraggs@gmail.com',
    description='Helper tools for interfacing with LatAnalyze.',
    long_description=long_description,
    package_dir={'': '.'},
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        ],
)
