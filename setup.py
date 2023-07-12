# installable setup.py file for s3handler
from setuptools import setup, find_packages

setup(
    name='s3handler',
    version='0.0.1',
    author='Fabian Frank',
    description='S3 handler for AWS',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pandas'
    ],
)
