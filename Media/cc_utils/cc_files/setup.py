from setuptools import setup, find_packages

setup(
    name="cc_files",  # Package name
    version="0.1.0",  # Start with 0.1.0 for initial release
    author="Captain Crunch",
    author_email="your_email@example.com",  # Optional
    description="A collection of general Python utility functions for file and media manipulation.",
    long_description=open("CC_README.md", encoding="utf-8").read(),  # Use your README
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cc_utils",  # Optional
    packages=find_packages(),  # Automatically find all packages in cc_utils/
    python_requires=">=3.10",  # Because you use `list[str]` and `str | None`
    install_requires=[
        # Any dependencies your functions might need (currently standard library only)
        # e.g., "numpy>=1.25.0", "pandas>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
