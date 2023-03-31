from setuptools import find_packages, setup

with open("requirements.txt") as fh:
    runtime_deps = [x.strip() for x in fh.read().splitlines() if x.strip()]

setup(
    name="volleyball-webscraper",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    python_requires=">=3.6.0",
    install_requires=runtime_deps,
    license="GPL-3.0",
    description="Webscraper for volleyball-tournaments",
    long_description="comming soon",
    long_description_content_type="text/markdown",
    author="Florian Rasbach",
    author_email="github@justcurious.bulc.club",
    url="https://https://github.com/frasbach/WebScrapVolleyball",
)