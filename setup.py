from setuptools import setup, find_packages

from pyanimelist.constants import LIBRARY_URL
from pyanimelist import (
    __license__ as license,
    __author__ as author,
    __title__ as title,
    __version__ as version
)

setup(
    name=title,
    version=version,
    packages=find_packages("listen"),
    url=LIBRARY_URL,
    license=license,
    author=author,
    author_email="",
    description="Python 3 bindings for the Listen.moe API.",
    long_description="An asynchronous wrapper for the Listen.moe api.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ],
    keywords="aiohttp asyncio listen.moe",
    install_requires=["aiohttp"],
)
