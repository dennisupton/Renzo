from setuptools import setup, find_packages

setup(
    name="renzo",
    version="0.1.0",
    description="A Python package by renzo.",
    author="renzo",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
