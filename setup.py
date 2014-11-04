"""
Anarcho setup script.
"""

from setuptools import setup, find_packages


with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='anarcho',
    version='0.1',
    url='https://github.com/nrudenko/anarcho',
    license='MIT',
    author='Nikolay Rudenko',
    author_email='r.nikolay.e@gmail.com',
    description='Android artifact hosting service',
    long_description='Android artifact hosting service',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'anarcho = scripts.anarcho_manage:main',
        ]
    }
)
