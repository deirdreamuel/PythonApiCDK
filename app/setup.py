from setuptools import setup

setup(
    name="package",
    packages=["src"],
    include_package_data=True,
    install_requires=[
        "flask",
        "cerberus",
        "pylint",
        "black",
    ],
)
