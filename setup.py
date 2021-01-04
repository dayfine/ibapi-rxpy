import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ibrx",
    version="0.0.1",
    author="dayfine",
    author_email="",
    description="IB API using RxPY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dayfine/ibapi-rxpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
