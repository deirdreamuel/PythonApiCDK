import setuptools

setuptools.setup(
    name="infrastructure",
    package_dir={"": "infra"},
    packages=setuptools.find_packages(where="infra"),
    install_requires=[
        "black",
    ],
)
