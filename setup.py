from setuptools import setup, find_packages

setup(
    name="isp-checker",
    version="0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["ispcheck = ispchecker.main:main"]},
    install_requires=[
        "requests==2.27.1",
        "cryptography==36.0.1",
    ],
)
