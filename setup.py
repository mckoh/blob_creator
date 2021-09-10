"""
Setup Module for Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

import setuptools

with open("README.md", "r", encoding="utf8") as readme_file:
    readme = readme_file.read()

with open('requirements.txt', "r", encoding="utf8") as requirement_file:
    requirements = requirement_file.read().splitlines()

setuptools.setup(
    name='blob_creator',
    version='3.2.5',
    author="Michael Kohlegger",
    author_email="michael@datenberge.org",
    description="Package to create dummy datasets for analysis tasks",
    long_description=readme,
    long_description_content_type="text/markdown",
    url = "https://github.com/mckoh/blob_creator",
    project_urls={
        "Bug Tracker": "https://github.com/mckoh/blob_creator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requirements
 )
