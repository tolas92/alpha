from setuptools import find_packages
from setuptools import setup

setup(
    name='ai_server',
    version='0.0.0',
    packages=find_packages(
        include=('ai_server', 'ai_server.*')),
)
