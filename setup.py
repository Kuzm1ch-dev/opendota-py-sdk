from setuptools import setup, find_packages

setup(
    name="opendota-sdk",
    version="1.0.0",
    description="Professional OpenDota API SDK",
    author="Developer",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "dataclasses>=0.6; python_version<'3.7'"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)