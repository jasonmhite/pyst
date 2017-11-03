from setuptools import setup

setup(
    name="pyst",
    version="0.1.1",
    author="Jason M. Hite",
    license="BSD",
    packages=["pyst"],
    install_requires=['numpy'],
    license="2-clause BSD (FreeBSD)",
    extras_require={
        "plots": ["matplotlib", "seaborn"],
    },
)                     
