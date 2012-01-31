from distutils.core import setup

NAME='ShopifyAPI'
VERSION='0.2.0'
DESCRIPTION='Shopify API for Python'
LONG_DESCRIPTION="""\
The ShopifyAPI library allows python developers to programmatically
access the admin section of stores using an ActiveResource like
interface similar the ruby Shopify API gem. The library makes HTTP
requests to Shopify in order to list, create, update, or delete
resources (e.g. Order, Product, Collection)."""

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='Shopify',
      author_email='developers@jadedpixel.com',
      url='https://github.com/Shopify/shopify_python_api',
      packages=['shopify'],
      package_dir={'': 'lib'},
      scripts=['scripts/shopify_api.py'],
      license='MIT License',
      install_requires=[
          'pyactiveresource>=1.0.0',
          'python-dateutil<2.0', # >= 2.0 is for python>=3.0
          'PyYAML',
      ],
      platforms='Any',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules']
      )
