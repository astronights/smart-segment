from setuptools import setup, find_packages

setup(
    name='smart-segment',
    version='0.1.0',
    packages=find_packages(),  # Automatically finds the smart_segment package
    install_requires=[
        'numpy',
        'scipy',
    ],
)