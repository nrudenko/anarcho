"""
Anarcho setup script.
"""

from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='anarcho',
    version='0.5.3',
    url='https://github.com/nrudenko/anarcho',
    license='MIT',
    author='Nikolay Rudenko',
    author_email='r.nikolay.e@gmail.com',
    description='Android and iOs artifacts hosting service',
    long_description='Android and iOs artifacts hosting service',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'anarcho = anarcho.manage:main',
        ]
    }
)
