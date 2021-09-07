import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='blob_creator',
    version='3.0.0',
    author="Michael Kohlegger",
    author_email="michael@datenberge.org",
    description="Package to create dummy datasets for analysis tasks",
    long_description=long_description,
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
    install_requires=[
        "openpyxl",
        "pandas",
        "numpy",
        "matplotlib",
        "Pillow",
        "names",
        "svglib",
        "reportlab"
    ]
 )
