from setuptools import setup, find_packages

setup(
    name="mock-screenshots",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow>=10.0.0",
    ],
    entry_points={
        'console_scripts': [
            'mock-screenshots=mock_screenshots.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to generate mockups from screenshots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/auto-mock-screenshots",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 