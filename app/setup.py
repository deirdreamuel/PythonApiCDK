from setuptools import setup, find_packages

setup(
    name="package",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "cerberus",
        "pylint",
        "black",
        "boto3",
        "requests",
        "serverless-wsgi"
    ],
)
