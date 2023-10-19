from setuptools import setup

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="Selector",
    version="0.0.1",
    description="Curated list math",
    author="arfy slowy",
    packages=["Selector"],
    python_requires=">=3.7",
    install_requires=requirements,
)