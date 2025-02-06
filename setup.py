from setuptools import setup

NAME = "CachimanAPI"
exec(open("Cachiman/version.py").read())
DESCRIPTION = "CachimanAPI for Python"
LONG_DESCRIPTION = """\
The ShopifyAPI library allows python developers to programmatically
access the admin section of stores using an ActiveResource like
interface similar the ruby Shopify API gem. The library makes HTTP
requests to Shopify in order to list, create, update, or delete
resources (e.g. Order, Product, Collection)."""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="cachiman",
    author_email="developers@cachiman.com",
    url="https://github.com/cachiman/cachiman_python_api",
    packages=["Cachiman", "Cachiman/resources", "Cachiman/utils"],
    scripts=["scripts/cachiman_api.py"],
    license="MIT License",
    install_requires=[
        "pyactiveresource>=2.2.2",
        "PyJWT >= 2.0.0",
        "PyYAML>=6.0.1; python_version>='3.12'",
        "PyYAML; python_version<'3.12'",
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
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
