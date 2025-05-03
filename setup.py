import os
from setuptools import setup, find_packages

# Function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="driftbench_sdk",
    version="0.1.0",
    packages=find_packages(include=["cli", "cli.*", "sdk*", "driftbench_sdk*"],
                           exclude=["tests*", "roslyn_daemon*"]),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0",
        "uvicorn>=0.15",
        'gunicorn>=20.0; sys_platform != "win32"',  # skip on Windows
        "click>=8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            # Add other dev tools like linters if needed
        ],
        # 'prod' extra mentioned in blueprint's Dockerfile - corresponds to install_requires
        "prod": [] # Core dependencies are already in install_requires
    },
    entry_points={
        "console_scripts": [
            "driftbench=cli.main:cli",
        ],
    },
    author="Manus",
    author_email="manus@example.com",
    description="DriftBench SDK - LLM Response Validation Middleware (Scaffold)",
    long_description=read('README.md') if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    url="https://example.com/driftbench", # Placeholder URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License", # Placeholder license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

