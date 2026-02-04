from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="UAForge",
    version="1.1.2",
    author="bolgac",
    author_email="bytearchsoft@gmail.com",
    description="A powerful Python library and CLI tool for generating realistic, random user agent strings for Chrome, Firefox, and Opera browsers across multiple platforms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bolgac/UAForge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4>=4.13.3",
        "requests>=2.32.3",
        "lxml>=6.0.2",
    ],
    entry_points={
        "console_scripts": [
            "uaforge=uaforge.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "uaforge": ["data/*.db"],
    },
)