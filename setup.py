from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="boostcampapi",
    version="0.1.0",
    author="Alex Keyes",
    author_email="alex.o.keyes@gmail.com",
    description="Unofficial Python API client for Boostcamp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexkeyes/boostcamp-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
    ],
)
