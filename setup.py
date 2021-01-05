# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="sourcegen-antoniojkim",
    version="0.0.1",
    author="Antonio J Kim",
    author_email="contact@antoniojkim.com",
    description="Module that allows you to autogen source code using a template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antoniojkim/SourceGen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # entry_points={"console_scripts": ["sourcegen = sourcegen.sourcegen:main"]},
    # include_package_data=True,
)
