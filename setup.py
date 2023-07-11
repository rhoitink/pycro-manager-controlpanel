from setuptools import setup, find_packages

setup(
    name="pycontrolpanel",
    version="0.1.0",
    author="Roy Hoitink",
    author_email="L.D.Hoitink@uu.nl",
    long_description=open("README.md").read(),
    packages=find_packages(include=["pycontrolpanel", "pycontrolpanel.*"]),
    entry_points={
        "console_scripts": [
            "pycontrolpanel=pycontrolpanel.__main__:main",
        ]
    },
    install_requires=[
        "pyserial",
        "pyqt6",
        "pycromanager==0.15.0",
        "numpy==1.22.1",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
        ]
    },
)