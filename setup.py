from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='cp3-bench',
    version='0.1',
    description='A symbolic regression benchmark tool for cosmology and particle physics phenomenology',
    license="MIT",
    long_description=long_description,
    author='Mattias Ermakov Thing',
    author_email='thing@cp3.sdu.dk',
    packages=['cp3-bench'],
    install_requires=['wheel', 'click', 'scikit-learn', 'coverage', 'numpy', 'pandas'],
    scripts=['bench/install.py']
)
