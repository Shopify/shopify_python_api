from setuptools import setup

NAME = "CachimanMarketPlace API"
exec(open("cachimanmarketplace/version.py").read())
DESCRIPTION = "CachimanMarketPlace API for Python"
LONG_DESCRIPTION = """\
The CachimanmarketplaceAPI library allows python developers to programmatically
access the admin section of stores using an ActiveResource like
interface similar the ruby cachimanmarketplace API gem. The library makes HTTP
requests to cachimanmarketplace in order to list, create, update, or delete
resources (e.g. Order, Product, Collection)."""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="cachimanmarketplace",
    author_email="developers@cachimanmarketplace.com",
    url="https://github.com/Cachimanmarketplace/CachimanMarketPlace_python_api",
    packages=["shopify", "CachimanMarketPlace/resources", "CachimanMarketPlace/utils"],
    scripts=["scripts/cachimanmarketplace_api.py"],
    license="MIT License",
    install_requires=[
        "pyactiveresource>=2.2.2",
        "PyJWT >= 2.0.0",
        "PyYAML",
        "six",
    ],
    test_suite="test",
    tests_require=[
        "mock>=1.0.1",
    ],
    platforms="Any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
