from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='smart-segment',
    version='0.1.5',
    author='Shubhankar Agrawal',
    author_email='shubhankar.a31@gmail.com',
    description='An optimization-based customer segmentation tool for business intelligence',
    long_description=long_description,
    long_description_content_type='text/markdown',  # To support markdown rendering on PyPI
    url='https://github.com/astronights/smart-segment', 
    packages=find_packages(),  # Automatically finds the package directories
    install_requires=[
        'numpy',
        'scipy',
    ],
    extras_require={
        'dev': ['pytest'],  # Optional dependencies for development and testing
    },
    python_requires='>=3.6',  # Specify compatible Python versions
    license='MIT',  # Specify the license
    license_files=('LICENSE',),  # Ensure your LICENSE file is included
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
