from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='emulate-tornado-server',
      description='Collection of short functions to simplify tornado-based clients testing',
      long_description=long_description,
      version='1.0.0',
      url='https://github.com/risboo6909/emulate_tornado_server',
      author='Boris Tatarintsev',
      author_email='ttyv00@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7'
      ],
      keywords='tornado testing http server client',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=['tornado'])
