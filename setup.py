from setuptools import setup, find_packages

setup(
    name='ida_kern',
    version='1.0.0',
    description='Raw IDA Kernel API for IDAPython',
    author='NyaMisty',
    author_email='misty@misty.moe',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
)