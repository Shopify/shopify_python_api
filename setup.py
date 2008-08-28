from distutils.core import setup

version = '0.3'

setup(name='pyactiveresource',
      version=version,
      description='ActiveResource for Python',
      author='Jared Kuolt',
      author_email='me@superjared.com',
      url='http://code.google.com/p/pyactiveresource/',
      packages=['pyactiveresource'],
      package_dir={'pyactiveresource':'src'},
      license='MIT License',
      platforms=['any'],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers', 
                   'License :: OSI Approved :: MIT License', 
                   'Operating System :: OS Independent', 
                   'Programming Language :: Python', 
                   'Topic :: Software Development', 
                   'Topic :: Software Development :: Libraries', 
                   'Topic :: Software Development :: Libraries :: Python Modules']
      
    )
