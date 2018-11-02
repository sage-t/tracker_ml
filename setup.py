import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tracker_ml",
    version="0.0.1",
    author="Sage Thomas",
    author_email="sage.thomas@outlook.com",
    description="Machine learning file and parameter version control SDK for www.tracker.ml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sage-t/tracker_ml_python_sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)