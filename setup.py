"""
Setup configuration for Pinnacle Building Compliance Platform (BPB26)
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bpb26-pinnacle",
    version="1.0.0",
    author="BPB26 Team",
    description="AI-powered building compliance and regulation management platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NaTo1000/BPB26",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "torch>=2.1.0",
        "transformers>=4.35.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "pandas>=2.1.0",
        "PyPDF2>=3.0.0",
        "python-docx>=1.1.0",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bpb26=bpb26.cli:main",
        ],
    },
)
