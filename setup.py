import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="androidautotest",
    version="0.0.2.26",
    author="15045120",
    author_email="1337078409@qq.com",
    description="android test framework using adb connection and template matching in opencv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/15045120/AndroidTest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "psutil",
        "pillow",
        "numpy",
        "opencv-python"
    ],
    python_requires='>=3.5',
)
