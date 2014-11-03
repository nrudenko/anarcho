from setuptools import setup, find_packages


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
    install_requires=[
        'Flask==0.10.1',
        'Flask-Cors==1.3.1',
        'Flask-Login==0.2.11',
        'Flask-SQLAlchemy==1.0',
        'Flask-Script==2.0.5',
        'passlib==1.6.2',
        'CherryPy==3.6.0',
        'Paste==1.7.5.1'
    ],
    entry_points={
        'console_scripts': [
            'anarcho = scripts.anarcho_manage:main',
        ]
    }
)