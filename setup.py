# setup.py
from setuptools import setup, find_packages

setup(
    name='dash-ec2-wrapper',
    version='0.1.8',
    description='A custom Dash class for deployment on AWS EC2 instances',
    author='Darien Nouri',
    author_email='nouri.darien@gmail.com',
    url='https://github.com/DarienNouri/dash-wrapper',
    packages=find_packages(),
    install_requires=[
        'dash',
        'python-dotenv'
    ],
)
