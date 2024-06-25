from setuptools import find_packages
from setuptools import setup

setup(
    name='rosie_school',
    version='0.0.0',
    packages=find_packages(
        include=('rosie_school', 'rosie_school.*')),
)
