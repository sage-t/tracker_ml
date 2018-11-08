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
    url="https://github.com/sage-t/tracker_ml",
    download_url='https://github.com/sage-t/tracker_ml/archive/v0.0.1.tar.gz',
    keywords=['MACHINE', 'LEARNING', 'VERSION', 'TRACKING', 'TRACKER'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    entry_points={
        'console_scripts': [
            'tracker = tracker_ml.tools.cli:cli'
        ]
    },
)
