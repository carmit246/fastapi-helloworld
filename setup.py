"""
Setup file for fastapi-helloworld
Allows installation in development mode: pip install -e .
"""
from setuptools import setup, find_packages

setup(
    name="fastapi-helloworld",
    version="1.0.0",
    description="FastAPI Hello World microservice",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Read from requirements.txt
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "httpx>=0.24.0",
            "darker[isort]>=1.7.0",
            "flake8>=6.0.0",
            "pip-audit>=2.6.0",
            "safety>=2.3.0",
        ]
    },
)
