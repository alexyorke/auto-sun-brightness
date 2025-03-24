from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh.readlines()]

setup(
    name="auto-sun-brightness",
    version="0.1.0",
    author="Alex Yorke",
    author_email="",
    description="Get a numeric representation of how bright the sun is at any point in the day, anywhere",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexyorke/auto-sun-brightness",
    py_modules=["auto_sun_brightness"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "auto-sun-brightness=auto_sun_brightness:main",
        ],
    },
) 