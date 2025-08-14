"""
Setup configuration for EasyWorship to ProPresenter Converter
"""

from setuptools import setup, find_packages

VERSION = "1.1.5"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ewexport",
    version=VERSION,
    author="Karl Linder",
    description="Convert songs from EasyWorship 6.1 to ProPresenter 6 format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karllinder/ewexport",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Religion",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.8",
    install_requires=[
        "striprtf>=1.6",
    ],
    entry_points={
        "console_scripts": [
            "ewexport=src.main:main",
        ],
    },
)